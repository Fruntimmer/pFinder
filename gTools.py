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
		self.neighbours = []
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

	def AddNeighbour(self, nCell):
		if nCell not in self.neighbours:
			self.neighbours.append(nCell)
			nCell.AddNeighbour(self)

	def RemoveNeighbour(self, neighbour):
		if neighbour in self.neighbours:
			self.neighbours.remove(neighbour)

	def DisplayNeighbours(self):
		for cell in self.neighbours:
			cell.color = selColor

	def HideNeighbours(self):
		for cell in self.neighbours:
			cell.color = self.defaultColor

	def OpenNode(self, grid):
		self.closed = False
		grid.CheckNeighbours(self, self.x, self.y ,True)
		self.color = self.defaultColor

	def CloseNode(self):
		self.closed = True
		self.color = (155,155,155)
		for node in self.neighbours:
			node.RemoveNeighbour(self)
		self.neighbours = []

class jCell(Cell):
	def __init__(self , x,y):
		self.N = None
		self.NE = None
		self.E = None
		self.SE = None
		self.S = None
		self.SW = None
		self.W = None
		self.NW = None
		Cell.__init__(self,x,y)


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
			node.AddNeighbour(self.grid[x][y-a])
		if x > 0:
			if self.IsValidNeighbour(x-a,y):
				node.AddNeighbour(self.grid[x-a][y])
			if y > 0 and self.IsValidNeighbour(x-a, y-a):
				node.AddNeighbour(self.grid[x-a][y-a])
			if y < self.tileAmount-1 and self.IsValidNeighbour(x-a, y+a):
				node.AddNeighbour(self.grid[x-a][y+a])
		if allDir == True:
			self.RevCheckNeighbours(node, x, y)
	def RevCheckNeighbours(self, node, x, y):
		a = -1

		if y < self.tileAmount-1 and self.IsValidNeighbour(x,y-a):
			node.AddNeighbour(self.grid[x][y-a])
		if x < self.tileAmount-1:
			if self.IsValidNeighbour(x-a,y):
				node.AddNeighbour(self.grid[x-a][y])
			if y < self.tileAmount-1 and self.IsValidNeighbour(x-a, y-a):
				node.AddNeighbour(self.grid[x-a][y-a])
			if y > 0 and self.IsValidNeighbour(x-a, y+a):
				node.AddNeighbour(self.grid[x-a][y+a])

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