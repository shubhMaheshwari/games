import sys
import random
import signal
import time
import copy
	
import numpy as np


TIME = 16
MAX_PTS = 68
# N = 4


DEPTH = 30
TURN_RAND_STOP = 50 # Stop random moves after move 50
# For min max with pruning 
# turn depth num win lost draw
# 180  4	 10   5   2    3	
# 160  4	 10   4   2    4	
# 160  5	 10   3   0    7	
# 100  30	 10   4   0    6	
# 100  30	 10   4   0    6	
#  0   30	 10   5   2    3	
#  50   30	 10   4   1    5	


class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Team25_minimax():
	# ply is the character x or o
	def __init__(self,ply):
		self.block_number = 0
		self.ply = 1 if ply == 'x' else 0
		self.board = ''
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		possible_moves = board.find_valid_move_cells(old_move)
		# print("Allowed moves:",possible_moves)
		self.board = copy.deepcopy(board)
		# print("Current Board state")
		# self.board.print_board()
		sub_move,move_value = self.min_max(old_move,self.ply,DEPTH)
		# print("move:",sub_move,"value:",move_value)
		return sub_move

	def min_max(self, old_move,ply,depth,alpha = -10000,beta = 10000):		

		bs = self.board 		
		if(depth == 0):
			return old_move, 0

		# print("old move:",old_move)
		possible_moves = bs.find_valid_move_cells(old_move)
		if possible_moves == [] :
			possible_moves = bs.find_valid_move_cells((-1,-1))
		# possible_moves = possible_moves[0:16:4]
		if possible_moves == []:
			winner, message = bs.find_terminal_state()
			# print("winner:",winner,"message:",message)
			if message == 'WON':
				return old_move,5*(DEPTH-depth)
			elif message == 'DRAW':
				return old_move, 0	
			else: 
				return old_move, 0
		# print("possible:",possible_moves)
		
		sub_move = ''
		sub_value = ''
		block_won = 0

		# print("Starting Loop")
		if ply == 1:	
			best_move = '' 
			best_val = -10000
			for move in possible_moves:
				bs.board_status[move[0]][move[1]] = 'x'

				winner, message = bs.find_terminal_state()
				# print("winner:",winner,"message:",message)
				if message == 'WON':
					return move,5*(DEPTH-depth)

				block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'x')
				# print("block_won:",block_won)
				# bs.print_board()

				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'x'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value += DEPTH - depth

				elif block_won == 0:
					bs.block_status[move[0]/4][move[1]/4] = 'd'
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
				
				else:
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)

				# print("sub_move:",sub_move,"sub_value:",sub_value)
				
				# Alpha beta pruning 
				if sub_value > best_val:
					best_val = sub_value
					best_move = move

				alpha = max(alpha,best_val)

				# print("alpha:",alpha,"beta",beta)
				if(beta <= alpha):
					break	


				bs.board_status[move[0]][move[1]] = '-'

			return best_move,best_val

		else:
			best_move = ''
			best_val  = 10000
			for move in possible_moves:
				bs.board_status[move[0]][move[1]] = 'o'

				# bs.print_board()
				winner, message = bs.find_terminal_state()
				if message == 'WON':
					return move,-5*(DEPTH-depth)
				# print("winner:",winner,"message:",message)

				block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'o')
				# print("block_won:",block_won)	
				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'o'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value += depth - DEPTH

				elif block_won == 0:
					bs.block_status[move[0]/4][move[1]/4] = 'd'
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
				
				else:
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)
				# print("sub_move:",sub_move,"sub_value:",sub_value)

				# Alpha beta pruning 
				if sub_value < best_val:
					best_val = sub_value
					best_move = move

				beta = min(beta,best_val)

				# print("alpha:",alpha,"beta",beta)
				if(beta <= alpha):
					break	


				bs.board_status[move[0]][move[1]] = '-'
			# except Exception as e:
			# 	print(possible_moves)
			# 	print(e)
			# 	exit() 		
			return best_move,best_val


