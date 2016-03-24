from __future__ import division

import os
import os.path

import numpy as np

def trim_constant_rows_cols(img):
	'''
	Removes any rows or columns of a constant value from a image array
	based on a standard deviation of 0
	'''	
	img_goodrows = img[np.std(img, 1) != 0, :]
	img_no_zeros = img_goodrows[:, np.std(img_goodrows, 0) != 0]
	return img_no_zeros

def check_output_dir(filename):
	'''
	Checks if the designated directory name exists, creating it if it doesn't
	'''
	dirname = os.path.dirname(filename)
	if not os.path.isdir(dirname):	
		print "%s DOESN'T exist...\n" % dirname
		os.makedirs(dirname) 
		print "...but it does now"

def live_view_z(img):
	'''
	Enables display of z values in active matplotlib show() window
	Example	implementation:
		plt.imshow(np.log(image))
		plt.gca().format_coord = util.live_view_z(np.log(image))
		plt.show()
	See here for more info:
	http://matplotlib.org/examples/api/image_zcoord.html
	'''
	numrows,numcols = img.shape
	def format_coord(x,y):
		col = int(x+0.5)
		row = int(y+0.5)
		if col>=0 and col<numcols and row>=0 and row<numrows:
			z = img[row,col]
			return 'x=%1.4f, y=%1.4f, z=%5.5f'%(x,y,z)
		else:
			return  'x=%1.4f, y=%1.4f' %(x,y)
	return format_coord

def live_view_z_extent(img, extent):
	'''
	Same as live_view_z but works where extent is set in imshow
	Extent must be passed in as a tuple of xmin, xmax, ymin, ymax
	'''
	xmin, xmax, ymin, ymax = extent		
	def format_coord(x,y):
		col = int(x+0.5)
		row = int(y+0.5)
		if col>=ymin and col<ymax and row>=xmin and row<xmax:
			z = img[row,col]
			return 'x=%1.4f, y=%1.4f, z=%5.5f'%(x,y,z)
		else:
			return  'x=%1.4f, y=%1.4f' %(x,y)
	return format_coord
