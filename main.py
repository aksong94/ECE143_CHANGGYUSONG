from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from header import *
import numpy.random as random
import random as regular_random
import time

def main(t_width, t_height):
	assert isinstance(t_width, int)
	assert t_width>0
	assert isinstance(t_height, int)
	assert t_height>0
	"""
	t_width : width of desired coverage
	t_height : height of desired coverage
	"""

	plt.ion()
	"""
	Make plotting interactive
	"""
	fig1, ax1 = plotting(t_width, t_height)
	footprint = []

	plt.title('Desired total area of coverage: {pwidth}X{pheight}'.format
		(pwidth = t_width, pheight = t_height))
	plt.xlabel('Rect = [Width, Height, Start Position(x,y)]')
	plt.draw()
	plt.show()
	time.sleep(1)
	whole_count = 0
	square_count = 1
	"""
	title and xlabel will show the process right away
	"""

	while full_coverage(footprint) < t_width*t_height:

		rect = defi_tower(t_width, t_height)

		color_choice = regular_random.choice(colors)
		clear_choice = regular_random.choice(clear)
		"""
		choose color and transparent level randomly
		"""

		rect_patch = patches.Rectangle((rect.pos_x,rect.pos_y),rect.width,rect.height,
						alpha=clear_choice,fc=color_choice,hatch='/')
		plt.title('Tower[{pwidth}, {pheight}, ({ppos_x}, {ppos_y})] just comes in'.format
				(pwidth=rect.width, pheight=rect.height, ppos_x=rect.pos_x, ppos_y=rect.pos_y))

		ax1.add_patch(rect_patch)
		plt.draw()
		time.sleep(1)
		whole_count = whole_count + 1
		footprint, a = online(footprint, rect)
		"""
		This temporary graph(rect_patch) has to be removed if is has overlapping space.
		Thus, i declare as variable to remove easily
		"""

		if a==None:
			plt.title('Whole tower is overlapped')
			plt.draw()
			time.sleep(1)
			rect_patch.set_visible(False)
		else:
			if a == rect:
				plt.title('There are no towers that overlap')
				rect_patch.set_visible(False)
				ax1.add_patch(patches.Rectangle((a.pos_x,a.pos_y),a.width,a.height,
					alpha = clear_choice,fc=color_choice,linewidth=2))
				plt.text(a.pos_x+a.width/2,a.pos_y+a.height/2,'%d'%square_count,fontsize=15,ha='center')
				square_count = square_count + 1
				plt.draw()
				time.sleep(1)
			else:
				ax1.add_patch(patches.Rectangle((a.pos_x,a.pos_y),a.width,a.height,
					alpha = clear_choice,fc=color_choice, linewidth=2))
				plt.title('Tower[{pwidth}, {pheight}, ({x}, {y})] becomes online'.format
				(pwidth=a.width, pheight=a.height, x=a.pos_x, y=a.pos_y))
				plt.draw()
				time.sleep(1)
				rect_patch.set_visible(False)
				plt.text(a.pos_x+a.width/2,a.pos_y+a.height/2,'%d'%square_count,fontsize=15,ha='center')
				square_count = square_count + 1
				plt.draw()
				time.sleep(1)
	"""
	if : if the whole tower is overlapped, function online doesn't have any returning value.
		so i just remove the temporary graph.
	else :
		if : there is no overlapping space, so it is same as first
		else : trimmed and got biggest rectangle.
	"""
	plt.title('Whole tower is covered')

"""
Function main
=> shows plotting image of Network system.

>>> main(10, 10)
>>> main(20, 15)
"""


def q_1(width, height, n):
	assert isinstance(width, int)
	assert width > 0
	assert isinstance(height, int)
	assert height > 0
	assert isinstance(n, int)
	assert int > 0
	"""
	width : width of desired space
	height : height of desired space
	n : number of sequence
	"""

	fig1, ax1 = plotting(width, height)
	plt.ion()
	plt.show()

	plt.title('Desired total area of coverage: {pwidth}X{pheight}'.format
		(pwidth = width, pheight = height))

	count = 0
	rect_count = 0
	footprint = []
	"""
	count : count every towers
	rect_count : count valid towers
	footprint : saves history of rectangles
	"""
	while count < n:
		rect = defi_tower(width, height)
		color_choice = regular_random.choice(colors)
		clear_choice = regular_random.choice(clear)
		footprint, rect = online(footprint, rect)
		if rect != None:
			rect_count = rect_count + 1
			ax1.add_patch(patches.Rectangle((rect.pos_x,rect.pos_y),rect.width,rect.height,
			alpha = clear_choice,fc=color_choice, linewidth=1))
			plt.text(rect.pos_x+rect.width/2,rect.pos_y+rect.height/2,'%d'%rect_count,fontsize=10,ha='center')
		count = count + 1
	print("With given {n}-sequences of candidates,".format(n=n))
	print("{area} covered from {total} desired area".format(area = full_coverage(footprint),total = width*height))
	print("along with {tower} valid towers.".format(tower=rect_count))
	return full_coverage(footprint)
"""
Function q_1
=> returns size of area that has covered until n sequence comes in.
The while loop runs until 'n'th tower comes in.

return value: size of covered area

>>> q_1(10, 10, 10)
"""

