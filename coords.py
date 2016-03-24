'''
Gridding functions

These work mainly for projected coordinate systems

Chris 17/03/15
'''

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def corners(top_left_x, top_left_y, post, cols, rows):
	'''
	Calculates corner coordinates based on the known top left corner, cell size and known image dimensions

	Returns four tuples:

	Top left x,y
	Top right x,y
	Bottom right x,y
	Bottom left x,y
	'''

	tl_x = top_left_x
	tl_y = top_left_y
	tr_x = tl_x+(cols*post)
	tr_y = tl_y
	
	br_x = tr_x
	br_y = tl_y-(rows*post)
	bl_x = tl_x
	bl_y = br_y

	print "tl_northing = %f : tl_easting = %f" %(tl_y, tl_x)
	print "br_northing = %f : br_easting = %f" %(br_y, br_x)
	print "bl_northing = %f : bl_easting = %f" %(bl_y, bl_x)
	print "tr_northing = %f : tr_easting = %f" %(tr_y, tr_x)

	return [tl_x, tl_y], [tr_x, tr_y],[br_x, br_y],[bl_x, bl_y]


def grid_extent_labels(data, tl_x, tl_y, post, cols, rows, x_interval=200000,y_interval=400000):
	'''
	For use with matplotlib.pyplot.imshow

	Calculates the tick labels in x and y for an image based on known corner positions of a given projected reference system

	Also uses:
	coords.corners()

	Input notes:
	data - this is your grid array

	Returns:

	Tuples of [xtick_interval, xtick_labels] and [ytick_interval, ytick_labels]
	
	These can then be unpacked and used like:

	e.g.
	plt.xticks(xtick_interval, xtick_labels)
	plt.yticks(ytick_interval, ytick_labels)
	'''

	tl,tr,br,bl = coords.corners(tl_x, tl_y, post, cols, rows)
	br_x,br_y=br

	y,x=data.shape

	xtick_labels = np.arange(tl_x,br_x, x_interval)
	ytick_labels = np.arange(br_y, tl_y, y_interval)

	tick_num_x=(br_x-tl_x)/x_interval
	tick_num_y=(tl_y-br_y)/y_interval

	xtick_interval = np.arange(0, x, x/tick_num_x) # tick_num changes how many ticks you want...
	ytick_interval = np.arange(0, y, y/tick_num_y) # tick_num changes how many ticks you want...

	return [xtick_interval, xtick_labels],[ytick_interval, ytick_labels]