class RandomPlayer():
	# ply is the character x or o
	def __init__(self,ply):
		self.block_number = 0
		self.ply = ply
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		possible_moves = board.find_valid_move_cells(old_move)
		# udpate_list = [board.update(old_move,new_move,self.ply) for new_moves in possible_moves]
		# print possible_moves
		# print udpate_list
		return random.sample(possible_moves,1)[0]		

class Manual_Player:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		cells = board.find_valid_move_cells(old_move)
		print 'Valid Moves'
		print cells
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))		

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.board_status = [['-' for i in range(16)] for j in range(16)]
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print 
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print

	# old move = (row,column) row,column = [0,15]
	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules
		if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(16):
					if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))

		return allowed_cells	

	# check whether game is over or not 
	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0
		cntd = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1
				if bs[i][j] == 'd':
					cntd += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				return (col[0],'WON')

		#checking if diamond has been won
		if(bs[1][0] == bs[0][1] == bs[2][1] == bs[1][2]) and (bs[1][0] == 'x' or bs[1][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[1][1] == bs[0][2] == bs[2][2] == bs[1][3]) and (bs[1][1] == 'x' or bs[1][1] == 'o'):
			return (bs[0][0],'WON')
		if(bs[2][0] == bs[1][1] == bs[3][1] == bs[2][2]) and (bs[2][0] == 'x' or bs[2][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[2][1] == bs[1][2] == bs[3][2] == bs[2][3]) and (bs[2][1] == 'x' or bs[2][1] == 'o'):
			return (bs[0][0],'WON')

		if cntx+cnto+cntd <16:		#if all blocks have not yet been won, continue
			return ('-', 'CONTINUE')
		elif cntx+cnto+cntd == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL', False

		self.board_status[new_move[0]][new_move[1]] = ply
		x = new_move[0]/4
		y = new_move[1]/4

		block_won = self.check_block_status(x,y,ply)
		# if won or draw then update the block with player or draw
		if block_won == 1:
			self.block_status[x][y] = ply
		elif block_won == 0:
			self.block_status[x][y] = 'd'
		else:
			pass

		return 'SUCCESSFUL', True if block_won == 1 else False  

	# x,y => which block to check , ply = for which player
	def check_block_status(self,x,y,ply):	
		fl = 0
		bs = self.board_status

		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				return 1
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				return 1

		#checking for diamond pattern
		#diamond 1
		if (bs[4*x+1][4*y] == bs[4*x][4*y+1] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2]) and (bs[4*x+1][4*y] == ply):
			return 1
		#diamond 2
		if (bs[4*x+1][4*y+1] == bs[4*x][4*y+2] == bs[4*x+2][4*y+2] == bs[4*x+1][4*y+3]) and (bs[4*x+1][4*y+1] == ply):
			return 1
		#diamond 3
		if (bs[4*x+2][4*y] == bs[4*x+1][4*y+1] == bs[4*x+3][4*y+1] == bs[4*x+2][4*y+2]) and (bs[4*x+2][4*y] == ply):
			return 1
		#diamond 4
		if (bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x+3][4*y+2] == bs[4*x+2][4*y+3]) and (bs[4*x+2][4*y+1] == ply):
			return 1

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return -1
		# If no cell is remaining then return 0
		return 0

def player_turn(game_board, old_move, obj, ply, opp, flg,turn):
		# print("turn:",turn, "ply:",ply)
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)
		WINNER = ''
		MESSAGE = ''
		pts = {"P1" : 0, "P2" : 0}
		to_break = False
		p_move = old_move
		try:	
			#try to get player 1's move			
			if(turn < TURN_RAND_STOP):
				p_move = saitama3.move(game_board, old_move, flg)
			else:		
				p_move = obj.move(game_board, old_move, flg)
		except TimedOutExc:					#timeout error
