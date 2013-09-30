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
				if node.closed:
					if node in self.openList:
						self.openList.remove(node)
					self.closedList.append(node)
				elif node not in  self.closedList:
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

	def JumpFind(self):
		activeNode = self.startNode
		jumpNode = self.activeNode
		if activeNode.parent == None:
			self.CheckQuadrant(activeNode, "nwe", "ens")
			
	def CheckQuadrant(self, jumpNode, vertDir, horDir):
		origin = jumpNode #Origin must be kept to reset the jump and as parent if forced neighbour is found
		foundForced = False
		for direction, fDir1, fDir2 in [vertDir, horDir]:
			jumpNode = origin #important for reset for the jump in other dir
			while jumpNode != None and not jumpNode.closed:
				for fDir in [fDir1, fDir2]:
					if jumpNode.neighbours.get(fDir) != None and jumpNode.neighbours[fDir].closed == True:
						foundForced = True
						self.FoundForced(jumpNode, origin, direction, fDir)
				jumpNode = self.Jump(jumpNode, direction)
		#If we didn't find a forced neighbour we will move one step diagonally and call the function again from that node
		if not foundForced and origin.neighbours.get(vertDir[0]+horDir[0]) != None:
			self.CheckQuadrant(origin.neighbours[vertDir[0]+horDir[0]], vertDir, horDir)


	def FoundForced(self, node, parent, direction, fDir):
		node.parent = parent
		self.AddToOpenList(node)
		if (direction == "n" or direction == "s") and node.neighbours.get(direction+fDir) != None:
			node.neighbours[direction+fDir].parent = node
			self.AddToOpenList(node.neighbours[direction+fDir])
		elif (direction == "w" or direction == "e") and node.neighbours.get(fDir + direction) != None:
			node.neighbours[fDir + direction].parent = node
			self.AddToOpenList(node.neighbours[fDir + direction])
		print "found forced neighbour"


	def Jump(self, node, direction):
		if node.neighbours.get(direction) != None:
			node = node.neighbours[direction]
			return node
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
		return self.openList[0]
	def AddToOpenList(self, node):
		if node not in self.openList:
			self.openList.append(node)
			node.color = (0,0,255)
