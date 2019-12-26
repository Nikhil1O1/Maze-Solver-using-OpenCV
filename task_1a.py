
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ 48XX ]
# Author List:		[ Names of team members worked on this file separated by Comma: Rajat Srivastava & Nikhil Choudhary]
# Filename:			task_1a.py
# Functions:		readImage, solveMaze, Link, findNeighbours, buildGraph, next_num, numberMaze, shortestNumberedPath
# 					[ Comma separated list of functions in this file ]
# Global variables:	CELL_SIZE, file_num, img_file_path
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20

class Link():
	value = 0
	parent = 0
	def __init__(self, a, b):
		self.value = a
		self.parent = b

file_num = 0
img_file_path = 'image file path here' + str(file_num) + '.jpg'


def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image

	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

	"""

	binary_img = None

	#############	Add your Code here	###############
	
	img=cv2.imread(img_file_path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,binary_img = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

	###################################################

	return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point

	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image

	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

	"""
	
	shortestPath = []

	#############	Add your Code here	###############

	height, width = original_binary_img.shape
	no_cells_height = (height//CELL_SIZE)
	no_cells_width = (width//CELL_SIZE)
	initial_point = (0, 0)
	final_point = ((no_cells_height-1),(no_cells_width-1))
	shortestPath=[initial_point]
	visited = [initial_point]
	count = 1
	global path
	path = []
	global new
	new = {}
	global l
	l = []
	graph = buildGraph(original_binary_img)
	
	for k in graph.keys():
	    new[k] = -1
	
	new[initial_point] = 1
	global x
	x = list(range(1,1000))		
	numberMaze(graph, initial_point, new, l)
	path.append(new[final_point])
	shortestNumberedPath(l, new[initial_point], new[final_point], path)
	path.reverse()
	current = initial_point
	while(True):
		if current == final_point:
			return shortestPath
		for j in graph[current]:
			if not tuple(j) in visited:
				if new[tuple(j)] == new[current]:
					current = tuple(j)
					shortestPath.append(current)
					visited.append(current)
					break
				else:
					if new[tuple(j)] == path[count]:
						count += 1
						shortestPath.append(tuple(j))
						current = tuple(j)
						visited.append(current)
						break

	###################################################
	
	return shortestPath


#############	You can add other helper functions here		#############

def findNeighbours(original_binary_img,row,column):
	neighbours = []
	#############  Add your Code here   ###############
	i = 0
	while(True):
		if original_binary_img[i, i] != 0:
			border = i 
			break
		i += 1
	i = border
	cell = 0
	while(True):
		if original_binary_img[i, i] == 0:
			cell = i 
			break
		i += 1
	if original_binary_img[cell - border * 2, cell] == 0 or original_binary_img[cell, cell - border * 2] == 0:
		cell = cell + border
	row_new = int((2 * row + 1) * (cell / 2))
	col_new = int((2 * column + 1) * (cell / 2))
	top = int(row_new - (cell / 2) + 1)
	bottom = int(row_new + (cell / 2) - 2)
	left = int(col_new - (cell / 2) + 1)
	right = int(col_new + (cell / 2) - 2)
	if original_binary_img[top, col_new] != 0:
		neighbours.append([row - 1, column])
	if original_binary_img[bottom, col_new] != 0:
		neighbours.append([row + 1, column])
	if original_binary_img[row_new, left] != 0:
		neighbours.append([row, column - 1])
	if original_binary_img[row_new, right] != 0:
		neighbours.append([row, column + 1])
	###################################################
	return neighbours


def buildGraph(original_binary_img):  ## You can pass your own arguments in this space.
	graph = {}
	#############  Add your Code here   ###############
	i = 0
	while(True):
		if  original_binary_img[i, i] != 0:
			border = i 
			break
		i += 1
	i = border
	cell = 0
	while(True):
		if  original_binary_img[i, i] == 0:
			cell = i 
			break
		i += 1
	if  original_binary_img[cell - border * 2, cell] == 0 or  original_binary_img[cell, cell - border * 2] == 0:
		cell = cell + border
	r = len( original_binary_img) // cell
	c = len( original_binary_img) // cell
	for i in range(r):
		for j in range(c):
			graph[(i, j)] = findNeighbours( original_binary_img, i, j)
	###################################################

	return graph


def next_num():
	x.pop(0)
	return x[0]

def numberMaze(graph, initial_point, new, l):         
	empty = 0
	for k in graph[initial_point]:
		if new[tuple(k)] == -1:
			empty += 1
	if empty == 0:
		return
	elif empty == 1:

		for i in range(len(graph[initial_point])):        
			if new[tuple(graph[initial_point][i])] == -1:
				new[tuple(graph[initial_point][i])] = new[initial_point]
				numberMaze(graph, tuple(graph[initial_point][i]), new, l) 
	
	else:
		for i in range(len(graph[initial_point])):
			if new[tuple(graph[initial_point][i])] == -1:
				n = next_num()
				new[tuple(graph[initial_point][i])] = n
				l.append(Link(n, new[initial_point]))
				numberMaze(graph, tuple(graph[initial_point][i]), new, l)
	

def shortestNumberedPath(l, initial_point, final_point, path):
 
	if final_point == initial_point:
		return
	else:
		for i in l:
			if i.value == final_point:
				parent = i.parent
				break
		path.append(parent)
		shortestNumberedPath(l, initial_point, parent, path)

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


