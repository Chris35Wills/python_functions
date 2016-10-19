import sys
import numpy as np

## An Example
#
#import grid
#import matplotlib.pyplot as plt
#
#ll_x=-800000.
#ll_y=-3400000.
#nx=300. # always 301 in idl as based on grid defined by ll corner
#ny=500. # always 501 in idl as based on grid defined by ll corner
#px_size=500.
#a=grid.grid(ll_x, ll_y, nx, ny, px_size)
#
#cx,cy=a.cell_centre_mesh()
#lx,ly=a.cell_corner_mesh()
#
#cx.shape
#lx.shape
#
#fig=plt.figure()
#ax1=fig.add_subplot(121)
#ax1.imshow(cx)
#ax1.set_title("X (centre)")
#ax2=fig.add_subplot(122)
#ax2.imshow(cy)
#ax2.set_title("Y (centre)")
#plt.show()
#
# remeber that index 0,0 is the top left corner for python BUT bottom left for IDL

print("Grid Version: 1.3 imported")

class grid:
	"""
	Creates a meshgrid 

	Requires user to input bottom left x and y coordinates and x and y dimensions
	The bottom left coordinates are set as the BOTTOM LEFT CORNER

	ll_x=-800000.
	ll_y=-3400000.
	nx=301.
	ny=501.
	px_size=500.
	a=grid(ll_x, ll_y, nx, ny, px_size)
	"""

	def __init__(self, bl_x, bl_y, nx, ny, pixelWidth):
		self.bl_x=bl_x
		self.bl_y=bl_y

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

		tr_x=self.bl_x+(self.pixelWidth*(self.nx+1)) # +1 as grid will be of lower left corners
		tr_y=self.bl_y+(self.pixelWidth*(self.ny+1)) # +1 as grid will be of lower left corners

		x=np.arange(self.bl_x,tr_x,self.pixelWidth)
		y=np.arange(self.bl_y,tr_y,self.pixelWidth)
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

		tr_x=self.bl_x+(self.pixelWidth*(self.nx))
		tr_y=self.bl_y+(self.pixelWidth*(self.ny))

		x=np.arange(self.bl_x+(self.pixelWidth/2.),tr_x+(self.pixelWidth/2.),self.pixelWidth)
		y=np.arange(self.bl_y+(self.pixelWidth/2.),tr_y+(self.pixelWidth/2.),self.pixelWidth)
		xv, yv = np.meshgrid(x, y)

		return xv[::-1], yv[::-1]