#			print e
			WINNER = opp
			MESSAGE = 'TIME OUT'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print(exc_obj,exc_tb.tb_lineno)
			WINNER = opp
			MESSAGE = 'INVALID MOVE'
			pts[opp] = MAX_PTS			
			return old_move, WINNER, MESSAGE , pts["P1"], pts["P2"], False, False,turn
		signal.alarm(0)

		#check if board is not modified and move returned is valid
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = opp
			MESSAGE = 'MODIFIED THE BOARD'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn +1

		update_status, block_won = game_board.update(old_move, p_move, flg)
		# print("move played : ",p_move)
		if update_status == 'UNSUCCESSFUL':
			WINNER = opp
			MESSAGE = 'INVALID MOVE'
			pts[opp] = MAX_PTS
			exit()
			return old_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, False,turn

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		if status[1] == 'WON':	
			#if the game has ended after a player1 move, player 1 would win
			print("Status for win:",status)			
			pts[ply] = MAX_PTS
			WINNER = ply
			MESSAGE = 'WON'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn

		return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, block_won, turn if block_won else turn +1

def gameplay(obj1, obj2):				#game simulator

	game_board = Board()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1)
	WINNER = ''
	MESSAGE = ''	
	pts1 = 0
	pts2 = 0
	turn = 0


	# game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while (turn < 256):
		#player 1 turn
		p_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won,turn = player_turn(game_board, old_move, obj1 if turn%2 == 0 else obj2, "P1" if turn%2 == 0 else "P2" , "P2" if turn%2 == 0 else "P1" , fl1 if turn%2 == 0 else fl2,turn)
		# print(p_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won,turn)
		if to_break:
			break

		old_move = p_move
		# game_board.print_board()

		if block_won:
			# p1_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won = player_turn(game_board, old_move, obj1, "P1", "P2", fl1)
			p_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won,turn = player_turn(game_board, old_move, obj1 if turn%2 == 0 else obj2, "P1" if turn%2 == 0 else "P2" , "P2" if turn%2 == 0 else "P1" , fl1 if turn%2 == 0 else fl2,turn)
			
			if to_break:
				break

			old_move = p_move
			print(turn, MESSAGE)
			game_board.print_board()			

		# #do the same thing for player 2
		# p2_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)

		# if to_break:
		# 	break

		# game_board.print_board()
		# old_move = p2_move

		# if block_won:
		# 	p2_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)
		
		# 	if to_break:
		# 		break
		
		# 	old_move = p2_move
		# 	game_board.print_board()		
	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for i in range(4):
		for j in range(4):
			if game_board.block_status[i][j] == 'x':
				x += 1
			if game_board.block_status[i][j] == 'o':
				o += 1
			if game_board.block_status[i][j] == 'd':
				d += 1
	print 'x:', x, ' o:',o,' d:',d
	if MESSAGE == 'DRAW':

	# After the game is over
		for i in range(4):
			for j in range(4):
				val = 4
				if is_corner(i,j):
					val = 6
				elif is_centre(i,j):
					val = 3
				if game_board.block_status[i][j] == 'x':
					pts1 += val
				if game_board.block_status[i][j] == 'o':
					pts2 += val
	return (pts1,pts2)

def is_centre(row, col):
	if row == 1 and col == 1:
		return 1
	if row == 1 and col == 2:
		return 1
	if row == 2 and col == 1:
		return 1
	if row == 2 and col == 2:
		return 1
	return 0

def is_corner(row, col):
	if row == 0 and col == 0:
		return 1
	if row == 0 and col == 3:
		return 1
	if row == 3 and col == 0:
		return 1
	if row == 3 and col == 3:
		return 1
	return 0

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	saitama1 = ''
	saitama2 = ''
	option = sys.argv[1]	
	if option == '1':
		saitama1 = Team25_minimax('x')
		saitama2 = RandomPlayer('o')
		saitama3 = RandomPlayer('x')

	elif option == '2':
		saitama1 = Team25_minimax('x')
		saitama2 = Manual_Player()
	elif option == '3':
		saitama1 = Manual_Player()
		saitama2 = Manual_Player()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(saitama1, saitama2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]