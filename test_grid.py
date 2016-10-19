import sys
import os
import grid

# test data
px=50 # pixel size
nx=6 
ny=10
ll_x=-800 # lower left x
ll_y=-800
tl_x=-800 # top left x
tl_y=-250 

# create grid object instances
ll=grid.grid(ll_x,ll_y,nx,ny,px,corner='lower_left')
tl=grid.grid(tl_x, tl_y, nx, ny, px, corner='top_left')


def test_tl_corner_mesh():

	tl_corner=tl.cell_corner_mesh()

	#tl_corner[0] = the x coordiante mesh
	#tl_corner[1] = the x coordiante mesh

	try:
		assert tl_corner[0].min() == ll_x
	except AssertionError:
		sys.exit("Corner mesh output incorrect")

	try:
		assert tl_corner[0].max() == (ll_x+(px*nx))
	except AssertionError:
		sys.exit("Corner mesh output incorrect")

	try:
		assert tl_corner[1].min() == ll_y
	except AssertionError:
		sys.exit("Corner mesh output incorrect")

	try:
		assert tl_corner[1].max() == (ll_y+(px*ny))
	except AssertionError:
		sys.exit("Corner mesh output incorrect")

def test_ll_corner_mesh():

	ll_corner=ll.cell_corner_mesh()

	#ll_corner[0] = the x coordiante mesh
	#ll_corner[1] = the x coordiante mesh
	
	try:
		assert ll_corner[0].min() == ll_x
	except AssertionError:
		sys.exit("Corner mesh output incorrect")
	
	try:
		assert ll_corner[0].max() == (ll_x+(px*nx))
	except AssertionError:
		sys.exit("Corner mesh output incorrect")
		
	try:
		assert ll_corner[1].min() == ll_y
	except AssertionError:
		sys.exit("Corner mesh output incorrect")
	
	try:
		assert ll_corner[1].max() == (ll_y+(px*ny))
	except AssertionError:
		sys.exit("Corner mesh output incorrect")