def q_2(width, height):
	assert isinstance(width, int)
	assert width > 0
	assert height > 0
	assert isinstance(height, int)
	"""
	width : width of desired space
	height : height of desired space
	"""

	fig1, ax1 = plotting(width, height)
	plt.ion()
	count = 0
	rect_count = 0
	rect_dict = {}
	footprint = []
	"""
	count : count every towers
	rect_count : count valid towers
	rect_dict : dictionay that contains history of counts
				i.e. 'rect_count' towers were valid until 'count' tower comes in
				rect_dict[count] = rect_count
	footprint : saves every history of valid towers
	"""
	while full_coverage(footprint) < (width)*(height):
		rect = defi_tower(width, height)
		footprint, rect = online(footprint, rect)
		if rect != None:
			rect_count = rect_count + 1
		count = count + 1
		rect_dict[count] = rect_count

	n = random.random_integers(1,max(rect_dict))
	"""
	rect : tower with random integers
	n was picked after running ad-hoc system.
	"""
	for i in range(len(footprint)-1, rect_dict[n]-1, -1):
		footprint.pop(i)
	for i in range(len(footprint)):
		color_choice = regular_random.choice(colors)
		clear_choice = regular_random.choice(clear)
		ax1.add_patch(patches.Rectangle((footprint[i].pos_x,footprint[i].pos_y),footprint[i].width,footprint[i].height,
				alpha = clear_choice,fc=color_choice, linewidth=2))
		plt.text(footprint[i].pos_x+footprint[i].width/2,footprint[i].pos_y+footprint[i].height/2,'%d'%(i+1),fontsize=10,ha='center')	
	
	print('With randomly picked {n} number of input towers,'.format(n=n ))
	print('{tower} covered from {total} desired area'.format(tower=full_coverage(footprint),total=width*height))
	print('along with {ctower} valid towers'.format(ctower=rect_dict[n]))
	return full_coverage(footprint)
"""
Function q_2
=> returns size of area that has covered until randomly picked n-sequence comes in.
	i did the whole ad-hoc process first and picked n from that range.

>>> q_2(10, 10)
"""

def q_3(width, height, n=10):

	assert isinstance(width, int)
	assert width > 0
	assert isinstance(height, int)
	assert height > 0
	assert isinstance(n, int)
	assert n > 0
	"""
	width : width of desired space
	height : height of desired space
	n : number of sequence
	"""

	fig1 = plt.figure()
	plt.ion()
	plt.show()

	whole_count = 0
	overall_footprint = []
	overall_count = {}
	"""
	whole_count : count every towers
	overall_footprint : saves every processed ad-hoc system
	overall_count : contains number of valid towers on each system.
	"""
	for i in range(n):
		footprint = []
		rect_count = 0
		while full_coverage(footprint) < width*height:
			rect = defi_tower(width, height)
			footprint, rect = online(footprint, rect)
			whole_count = whole_count + 1
			if rect != None:
				rect_count = rect_count + 1
		overall_count[i] = rect_count
		overall_footprint.append(footprint)
	"""
	rect = new towers with random integer
	append footprint of every valid towers in overall_footprint
	"""
	count = 0
	for i in range(n):
		if overall_count[i] == min(overall_count.values()):
			ax1 = fig1.add_subplot(2,1,1)
			ax1.set_xlim([0,width])
			ax1.set_ylim([0,height])
			for j in overall_footprint[i]:
				count = count + 1
				color_choice = regular_random.choice(colors)
				clear_choice = regular_random.choice(clear)
				ax1.add_patch(patches.Rectangle((j.pos_x,j.pos_y),j.width,j.height,
					alpha = clear_choice,fc=color_choice, linewidth=2))
				plt.text(j.pos_x+j.width/2,j.pos_y+j.height/2,'%d'%(count),fontsize=10,ha='center')
				plt.title('Minimun number of valid towers')
			break
	"""
	plotting footprint that has minimum number of valid towers
	"""

	count = 0
	for i in range(n):
		if overall_count[i] == max(overall_count.values()):
			ax2 = fig1.add_subplot(2,1,2)
			ax2.set_xlim([0,width])
			ax2.set_ylim([0,height])
			for j in overall_footprint[i]:
				count = count + 1
				color_choice = regular_random.choice(colors)
				clear_choice = regular_random.choice(clear)
				ax2.add_patch(patches.Rectangle((j.pos_x,j.pos_y),j.width,j.height,
					alpha = clear_choice,fc=color_choice, linewidth=2))
				plt.text(j.pos_x+j.width/2,j.pos_y+j.height/2,'%d'%(count),fontsize=10,ha='center')
				plt.title('Maximum number of valid towers')
			break
	"""
	plotting footprint that has maximum number of valid towers
	"""
	
	print("In {pwidth}X{pheight} area, with {n} times excuted,".format(pwidth = width, pheight = height, n = n))
	print("The average amount of commnication tower candidates was {n}".format(n=whole_count/n))
	print("The average amount of Valid tower was {n}".format(n=sum(overall_count.values())/n))
	return whole_count/n

"""
Function q_3
=> returns average of towers require to fulfill the desired space

>>> q_3(10, 10)
"""

	