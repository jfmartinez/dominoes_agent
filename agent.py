#Authors: Jose F. Martinez Rivera, Adam Cancel

#Domino Class represents a domino object
class Domino:
	
	#Create domino tile
	def __init__(self, side_A, side_B):
		self.side_A = side_A
		self.side_B = side_B

	#Print to the domino tile
	def getTileString(self):
		return "("+self.side_A + "|" + self.side_B + ")"

	#Returns the value of the tile
	def get_value(self):
		return int(self.side_A) + int(self.side_B)

	#Returns true if the tile is double
	def is_double(self):
		return self.side_A == self.side_B

#Domino Player/Agent
class DominoAgent:

	def __init__(self):
		self.name = "Fernando 2.0"

	#Receive Hand
	def establish_hand(self,d1, d2, d3, d4, d5, d6,d7):
		self.domino_hand = {d1,d2,d3,d4,d5,d6,d7};

	#Representation of a Hand
	def get_hand(self):
		hand_string = ""
		for i in self.domino_hand:
			hand_string += i.getTileString() + ","
		return hand_string