""" Final Project
Satchel Hamilton
December 13, 2020 """

from tkinter import *
from random import choice
import time

global ai
global human

ai = 'o'
human = 'x'

class Connect4(object):
	""" Major class to contain overall game logic
	and relating methods. """

	def __init__(self, window=None):
		self.data = []
		self.height = 6
		self.width = 7

		for row in range(self.height):
			boardRow = []
			for col in range(self.width):
				boardRow += [' ']
			self.data += [boardRow]

		self.window = window
		self.Bheight = 600
		self.Bwidth = 600
		self.padding = 5
		self.footer = 50
		self.diamX = (self.Bwidth/self.width)- self.padding
		self.diamY = (self.Bheight/self.width)- self.padding

		self.frame = Frame(self.window)
		self.frame.pack()

		self.qButton = Button(self.frame, 
			text="Quit", 
			command=self.qButtonAction)
		self.qButton.pack(side=LEFT)

		self.draw = Canvas(self.window, 
			width=self.Bwidth+self.padding, 
			height=self.Bheight+self.padding+ self.footer)
		self.draw.bind('<Button-1>', self.mouse)
		self.draw.pack(side=TOP)

		self.nButton = Button(self.window, 
			text="New Game", 
			command=self.nButtonAction)
		self.nButton.pack()

		self.circles = []
		self.colors = []
		y = self.padding

		for row in range(self.height):
			circleRow = []
			colorRow = []
			x = self.padding
			for col in range(self.width):
				circleRow += [self.draw.create_oval(x, y, 
					x+self.diamX, y+self.diamY, 
					fill='pale green')]
				colorRow += ['pale green']
				x += self.diamX + self.padding
			self.circles += [circleRow]
			self.colors += [colorRow]
			y += self.diamY + self.padding

		self.message = self.draw.create_text(50, 
			self.Bheight,
			text="""Welcome! Let's Play!""",
			anchor="w", font="Courier 20")

		self.horizontal = Scale(self.window, from_=1,to=7, orient=HORIZONTAL, command=self.slider)
		self.horizontal.pack()
	"""Constructor method to create frontend GUI object.
	All code contained is executed at the time an object
	of the Connect4 class is instantiated. Utilizes tkinter package
	to create all GUI elements."""

	def __repr__(self):
		s = ''
		for row in range(self.height):
			s+= '|'
			for col in range(self.width):
				s += self.data[row][col] + '|'
			s += '\n'

		s += '--'*self.width + '-\n'

		for col in range(self.width):
			s+= ' ' + str((col % 10) + 1)
		s += '\n'
		return s
	""" Method creates and returns printable representational
	string of object (backend ascii board). """

	def mouse(self, event):
		print(event.x, event.y)
		print(int(event.x/self.diamX), 
			int(event.y/self.diamY))
		col = int(event.x/self.diamX)
		if self.gameOver() == False:
			if self.allowsMove(col):
				row = self.checkRow(col)
				self.addMove(col, human)
				self.draw.itemconfig(self.circles[row][col], fill='royal blue')
				self.window.update()
				message = "You clicked %d,%d." % (row, col)
				self.draw.itemconfig(self.message, text=message)
				col = self.aiPlayer.nextMove(self)
				row = self.checkRow(col)
				if not self.winsFor(human):
					self.addMove(col, ai)
					self.draw.itemconfig(self.circles[row][col], fill='firebrick1')
				print(self)
			else:
				message = 'Please pick a valid column'
				self.draw.itemconfig(self.message, text=message)

			if self.winsFor(human):
				message = 'You Won! Huzzah!'
				self.draw.itemconfig(self.message, text=message)
				self.gameOver = True

			elif self.winsFor(ai) and not self.winsFor(human):
				message = 'You Lost!'
				self.draw.itemconfig(self.message, text=message)
				self.gameOver = True
				
			if self.isFull():
				message = """Cat's Game!"""
				self.draw.itemconfig(self.message, text=message)
				self.gameOver = True
	""" Method intercepts mouse events from user
	and translates them into coordinate points
	that can be interpreted by the backend logic. """

	def playGUI(self, aiPlayer):
		self.aiPlayer = aiPlayer
	""" Method allows a player object to interface with
	board object. """

	def slider(self, value):
		self.aiPlayer.ply = self.horizontal.get()
	""" Method sets the ply level inside of the player
	object to intercept and retain values from the slider GUI
	element (scale) as it is modified by user. """

	def qButtonAction(self):
		self.window.destroy()
	""" Method sets command for the "Quit" button
	GUI element, allowing user to terminiate program. """

	def nButtonAction(self):
		self.window.destroy()
		exec(open("./final.py").read())
	""" Method sets command for the "New Game" button
	GUI element, allowing user to restart program. """

	def checkRow(self, col):
		for row in range(self.height):
			if self.data[self.height-row-1][col] == ' ':
				return self.height-row-1
			else:
				row -= 1
	""" Method checks if the cell of a particular row is full
	and assigns column value to the first open cell, therby
	ensuring that pieces are only placed directly "on top" of 
	current pieces. """	

	def allowsMove(self, col):
		if col >= 0 and col < self.width:
			return self.data[0][col] == ' '
		else:
			return False
	""" Method to check if a move is valid,
	i.e. if the column is not already full. """

	def addMove(self, col, ox):
		if self.allowsMove(col):
			for row in range(self.height):
				if self.data[row][col] != ' ':
					self.data[row-1][col] = ox
					return True
			self.data[self.height-1][col] = ox
			return True
		else:
			return False
	""" Method allows for an empty cell in the backend board 
	representation to be replaced by a character (str) representation
	of a player board piece (x or o). """

	def delMove(self, col):
		for row in range(self.height):
			if self.data[row][col] != ' ':
				self.data[row][col] = ' '
				return
		self.data[row][col] == ' '
	""" Method deletes move after it has been made.
	Crucial for AI to create permutations on board state,
	therby allowing look-ahead functionality. """

	def isFull(self):
		for row in range(self.height):
			for col in range(self.width):
				if self.data[row][col] == ' ':
					return False
		return True
	""" Method looks at backend board state to determine
	if the board is full."""

	def isEmpty(self):
		for row in range(self.height):
			for col in range(self.width):
				if self.data[row][col] != ' ':
					return False
		return True
	""" Method looks at backend board state to determine
	if the board is entirely empty."""

	def winsFor(self, ox):
		for row in range(self.height):
			for col in range(self.width - 3):
				if self.data[row][col] == ox and \
					self.data[row][col+1] == ox and \
					self.data[row][col+2] == ox and \
					self.data[row][col+3] == ox:
						return True

		for row in range(self.height - 3):
			for col in range(self.width):
				if self.data[row][col] == ox and \
					self.data[row+1][col] == ox and \
					self.data[row+2][col] == ox and \
					self.data[row+3][col] == ox:
						return True

		for row in range(self.height - 3):
			for col in range(self.width - 3):
				if self.data[row][col] == ox and \
					self.data[row+1][col+1] == ox and \
					self.data[row+2][col+2] == ox and \
					self.data[row+3][col+3] == ox:
						return True

		for row in range(3, self.height):
			for col in range(self.width - 3):
				if self.data[row][col] == ox and \
					self.data[row-1][col+1] == ox and \
					self.data[row-2][col+2] == ox and \
					self.data[row-3][col+3] == ox:
						return True
		return False
	""" Method looks at data object to determine if win-state
	has been reached either vertically, horizontally, or diagonally."""

	def clear(self):
		while not self.isEmpty():
			for row in range(self.height):
				for col in range(self.width):
					if self.data[row][col] != ' ':
						self.data[row][col] = ' '
	""" Method to clear backend board object by replacing
		 any value other than a space with a space. """

	def gameOver(self):
		return False
	""" Simple bool method to determine if win state or 
	gamer-over state has been reached. Used to stop user from
	making moves once game is over. """

	def playGameWith(self, aiPlayer):
		self.aiPlayer = aiPlayer
		currentPlayer = ai
		while self.winsFor(currentPlayer) == False and self.isFull() == False:
			oMove = aiPlayer.nextMove(self)
			print(self)
			print("Please pick a column.")
			if currentPlayer == ai:
				currentPlayer = human
				columnChoice = int(input())-1
				if not self.allowsMove(columnChoice):
					print("\nPlease pick a valid column.\n")
					columnChoice = int(input())-1
			elif currentPlayer == human:
				currentPlayer = ai
				time.sleep(0.5)
				columnChoice = oMove
			self.addMove(columnChoice, currentPlayer)

		if not self.isFull():
			print(self, "Player " + currentPlayer + " wins!")
		else:
			print("Cat's Game!")
	""" Unused method left from previous ascii game iteration. 
	Allowed for player object to interface with board object, containing 
	logic for switching players and other events. Precursor to logic used
	elsewhere in program. """

