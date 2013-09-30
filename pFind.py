openListColor = (100,100,255)
closedListColor = ( 100,255,100)

class pathFinder:
	def __init__(self, start, goal):
		self.startNode = start
		self.goalNode = goal
		self.openList = []
		self.closedList = []
		self.activeNode = start
		self.openList.append(self.activeNode)
		self.FoundPath = False
		self.path = []

	def AstarFind(self):
		while self.FoundPath != True:
			for node in self.activeNode.neighbours.values():
				if node not in  self.closedList:
					if node in self.openList:
						if node.g > self.activeNode.g + node.CalculateLocalG(self.activeNode.x, self.activeNode.y):
							node.parent = self.activeNode
							node.CalculateG
							node.CalculateF
					else:
						node.AddParent(self.activeNode)
						node.CalculateG(self.activeNode.x, self.activeNode.y, self.activeNode.g)
						node.CalculateF()
						self.openList.append(node)
						node.color = openListColor

			self.openList.remove(self.activeNode)
			self.closedList.append(self.activeNode)
			self.activeNode.color = closedListColor
			if len(self.openList) > 0:
				self.activeNode = self.FindLowestF()			
			
				if self.activeNode == self.goalNode:
					self.CreatePath()
					self.FoundPath = True
					return self.path
			else:
				print "no valid path found"
				return None
	def JumpFind(self,grid, tileAmount):
		jBool = None
		for x in range (self.activeNode.x+1, tileAmount):
			jBool = self.CheckJumpX(grid, x)
			if jBool:
				print True
				break
			elif jBool == False:
				print False
				break
		

	def CheckJumpX(self,grid, x):
		y =  self.activeNode.y
		if grid[x][y].closed:
			return False
		elif grid[x][y+1].closed:
			self.FNeighbourFound(grid,x,y)
			return True
		elif grid[x][y-1].closed:
			self.FNeighbourFound(grid, x,y)
			return True
		else:
			return None

	def FNeighbourFound(self, grid, x, y):
		grid[x][y].parent = self.activeNode
		grid[x][y].color = (0,0,255)
		self.openList.append(grid[x][y])


	def CreatePath(self):
		node = self.goalNode
		while node != None:
			self.path.append(node)
			node = node.parent

	def FindLowestF(self):
		self.openList.sort(key=lambda node: node.f, reverse=False)
		return self.openList[0]#BAJS
