"""
General methods to complement implementation of channel_mapper_expt.py 
including seed formatting, cooridnate transformations and raster I/Opens

@author: CWilliams
"""
import os
import pandas as pd
import numpy as np
from osgeo import gdal, osr
from osgeo.gdalconst import *
import matplotlib.pyplot as plt
from channel_mapper_expt import Path, ChannelObjective, Charge

def check_output_dir(filename):
	'''
	Checks if the designated directory name exists, creating it if it doesn't
	'''
	dirname = os.path.dirname(filename)
	if not os.path.isdir(dirname):	
		print "%s DOESN'T exist...\n" % dirname
		os.makedirs(dirname) 
		print "...but it does now"


def open_raster(raster_path):
    """
    Opens a tiff as specified by the user

    Returns a gdal dataset and an array of the raster
    """

    driver = gdal.GetDriverByName('Gtiff')
    driver.Register()
    dataset = gdal.Open(raster_path, GA_ReadOnly)
    data=dataset.ReadAsArray()
    print("Opened %s" %(raster_path))
    
    return (dataset, data)


def set_seeds(seeds_xyz, obj, Path):
	"""
	IMPORTANT: DOESN'T APPEND Z (ELEVATION) CURRENTLY - 23/02/16

	Takes in an nx3 ndarray of x,y,z values representing seeds and returns them in a format 
	to enable them to be cobvereted to Path objects as defined in channel_mapper_expt:

	[ Path(307,213,obj), 
	Path(271,606,obj), 
	Path(386,809,obj) ]

	VARIABLES:

	seeds_xyz : The input array to this function is created using npstereo_to_grid_xy().
	obj       : Imported from channel_mapper_expt
	Path      : Imported from channel_mapper_expt

	RETURNS:
	list of channel_mapper_expt Path instances
	"""
	
	length=len(seeds_xyz)
	seeds=[None]*length

	for i in range(length):
		seeds[i]=(Path(seeds_xyz[i,0],seeds_xyz[i,1],obj))

	return seeds


def npstereo_to_grid_xy_MORLIG_FORMAT(arr, msk_geodata, seeds, show_plots=0):
	"""
	Takes in points from the subset morlighem points csv (in npstereo projection) and "zeros" 
	them relative to the mask (also in npstereo projection) to which they are associated.

	Returns an x,y,z list
	"""

	#calc corners
	geotransform=msk_geodata.GetGeoTransform()
	post=geotransform[1]

	#open up seeds
	seeds_csv=pd.read_csv(seeds, sep=',')

	#calc grid coords	
	x=abs(seeds_csv['x_bamber'].values-geotransform[0])/post
	y=abs(seeds_csv['y_bamber'].values-geotransform[3])/post
	z=seeds_csv['bed_elev_gimp_thick_m'].values

	if show_plots==1:
		plt.imshow(arr)
		plt.scatter(x, y, c='g')
		plt.title("Seed/mask check...")
		plt.show()

	return np.asarray([x,y,z]).transpose()


def npstereo_to_grid_xy_MANUALLY_SEEDED(arr, mask_geodata, seeds, show_plots=0):
	"""
	Takes in manually seeded points (in npstereo projection) and "zeros" 
	them relative to the mask (also in npstereo projection) to which they are associated.

	Returns an x,y,z list
	"""

	#calc corners
	geotransform=mask_geodata.GetGeoTransform()
	post=geotransform[1]

	#open up seeds
	seeds_csv=pd.read_csv(seeds, sep=',')

	#calc grid coords	
	x=abs(seeds_csv['X'].values-geotransform[0])/post
	y=abs(seeds_csv['Y'].values-geotransform[3])/post
	
	if show_plots==1:
		plt.imshow(arr)
		plt.scatter(x, y, c='g')
		plt.title("Seed/mask check...")
		plt.show()

	return np.asarray([x,y]).transpose()


def grid_xy_to_map_xy(grid_xy, mask_geodata):
	"""
	Takes in grid points and converts them to the original geospatial coordinates 
	of the mask from which they have been calculated.
	
	Inputs:
	grid_xy 	   : list of gridded xy points
	msk_geodata    : mask geodata (gdal dataset object)

	Outputs:
	coordinate_xy  : list of xy map coordinates
	"""

	#calc corners
	geotransform=mask_geodata.GetGeoTransform()
	post=geotransform[1]

	#from grid to spatial
	x=(grid_xy[:,0]*post)+geotransform[0]
	y=((grid_xy[:,1]*post)*-1)+geotransform[3]

	coordinate_xy=np.vstack([x, y]).transpose()
	
	return coordinate_xy
	

def path_to_csv(complete_output, mask_geodata, opath='./'):
	"""
	Takes in a list of path object and writes out all point coordinates to a specific csv file

	Inputs:
	complete_output  : list of path objects
	mask_geodata     : mask geodata (gdal dataset object)
	"""
	
	check_output_dir(opath)

	i=0
	for path in complete_output:
		i+=1
		
		grid_xy=np.vstack([path.x, path.y]).transpose()
		coord_xy=grid_xy_to_map_xy(grid_xy, mask_geodata)

		coord_x = coord_xy[:,0].tolist()
		coord_y = coord_xy[:,1].tolist()

		ofile= "%s/path_%i.csv" %(opath, i)
		f = open(ofile, 'w')
		#f.write("grid_x, grid_y, dist_from_cofm\n")
		f.write("grid_x,grid_y,dist_from_cofm,coord_x,coord_y\n")
		#for z in sorted(zip(path.x,path.y,path.J,path.dx,path.dy, coord_x, coord_y), key = lambda x: x[2])[0:30]: # just 30 records?
		for z in zip(path.x,path.y,path.J,path.dx,path.dy, coord_x, coord_y):
			#print ("%f,%f,%f" %(z[0], z[1], z[2]))
			#f.write("%f,%f,%f\n" %(z[0], z[1], z[2]))
			f.write("%f,%f,%f,%f,%f\n" %(z[0], z[1], z[2], z[5], z[6]))

		f.close()

	return

if __name__  == "__main__":
	
	import ast

	print("Run from import")
	print("Functions for channel pathfinder.")
	print("Available functions:")

	def top_level_functions(body):
	    return (f for f in body if isinstance(f, ast.FunctionDef))

	def parse_ast(filename):
	    with open(filename, "rt") as file:
	        return ast.parse(file.read(), filename=filename)

	#Printing functions in module...
	#http://stackoverflow.com/questions/139180/listing-all-functions-in-a-python-module
	filename="Linear_referencing_FUNCTION.py"
	tree = parse_ast(filename)
	for func in top_level_functions(tree.body):
		print("  %s" % func.name)