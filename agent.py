#Authors: Jose F. Martinez Rivera, Adam Cancel

#Domino Class represents a domino object
class Domino:
	
	#Create domino tile
	def __init__(self, side_A, side_B):
		self.side_A = side_A #One side of the tile
		self.side_B = side_B #Other side of the tile

	#Print to the domino tile
	def getTileString(self):
		return "("+self.side_A + "|" + self.side_B + ")"

	#Returns the value of the tile
	def get_value(self):
		return int(self.side_A) + int(self.side_B)

	#Returns true if the tile is double
	def is_double(self):
		return self.side_A == self.side_B

	#See if a tile matches with side A
	def match_sideA(self, tile):

		if self.side_A == tile.side_A:
			return "AA"
		elif self.side_A == tile.side_B:
			return "AB"
		else:
			return "N/A" #No Match

	#See if a tile matches with side B
	def match_sideB(self, tile):
		
		if self.side_B == tile.side_B:
			return "BB"
		elif self.side_B == tile.side_A:
			return "BA"
		else:
			return "N/A" #No Match
	#Flip the domino
	def flip(self):
		temp = self.side_A
		self.side_A = self.side_B
		self.side_B = temp

	def hasSide(self, side):
		if self.side_A == side:
			return True
		elif self.side_B == side:
			return True
		else:
			return False

#Game Board
class GameBoard:

	def __init__(self):
		self.name ="Daz Ruler"
		self.a_list = [Domino("6","6")]
		self.b_list = [Domino("6","6")]
		self.player_names = []
		self.player_tiles = [7,7,7,7]
		self.current_player = 1



	#Append tile to one side of the board
	#It's important to know that all tiles will be connected strictly through side B to side A
	def place_tile(self,tile, side):
		#Choose to place the tile on one side
		if side == "LEFT":
			edge_tile = self.a_list[-1]
			response = edge_tile.match_sideB(tile)
			print(response)
			if response == "BA":
				self.a_list.append(tile)
			elif response == "BB":
				tile.flip()
				self.a_list.append(tile)

		#Choose to place the tile on the other side
		elif side == "RIGHT":
			edge_tile = self.b_list[-1]
			response = edge_tile.match_sideB(tile)
			if response == "BA":
				self.b_list.append(tile)
			elif response == "BB":
				tile.flip()
				self.b_list.append(tile)

	def get_sideA(self):
		listA = ""
		for tile in self.a_list:
			listA += tile.getTileString()

	def get_sideB(self):
		listB = ""
		for tile in self.b_list:
			listB += tile.getTileString()

	def get_edgeA(self):
		return a_list[-1].side_B

	def get_edgeB(self):
		return b_list[-1].side_B

	#Circle between players
	#Get current player name

	def	get_current_player(self):
		index =	self.current_player
		return self.player_names.index(index)

	def add_player(self,name):
		self.player_names.append(name)

	def erase_players(self,name):
		self.player_names = []	
	
	def next_player(self):

		if self.current_player == 4:
			self.current_player = 1
		else:
			self.current_player = self.current_player + 1


	def set_starting_player(self, name):
		index = self.player_names.index(name)
		self.current_player = index


	def player_number_tiles(self,name):
		index = self.player_names.index(name)
		return self.player_tiles[index]


	def update_player_number_tiles(self):
		self.player_tiles[self.current_player] = self.player_tiles[self.current_player] - 1


	



#Domino Player/Agent
class DominoAgent:

	def __init__(self):
		self.name = "Fernando 2.0"

	#Receive Hand
	def establish_hand(self,d1, d2, d3, d4, d5, d6,d7):
		self.domino_hand = [d1,d2,d3,d4,d5,d6,d7]

	#Representation of a Hand
	def get_hand(self):
		hand_string = ""
		for i in self.domino_hand:
			hand_string += i.getTileString() + ","
		return hand_string

	#For initial AI testing purposes, this makes the agent do a random move
	def random_move(self):
		choice = random.randint(0,1)
		if choice == 0: #Aim for the left side
			left_edge = gameboard.get_sideA()
			viable_tiles = getTilesWithSide(left_edge)
			if len(viable_tiles) != 0:
				gameboard.place_tile(getHighestValue(viable_tiles), "LEFT")
			else:
				print("PASS")
		else: #Aim for the right side
			right_edge = gameboard.get_sideA()
			viable_tiles = getTilesWithSide(right_edge)
			if len(viable_tiles) != 0:
				gameboard.place_tile(getHighestValue(viable_tiles), "RIGHT")
			else:
				print("PASS")
				
	#Viable tiles that can be played in an edge
	def getTilesWithSide(self, side):
		viable_tiles = []
		for i in self.domino_hand:
			if i.hasSide(side):
				viable_tiles.append(i)
		return viable_tiles

	#The highest possible tile
	def getHighestValue(self, tiles):
		highest_tile, value = 0
		for i in tiles:
			if(i.get_value > value):
				highest_tile = i #Get the highest tile
				value = i.get_value
		return highest_tile #Return the highest tile


#Class for generating dominos
class DominoGenerator:
	def __init__(self):
		generateDominos()

	def generateDominos(self):
		for i 



