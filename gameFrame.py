import pygame
import gTools
import pFind

def DisplayCell(node, tileSize, border):
	pygame.draw.rect(screen, node.color, (node.x*tileSize, node.y*tileSize, tileSize-border, tileSize-border))

def GetGridMousePos(tileSize):
	(mouseX, mouseY) = pygame.mouse.get_pos()
	(x, y) = (int(mouseX/tileSize),int(mouseY/tileSize)) #mousepos on tilegrid
	return (x,y)

def Drag(node, grid, color,  x,y):
	if node != None:
		node.color = node.defaultColor
	node = grid[x][y]
	node.color = color
	return node

def LeftClick(startNode, goalNode, grid, x,y):
	activeMode = None
	if startNode == None:
		startNode = grid[x][y]
		startNode.color = (50,255,50)
	elif goalNode == None:
		goalNode = grid[x][y]
		goalNode.color = (255,50,50)
	elif grid[x][y] == startNode:
		activeMode = "dragStart"
		dragNode = startNode
	elif grid[x][y] == goalNode:
		activeMode = "dragGoal"
		dragNode = goalNode
	elif grid[x][y].closed == False:
		activeMode = "paintWall"
	elif grid[x][y].closed == True:
		activeMode = "paintOpen"
	return (activeMode, startNode, goalNode)

def RightClick(currentSelection,grid,x,y):
	if currentSelection != None:
		currentSelection.HideNeighbours()
	currentSelection = grid[x][y]
	currentSelection.DisplayNeighbours()
	return currentSelection




width = 800
height = 800
screen = pygame.display.set_mode((width,height))



def Main():

	backgroundColor = (155,155,155)
	
	tileAmount = 10
	tileSize = int(width/tileAmount)
	border = max(1, int(tileSize/15))
	mapi = gTools.Grid(tileAmount)
	mapi.CreateGrid()

	currentSelection = None
	startNode = None
	goalNode = None
	dragNode = None
	
	activeMode = None

	

	running = True
	while running:
		screen.fill(backgroundColor)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:    
				key = pygame.key.get_pressed()
				if key[pygame.K_RETURN]:
					if goalNode != None and startNode != None:
						mapi.CalculateAllH(goalNode)
						astar = pFind.pathFinder(startNode, goalNode)
						path = astar.JumpFind()
						#path = astar.AstarFind()
					else:
						print "Missing start or goal."
			if event.type == pygame.MOUSEBUTTONDOWN:
				(b1,b2,b3) = pygame.mouse.get_pressed()         
				(x,y) = GetGridMousePos(tileSize)
				
				if b1:
					(activeMode,startNode,goalNode) = LeftClick(startNode, goalNode, mapi.grid, x,y)

				if b3:
					currentSelection = RightClick(currentSelection,mapi.grid, x,y)
		
		if event.type == pygame.MOUSEBUTTONUP:
			(b1,b2,b3) = pygame.mouse.get_pressed()
			if b1 == False:
				activeMode = None

		if activeMode != None:
			(x,y) = GetGridMousePos(tileSize)
			if activeMode == "paintWall":
				if mapi.grid[x][y].closed == False:
					mapi.grid[x][y].CloseNode()
			elif activeMode == "paintOpen":
				if mapi.grid[x][y].closed == True:
					mapi.grid[x][y].OpenNode(mapi)
			elif activeMode == "dragStart":
				startNode = Drag(startNode, mapi.grid, (59,255,50), x,y)
			elif activeMode == "dragGoal":
				goalNode = Drag(goalNode, mapi.grid, (255,50,50), x,y)

		for x in range(0,tileAmount):
			for y in range(0, tileAmount):          
				DisplayCell(mapi.grid[x][y], tileSize, border)
		pygame.display.flip()

Main()

