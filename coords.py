'''
Various coordinate and gridding related functions

@author: Chris Williams
@date  : 17/03/15 onwards...
'''

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap.pyproj as pyproj

def warp_xyz(xyz, inprj, outprj):
	"""

	Changes coordinates of an input xyz dataset from those specified by inproj to outprj.

	VARIABLES

	xyz    - xyz columns
	inprj  - input projection (proj4 syntax / epsg code)
	outprj - output projection (proj4 syntax / epsg code)

	RETURNS

	xyz_out - numpy array of warped xyz values

	EXAMPLE
	
	#set paths
	path="O:/Documents/CHRIS_Bristol/Lamont_BATHYMETRY/new_data_2016"

	in_f="%s/IGBTH4_20150126_labelled.csv" %(path)
	out_f="%s/IGBTH4_20150126_bamber_XYZ.csv" %path
	#in_f="%s/IGBTH4_20141008_labelled.csv" %(path)
	#out_f="%s/IGBTH4_20141008_bamber_XYZ.csv" %path
	#in_f="%s/IGBTH4_20140207_labelled.csv" %(path)
	#out_f="%s/IGBTH4_20140207_bamber_XYZ.csv" %path

	#read in data
	data=np.genfromtxt(in_f, skiprows=1,delimiter=',')
	lon=data[:,3]
	lat=data[:,4]
	z=data[:,5]
	xyz=np.array((lon, lat, z)).transpose()

	#warp
	wgs84 = "+init=EPSG:4326" # LatLon with WGS84 datum 
	bamb  = "+proj=stere +lat_0=90 +lat_ts=71 +lon_0=-39 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs" # bamber polar stereo
	xyz_out, xyz_out_transp = warp_xyz(xyz, wgs84, bamb)

	# write data out
	np.savetxt(out_f, xyz_out_transp, delimiter=",", header="x_bamb, y_bamb, z", comments='')
	print("Coordinate transformation COMPLETE")
	print("Input was: %s" %(in_f))
	print("Outputs is: %s" %(out_f))

	"""

	inprj=pyproj.Proj(inprj)
	outprj=pyproj.Proj(outprj) 

	x_in = xyz[:,0]
	y_in = xyz[:,1]
	z    = xyz[:,2]

	x_out,y_out=pyproj.transform(inprj, outprj, x_in, y_in)

	xyz_out=np.array((x_out,y_out,z))
	xyz_out_transp=np.array((x_out,y_out,z)).transpose() # transposed

	return xyz_out, xyz_out_transp


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