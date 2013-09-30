selColor = (255,0,0)

class Cell():
	def __init__(self,x,y):
		self.x = x
		self.y = y

		#Vis variables
		self.color = (255,255,255)
		self.defaultColor = self.color

		#Astar variables
		self.parent = None
		
		self.h = 0
		self.g = 0
		self.f = 0
		
		self.neighbours = {}
		self.closed = False

	def CalculateH(self, goal):
		self.h = (abs(self.x - goal.x) + abs(self.y - goal.y))*10

	def CalculateG(self, x, y, prevG):
		self.g = self.CalculateLocalG(x, y) + prevG

	def CalculateLocalG(self, x,y):
		self.localG = None
		if abs(self.x -x)+abs(self.y-y) > 1:
			self.localG = 14
		else:
			self.localG = 10
		return self.localG

	def CalculateF(self):
		self.f = self.g + self.h

	def AddParent(self, node):
		self.parent = node

	def AddNeighbour(self, nCell, dir1, dir2):
		if nCell not in self.neighbours:
			self.neighbours[dir1] = nCell
			nCell.neighbours[dir2] = self

			#self.neighbours.append(nCell)
			#nCell.AddNeighbour(self)

	def RemoveNeighbour(self, neighbour):
		for key, value in self.neighbours.items():
			if neighbour == value:
				del self.neighbours[key]

	def DisplayNeighbours(self):
		for cell in self.neighbours.values():
			cell.color = selColor

	def HideNeighbours(self):
		for cell in self.neighbours.values():
			cell.color = self.defaultColor

	def OpenNode(self, grid):
		self.closed = False
		grid.CheckNeighbours(self, self.x, self.y ,True)
		self.color = self.defaultColor

	def CloseNode(self):
		self.closed = True
		self.color = (155,155,155)
		#for node in self.neighbours.values():
		#	node.RemoveNeighbour(self)
		#self.neighbours = {}

class Grid():
	def __init__(self, tileAmount):
		self.tileAmount = tileAmount

	def CreateGrid(self):
		self.grid = [[0 for x in range(self.tileAmount)] for y in range(self.tileAmount)]
		for x in range (0, self.tileAmount):
			for y in range (0, self.tileAmount):
				newCell = Cell(x, y)
				self.CheckNeighbours(newCell, x, y)
				self.grid[x][y] = newCell
		return self.grid
	def CheckNeighbours(self, node, x, y, allDir = False):
		a = 1
		if y > 0 and self.IsValidNeighbour(x,y-a):
			node.AddNeighbour(self.grid[x][y-a], "n","s")

		if x > 0:
			if self.IsValidNeighbour(x-a,y):
				node.AddNeighbour(self.grid[x-a][y], "w","e")
			
			if y > 0 and self.IsValidNeighbour(x-a, y-a):
				node.AddNeighbour(self.grid[x-a][y-a], "nw", "se")
			
			if y < self.tileAmount-1 and self.IsValidNeighbour(x-a, y+a):
				node.AddNeighbour(self.grid[x-a][y+a], "sw", "ne")
		
		if allDir == True:
			self.RevCheckNeighbours(node, x, y)

	def RevCheckNeighbours(self, node, x, y):
		a = -1

		if y < self.tileAmount-1 and self.IsValidNeighbour(x,y-a):
			node.AddNeighbour(self.grid[x][y-a], "s" , "n")
		
		if x < self.tileAmount-1:
			if self.IsValidNeighbour(x-a,y):
				node.AddNeighbour(self.grid[x-a][y], "e","w")
			if y < self.tileAmount-1 and self.IsValidNeighbour(x-a, y-a):
				node.AddNeighbour(self.grid[x-a][y-a], "se","nw")
			if y > 0 and self.IsValidNeighbour(x-a, y+a):
				node.AddNeighbour(self.grid[x-a][y+a], "ne","sw")

	def CalculateAllH(self, goal):
		for x in range (0, self.tileAmount):
			for y in range (0, self.tileAmount):
				self.grid[x][y].CalculateH(goal)

	def IsValidNeighbour(self,x,y):
		if self.grid[x][y] != None and not self.grid[x][y].closed:
			return True
		else:
			return False
class Path:
	def __init__(self, path):
		self.path = path