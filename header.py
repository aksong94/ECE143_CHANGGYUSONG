from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy.random as random
import random as regular_random

colors = ['red','green','grey','blue','black','yellow','aliceblue',
		'plum','crimson','pink','indigo','khaki','salmon']
clear = [0.1,0.2,0.3,0.4,0.5]
'''
colors = candidate colors of rectangle
clear = level of transparent to distinguish rectangle more effectively
'''

class tower:
	"""
	Class tower
	=> tower that contains width, height and positions
	tower(width, height, pos_x, pos_y)

	Functions in this class:
	integer_corners() => returns each corner
	deif() => returns definition of itself
	dots() => returns every dots that has itself
	tile() => returns every tile of itself

	width : width of the rectangle
	height : height of the rectnagle
	pos_x : x point of starting position
	pos_y : y point of starting position 
	"""

	def __init__(self, width, height, pos_x, pos_y):
		self.width = width
		self.height = height
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.pos_start = (pos_x, pos_y)
	'''
	>>> rect = tower(4,4,1,1)
	'''

	def integer_corners(self):
		self.lb = self.pos_start
		self.lt = (self.pos_x, self.pos_y + self.height)
		self.rb = (self.pos_x + self.width, self.pos_y)
		self.rt = (self.pos_x + self.width, self.pos_y + self.height)
		return [self.lb, self.lt, self.rb, self.rt]
	'''
	Function integer_corners
	=> returns position of each corners
		each points should be integer

	lb : left bottoms
	lt : left top
	rb : right bottom
	rt : right top
	
	return value : [lb, lt, rb, rt]

	>>> rect.integer_corners()
	'''

	def defi(self):
		return [self.width, self.height, self.pos_x, self.pos_y]

	'''
	Function defi
	=> returns definition of itself

	return value
	: [width, height, x points of starting position, y points of starting position]

	>>> rect.defi()
	'''

	def dots(self):
		dots = []
		for i in range(self.pos_x,self.pos_x+self.width+1):
			for j in range(self.pos_y,self.pos_y+self.height+1):
				dots.append((i,j))
		return dots

	'''
	Function dots
	=> returns every dots that rectangle contains itself

	>>> rect.dots()
	'''

	def tile(self):
		tile = {}
		for i in range(self.pos_x,self.pos_x + self.width):
			for j in range(self.pos_y,self.pos_y + self.height):
				tile[(i,j),(i+1,j+1)] = 1
		return tile

	'''
	Function tile
	=> returns every tiles that rectangle has itself

	return dictionary : tile[(x,y),(x+1,y+1)] = size of area

	About tile
	=> Since its integer base, i came up with the 'tile' concept
	Tile represents 1 by 1 square. It doesn't have all the corners of it but 
	has a key of left down corner and right upper corner and 
	value itself has a size of area which is, of course, 1.

	>>> rect.tile()
	'''

def full_coverage(footprint):
	
	result = [a.width * a.height for a in footprint]
	return sum(result)

	'''
	Function full_coverage
	=> returns the size of area that has been covered

	input 'footprint' : footprint that contains history of communication towers
	return 'value' : size of area that has been covered

	>>> area = full_coverage(footprint)
	'''

def is_overlap(footprint, ins_tower):
	
	ins_tile = ins_tower.tile().keys()
	for i in footprint:
		over_tile = i.tile().keys()
		for j in ins_tile:
			for k in over_tile:
				if j == k:
					return True
	return False

	'''
	Function 'is_overlap'
	=> function that determine it is overlapped or not.

	input 'ins_tower' : candidates of tower
	input 'footprint' : footprint that contains history of communication towers
	
	return : True or False

	>>> is_overlap(footprint, tower(4,4,1,1))
	'''

