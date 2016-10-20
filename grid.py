"""
Various gridding functions - creating meshes etc.

Attempts to minimize confusion/mis-calculation with regard to grid dimensions set based on cell corner coordinates or cell centre coordinates.

TESTING: test_grid.py
"""

__author__ = "Chris Wiliams"
__email__ = "chris.neil.wills@gmail.com"
__date__ = "19th October 2016"
__version__ = "1.0"

import sys
import numpy as np

print("Grid Version: 1.3 imported")

class grid:
	"""
	Various features extending from input grid dimensions.

	Requires user to input corner x and y coordinates and x and y dimensions
	
	Coordinates are set as the OUTERMOST LEFT CORNER 
		i.e. lower_left = coordinate is the lower left corner of the pixel
		i.e. top_left = coordinate is the top left corner of the pixel

	# lower_left example:

	ll_x=-800000.
	ll_y=-3400000.
	nx=301.
	ny=501.
	px_size=500.
	a=grid(ll_x, ll_y, nx, ny, px_size, corner='lower_left')
	"""

	def __init__(self, x, y, nx, ny, pixelWidth, corner='top_left'):
		"""
		corner: which corner are your x and y? top_left (default), lower_left? 
		"""
		
		if corner=='top_left' or corner =='lower_left':
			self.corner=corner
		else:
			print("corner must be set to either 'top_left' or 'lower_left'")
			raise RuntimeError

		if corner=='lower_left':
			self.bl_x=x # corner_y
			self.bl_y=y # corner_x
		elif corner =='top_left':
			self.tl_x=x # corner_y
			self.tl_y=y # corner_x

		self.nx=nx
		self.ny=ny
		self.pixelWidth=pixelWidth
	
	def cell_corner_mesh(self):
		"""
		XY mesh where each cell value pertains to the lower left cell corner coordinate

		e.g. x cell value =  lower left cell coordinate

		RETURNS

		x coordinate mesh
		y coordinate mesh
		"""

		print("Running cell corner mesh function")

		if self.corner=='lower_left':
			tr_x=self.bl_x+(self.pixelWidth*(self.nx+1)) # +1 as grid will be of lower left corners
			tr_y=self.bl_y+(self.pixelWidth*(self.ny+1)) # +1 as grid will be of lower left corners
			
			x=np.arange(self.bl_x,tr_x,self.pixelWidth)
			y=np.arange(self.bl_y,tr_y,self.pixelWidth)

		elif  self.corner=='top_left':
			tr_x=self.tl_x+(self.pixelWidth*(self.nx+1)) # +1 as grid will be of lower left corners
			br_y=self.tl_y-(self.pixelWidth*(self.ny+1)) # +1 as grid will be of lower left corners
			
			x=np.arange(self.tl_x,tr_x,self.pixelWidth)
			y=np.arange(br_y,self.tl_y,self.pixelWidth)
		
		xv, yv = np.meshgrid(x, y)

		return xv[::-1], yv[::-1]

	def cell_centre_mesh(self):
		"""
		XY mesh where each cell value pertains to the centre cell corner coordinate

		e.g. x cell value =  lower left x cell coordinate + (pixelWidth/2)

		RETURNS

		x coordinate mesh
		y coordinate mesh
		"""

		print("Running cell centre mesh function")

		if self.corner=='lower_left':

			bl_xc=self.bl_x+(self.pixelWidth/2)
			bl_yc=self.bl_y+(self.pixelWidth/2)
			
			tr_xc=bl_xc+(self.pixelWidth*(self.nx))
			tr_yc=bl_yc+(self.pixelWidth*(self.ny))
			
			x=np.arange(bl_xc,tr_xc,self.pixelWidth)
			y=np.arange(bl_yc,tr_yc,self.pixelWidth)
		
		elif self.corner=='top_left':

			tl_xc=self.tl_x+(self.pixelWidth/2) 
			tl_yc=self.tl_y-(self.pixelWidth/2)

			tr_xc=tl_xc+(self.pixelWidth*(self.nx))
			bl_yc=tl_yc-(self.pixelWidth*(self.ny)) 

			x=np.arange(tl_xc,tr_xc,self.pixelWidth)
			y=np.arange(bl_yc,tl_yc,self.pixelWidth)

		xv, yv = np.meshgrid(x, y)

		return xv[::-1], yv[::-1]