class Player():
	""" Player class contains methods that determine AI logic in regards
	to rating and choosing moves, and allows player objects to be instantiated. """

	def __init__(self, b, ox, tbt, ply):
		self.ox = ox
		self.tbt = tbt
		self.b = b
		self.ply = ply
	""" Method used to instantiate current instance of class, 
	and initialize and access variables that belong to the class. """
		
	def scoreBoard(self, b):
		scores = []
		bestMove = 0

		if self.b.winsFor(ai) == False:
			for col in range(self.b.width):
				self.b.addMove(col, ai)

				if self.b.allowsMove(col) == False:
					scores += [-1]
				if self.b.winsFor(human):
					scores += [100]
				if self.b.winsFor(ai):
					scores += [0]
				else:
					scores += [50]
			return scores
	""" Unused method that utlizes zero-lookahead
	logic to rate winnability of board state. Implemented
	in previous iterations. Precursor to scoresFor method. """

	def scoresFor(self, b, ox, ply):
		scores = []
		for col in range(self.b.width):
			if b.allowsMove(col):
				b.addMove(col, ox)
				if b.winsFor(ox):
					scores +=[500]
				else:
					if ply > 1:
						if ox == ai:
							switchPlayer = human
						else:
							switchPlayer = ai
						bestMove = max(self.scoresFor(b, switchPlayer, ply-1))
						scores +=[500 - bestMove]
					else:
						scores +=[50]
				b.delMove(col)
			else:
				scores +=[-1]
		return scores
	""" Method creates rules for AI logic to function.
	Works by making valid moves, checking for win state,
	rating and deleting moves, then switching the player
	variable and doing the same for the opponenet. """

	def nextMove(self, b):
		scores = self.scoresFor(b, self.ox, self.ply)
		move = self.tiebreakMove(scores)
		return move
	""" In-between method that initiallizes variables
	to contain values passed by scoresFor method and allows
	them to be evaluated by the tiebreakMove method. """

	def tiebreakMove(self, scores):
		bestMoves = max(scores)
		moveChoice = []

		for i in range(len(scores)):
			if scores[i] == bestMoves:
				moveChoice.append(i)

		if self.tbt == 'Left':
			return moveChoice[0]
		if self.tbt == 'Right':
			return moveChoice[-1]
		if self.tbt == 'Random':
			return choice(moveChoice)
	""" Method used to make a selection from a list of equivalently
	rated moves by selecting the value contained in either
	the first, last, or a random index. """

def main():
	root = Tk()
	root.title("Connect4")
	b = Connect4(root)
	p = Player(b, 'o', 'Left', 0)
	b.playGUI(p)
	root.mainloop()

if __name__ == '__main__': 
    main()