def reshape(footprint, ins_tower):
	
	ins_tile = ins_tower.tile().keys()
	for i in footprint:
		over_tile = i.tile().keys()
		for j in over_tile:
			if j in ins_tile:
				ins_tile.remove(j)
	if len(ins_tile) == 0:
		return 0
	"""
	Simply remove the tile if it is already existed.
	"""

	start_pos = []
	result = {}
	for i in ins_tile:
		start_pos.append(i[0])
	"""
	gathering only starting point to reduce using spaces.
	starting position let us know 
	if 1 by 1 square starting from that point is valid.
	"""		
	for i in start_pos:
		width, height = 1, 1
		while True:
			if (i[0] + width,i[1]) in start_pos:
				width = width + 1
			else:
				break
		count = len(range(i[0],width+i[0]))
		while True:
			isit = [1 for j in range(i[0],width+i[0]) if (j,i[1]+height) in start_pos]
			if sum(isit) == count:
				height = height + 1
			else:
				break
		result[width*height] = (width,height,i[0],i[1])
	"""
	for every starting point that now exist,
	from that point, it goes right first to find the longest width
	and going up to find the longest height with the same width
	"""
	for i in start_pos:
		width, height = 1, 1
		while True:
			if (i[0],i[1]+height) in start_pos:
				height = height + 1
			else:
				break
		count = len(range(i[1],height+i[1]))
		while True:
			isit = [1 for j in range(i[1],height+i[1]) if (i[0]+width,j) in start_pos]
			if sum(isit) == count:
				width = width + 1
			else:
				break
		result[width*height] = (width,height,i[0],i[1])
	"""
	for every starting point that now exist,
	from that point, it goes up first to find the longest height
	and going right to find the longest width with the same height
	"""
	a = result[max(result)]
	return tower(a[0],a[1],a[2],a[3])

	'''
	Function reshape
	=> trim all the overlapped areas and returns biggest rectangle.
	
	input 'ins_tower' : candidates of tower
	input 'footprint' : footprint that contains history of communication towers
	return value : new tower with the biggest rectangle after being trimmed.

	>>> footprint, rectangle = reshape(footprint, tower(3,3,1,1))
	'''

def defi_tower(t_width, t_height):

	width = random.random_integers(1,t_width)
	height = random.random_integers(1,t_height)
	pos_x = random.random_integers(0,t_width - width)
	pos_y = random.random_integers(0,t_height - height)
	return tower(width, height, pos_x, pos_y)
	'''
	Function defi_tower
	=> function that make a new tower with given width and height.

	input 't_width' : width of desired area.
	input 't_height' : height of desired area.
	return value : new tower with random integers.

	>>> defi_tower(10,10)
	'''

def online(footprint, ins_tower):
	
	if is_overlap(footprint, ins_tower) == True:
		ins_tower = reshape(footprint, ins_tower)
		if ins_tower != 0 and ins_tower.width>0 and ins_tower.height>0:
			footprint.append(ins_tower)
			return footprint, ins_tower
		else:
			return footprint, None
	elif is_overlap(footprint, ins_tower) == False:
		footprint.append(ins_tower)
		return footprint, ins_tower

	'''
	Function online
	=> This is the main function of this problem.
	once the tower comes in, it checks if the tower is overlapped or not.
	and after all the process(checking, trimming), 
	it saves history of towers in footprint.
	But it rejects if the tower's width or height is lower than 1, becuase it is not an rectangle.

	input 'ins_tower' : candidate tower that might be online
	input 'footprint' : footprint that contains history of communication towers
	
	>>> footprint, rect = online(footprint, tower(3,3,1,1))
	'''

def plotting(width, height, x_count=1,y_count=1):
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(x_count,y_count,1)
	ax1.set_xlim([0,width])
	ax1.set_ylim([0,height])
	return fig1, ax1

	'''
	Function plotting
	=> returns a figure and axis of a plot.

	input 'width' : width of desired area.
	input 'height' : height of desired area.
	input 'x_count' : number of rows
	input 'y_count' : number of columns

	>>> fig, ax = plotting(10, 10)
	>>> fig, ax = plotting(10, 10, x_count = 2, y_count = 2)
	'''
