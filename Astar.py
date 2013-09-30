class Astar:
	def __init__(self, start, goal):
		self.startNode = start
		self.goalNode = goal
		self.openList = []
		self.closedList = []
		self.activeNode = startNode
		self.openList.append(self.activeNode)
		self.FoundPath = False
		self.path = []

	def FindPath(self):
		while self.FoundPath != True:
			for node in self.activeNode.neighbours:
					if node in self.openList and node not in self.closedList:
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

	def CreatePath(self):
		node = self.goalNode
		while node != None:
			self.path.append(node)
			node = node.parent

	def FindLowestF(self):
		self.openList.sort(key=lambda node: node.f, reverse=False)
		return self.openList[0]