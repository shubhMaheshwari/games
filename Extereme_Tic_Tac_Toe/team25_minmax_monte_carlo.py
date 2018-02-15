import sys
import random
import signal
import time
import copy
	

class Team25_minimax_monte_carlo():
	# ply is the character x or o
	def __init__(self,ply,depth):
		self.block_number = 0
		self.ply = 1 if ply == 'x' else 0
		self.board = ''	
		self.turn = 2
		self.depth = depth
		self.explore = self.turn
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# print("Allowed moves:",possible_moves)
		self.board = copy.deepcopy(board)
		# print("Current Board state")
		# self.board.print_board()
		
		# IDA instead of DFS

		# for i in range(1,self.turn):
		sub_move,move_value = self.min_max(old_move,self.ply,self.depth)
		print("move:",sub_move,"value:",move_value,"ply:",self.ply)
		

		self.turn += 2

		return sub_move

	def monte_carlo(self,old_move,ply):
		bs = self.board
		possible_moves = bs.find_valid_move_cells(old_move)
		if possible_moves == [] :
			possible_moves = bs.find_valid_move_cells((-1,-1))
		# possible_moves = possible_moves[0:16:4]
		if possible_moves == []:
			winner, message = bs.find_terminal_state()
			# print("winner:",winner,"message:",message)
			if message == 'WON':
				return (5 if ply == 1 else -5)
			elif message == 'DRAW':
				return  0	
			else: 
				return  0
		# print("possible:",possible_moves)

		move = random.sample(possible_moves,1)[0]	
		
		if ply == 1:
			bs.board_status[move[0]][move[1]] = 'x'

			winner, message = bs.find_terminal_state()
			# print("winner:",winner,"message:",message)
			if message == 'WON':
				return 5
			elif message == 'DRAW':
				return 0

			block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'x')
			# print("block_won:",block_won)
			# bs.print_board()

			if block_won == 1:
				bs.block_status[move[0]/4][move[1]/4] = 'x'
				sub_value = self.monte_carlo(move,ply)					
				bs.block_status[move[0]/4][move[1]/4] = '-'
				# Add the reward of winning a block 
				sub_value += 1

			elif block_won == 0:
				bs.block_status[move[0]/4][move[1]/4] = 'd'
				sub_value = self.monte_carlo(move,ply^1)					
				bs.block_status[move[0]/4][move[1]/4] = '-'
			
			else:
				sub_value = self.monte_carlo(move,ply^1)

		elif ply == 0:

			bs.board_status[move[0]][move[1]] = 'o'

			winner, message = bs.find_terminal_state()
			# print("winner:",winner,"message:",message)
			if message == 'WON':
				return -5
			elif message == 'DRAW':
				return 0

			block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'o')
			# print("block_won:",block_won)
			# bs.print_board()

			if block_won == 1:
				bs.block_status[move[0]/4][move[1]/4] = 'o'
				sub_value = self.monte_carlo(move,ply)					
				bs.block_status[move[0]/4][move[1]/4] = '-'
				# Add the reward of winning a block 
				sub_value -= 1

			elif block_won == 0:
				bs.block_status[move[0]/4][move[1]/4] = 'd'
				sub_value = self.monte_carlo(move,ply^1)					
				bs.block_status[move[0]/4][move[1]/4] = '-'
			
			else:
				sub_value = self.monte_carlo(move,ply^1)

		bs.board_status[move[0]][move[1]] = '-'

		return sub_value



	def min_max(self, old_move,ply,depth,alpha = -10000,beta = 10000):		

		bs = self.board 		
		

		# print("old move:",old_move)
		possible_moves = bs.find_valid_move_cells(old_move)
		if possible_moves == [] :
			possible_moves = bs.find_valid_move_cells((-1,-1))
		# possible_moves = possible_moves[0:16:4]
		if possible_moves == []:
			winner, message = bs.find_terminal_state()
			# print("winner:",winner,"message:",message)
			if message == 'WON':
				return old_move,(1 if ply == 1 else -1) *5*(self.depth-depth)
			elif message == 'DRAW':
				return old_move, 0	
			else: 
				return old_move, 0
		# print("possible:",possible_moves)
		
		if(depth == 0):
			mc_sum = 0
			explore = 3*len(possible_moves)
			for i in range(explore):
				mc_sum += self.monte_carlo(old_move,ply)

			mc_sum = 5*float(mc_sum/explore)
			
			# print("mc_sum:",mc_sum)	
			return old_move, mc_sum




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
					return move,5*(self.depth-depth)
				elif message == 'DRAW':
					return move,0

				block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'x')
				# print("block_won:",block_won)
				# bs.print_board()

				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'x'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value += self.depth - depth

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
					return move,-5*(self.depth-depth)
				if message == 'DRAW':
					return move,0
				# print("winner:",winner,"message:",message)

				block_won = bs.check_block_status(old_move[0]/4,old_move[1]/4,'o')
				# print("block_won:",block_won)	
				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'o'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value += depth - self.depth

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