# The Coding train's p5.js A* program in Python

import sys
import random

cols = 10
rows = 10
grid = []

open_set = [] # a list of nodes that we HAVEN'T been to
closed_set = [] # a list of nodes that we HAVE been to
path = []

class Node():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.f = 0
		self.g = 0
		self.h = 0
		self.wall = False
		if random.randint(1,10) < 3:
			self.wall = True
		self.previous = None
		self.neighbours = []

	def addNeighbour(self,grid):
		x = self.x
		y = self.y
		# up down left right
		if x < cols - 1:
			self.neighbours.append(grid[x+1][y])
		if x > 0:
			self.neighbours.append(grid[x-1][y])
		if y < rows - 1:
			self.neighbours.append(grid[x][y+1])
		if y > 0:
			self.neighbours.append(grid[x][y-1])
		# diagonals
		if x < cols - 1 and y < rows - 1:
			self.neighbours.append(grid[x+1][y+1])
		if x > 0 and y > 0:
			self.neighbours.append(grid[x-1][y-1])
		if x < cols - 1 and y > 0:
			self.neighbours.append(grid[x+1][y-1])
		if x > 0 and y < rows - 1:
			self.neighbours.append(grid[x-1][y+1])

def heuristic(pos1,pos2):
	x_diff, y_diff = pos1.x-pos2.x, pos1.y-pos2.y
	return abs((x_diff*x_diff)*(y_diff*y_diff))

# def reverseRemove(array, item): # iterate backwards and remove item from an array
# 	for i in range(len(array), 0, -1):
# 		if array[i-1] == item:
# 			del array[i-1]
# 	return array

# create nodes
for c in range(cols):
	array = []
	for r in range(rows):
		array.append(Node(c,r))
	grid.append(array)

# find neighbour nodes
for c in range(cols):
	for r in range(rows):
		grid[c][r].addNeighbour(grid)

start = grid[0][0]
end = grid[cols-1][rows-1]

open_set.append(start)

while True:
	try:
		if len(open_set) > 0:
			lowest_index = 0 # set the optimal node to the node with lowest "f"
			for i in range(len(open_set)): # loop through nodes that have been calculated
				if open_set[i].f < open_set[lowest_index].f: # find the node with smallest f score
					lowest_index = i

			current = open_set[lowest_index] # move current node to the node with lowest f score

			if current == end: # end path finding if reached goal
				node = current
				path.append(node)
				while node.previous: # work backwards from the last node to find the full path
					path.append(node.previous)
					node = node.previous
				break

			open_set.remove(current)
			closed_set.append(current)

			for neighbour in current.neighbours:
				if neighbour not in closed_set and not neighbour.wall:
					tent_g = current.g+1 # g value of neighbour. Change +1 to +dist(current,neighbour) if the distance between nodes are different
					new_path = False
					if neighbour in open_set: # if this neighbour node has been calculated
						if tent_g < neighbour.g: #
							neighbour.g = tent_g
							new_path = True
					else: # if we come a cross a new neighbour node that hasn't been calculated
						neighbour.g = tent_g
						open_set.append(neighbour)
						new_path = True
					if new_path:
						neighbour.h = heuristic(neighbour, end) # find the heuristic
						neighbour.f = neighbour.g + neighbour.h # total score of neighbour node
						neighbour.previous = current # remember where this neighbour came from
		else:
			print("No Path")
			sys.exit(0)
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		sys.exit(0)

if path:
	print("Path found")
	for node in path:
		print(node.x,node.y)
	print(len(path))
# break loop and finish
