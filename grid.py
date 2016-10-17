import sys
import numpy as np
import matplotlib.pyplot as plt

pixelWidth=500.
nx=301.
ny=561.

bl_x=-800000
bl_y=-3400000
tr_x=bl_x+(pixelWidth*nx)
tr_y=bl_y+(pixelWidth*ny)

print("BL X: %d" %bl_x)
print("TR X: %d" %tr_x)
print("BL Y: %d" %bl_y)
print("TR Y: %d" %tr_y)


x=np.arange(bl_x,tr_x,pixelWidth)
y=np.arange(bl_y,tr_y,pixelWidth)
xxv, yyv = np.meshgrid(x, y)
fig, ax = plt.subplots(2)
ax[0].imshow(xxv)
ax[0].set_title("XXV")
ax[1].imshow(yyv)
ax[1].set_title("YYV")
plt.show()


class grid:
	"""
	Creates a meshgrid 

	Requires user to input bottom left x and y coordinates and x and y dimensions
	The bottom left coordinates are set as the BOTTOM LEFT CORNER
	"""

	def __init__(self, bl_x, bl_y, nx, ny, pixelWidth):
		self.__bl_x=bl_x
		self.__bl_y=bl_y
		self.__nx=nx
		self.__ny=ny

		self.x=np.arange(bl_x,tr_x,pixelWidth)
		self.y=np.arange(bl_y,tr_y,pixelWidth)
		self.xv, self.yv = np.meshgrid(x, y)


	@property
	def mesh(self):
		return self.xv, self.yv



