from __future__ import division
import os
import sys

from osgeo import gdal, gdalconst, osr
from osgeo.gdalconst import * 

import util

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# NB/ The geotransorm contains the following:
# geotransform[0] /* top left x */
# geotransform[1] /* w-e pixel resolution */
# geotransform[2] /* rotation, 0 if image is "north up" */
# geotransform[3] /* top left y */
# geotransform[4] /* rotation, 0 if image is "north up" */
# geotransform[5] /* n-s pixel resolution */

'''
Various gdal realted functions to import raster images and their projections 
into python - can then be used as standard numpy matrixes

@ Chris 2013--onward...
'''

# Register driver
#gdal.AllRegister() #<-- useful only if reading in 
def openTiff(file_name):
	'''
	Converts a geotiff image to a numpy arra.
	
	Returns:
	
	image_array, pixelWidth, [geotransform, inDs]
	'''

	driver = gdal.GetDriverByName('GTiff') ## http://www.gdal.org/formats_list.html
	driver.Register()

	inDs = gdal.Open(file_name, GA_ReadOnly)
	
	if inDs is None:
		print("Couldn't open this file: " + file_name)
		sys.exit("Something's missing... can't process file.")
	else:
		print("%s opened successfully" %file_name)
			
		print('~~~~~~~~~~~~~~')
		print('Get image size')
		print('~~~~~~~~~~~~~~')
		cols = inDs.RasterXSize
		rows = inDs.RasterYSize
		bands = inDs.RasterCount
	
		print("columns: %i" %cols)
		print("rows: %i" %rows)
		print("bands: %i" %bands)
	
		print('~~~~~~~~~~~~~~')
		print('Get georeference information')
		print('~~~~~~~~~~~~~~')
		geotransform = inDs.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		print("origin x: %i" %originX)
		print("origin y: %i" %originY)
		print("width: %2.2f" %pixelWidth)
		print("height: %2.2f" %pixelHeight)
	
		# Set pixel offset.....
		print('~~~~~~~~~~~~~~' )
		print('Convert image to 2D array')
		print('~~~~~~~~~~~~~~')
		band = inDs.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		print(type(image_array))
		print(image_array.shape)
		
		return image_array, pixelWidth, [geotransform, inDs]#, cols, rows, bands, originX, originY, pixelWidth, pixelHeight,image_array_name]

def tiff_to_2d_array_COMPACT(file_name):
	'''
	Converts a geotiff image to a numpy arra.
	
	Retuns:
	
	[geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight,image_array_name]
	'''

	driver = gdal.GetDriverByName('GTiff') ## http://www.gdal.org/formats_list.html
	driver.Register()

	inDs = gdal.Open(file_name, GA_ReadOnly)
	
	if inDs is None:
		print("Couldn't open this file: " + file_name)
		sys.exit("Something's missing... can't process file.")
	else:
		print("%s opened successfully" %file_name)
			
		print('~~~~~~~~~~~~~~')
		print('Get image size')
		print('~~~~~~~~~~~~~~')
		cols = inDs.RasterXSize
		rows = inDs.RasterYSize
		bands = inDs.RasterCount
	
		print("columns: %i" %cols)
		print("rows: %i" %rows)
		print("bands: %i" %bands)
	
		print('~~~~~~~~~~~~~~')
		print('Get georeference information')
		print('~~~~~~~~~~~~~~')
		geotransform = inDs.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		print("origin x: %i" %originX)
		print("origin y: %i" %originY)
		print("width: %2.2f" %pixelWidth)
		print("height: %2.2f" %pixelHeight)
	
		# Set pixel offset.....
		print('~~~~~~~~~~~~~~' )
		print('Convert image to 2D array')
		print('~~~~~~~~~~~~~~')
		band = inDs.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		print(type(image_array))
		print(image_array.shape)
		
		return image_array, [geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight,image_array_name]

driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
driver.Register()

def ENVI_raster_binary_to_2d_array_COMPACT(file_name):
	'''
	Converts a binary file of ENVI type to a numpy arra.
	Lack of an ENVI .hdr file will cause this to crash
	
	Returns: 

	[geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name]
	'''
	driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
	driver.Register()

	inDs = gdal.Open(file_name, GA_ReadOnly)
	
	if inDs is None:
		print("Couldn't open this file: " + file_name)
		print('\nPerhaps you need an ENVI .hdr file? A quick way to do this is to just open the binary up in ENVI and one will be created for you.')
		sys.exit("Try again!")
	else:
		print("%s opened successfully" %file_name)
			
		print('~~~~~~~~~~~~~~')
		print('Get image size')
		print('~~~~~~~~~~~~~~')
		cols = inDs.RasterXSize
		rows = inDs.RasterYSize
		bands = inDs.RasterCount
	
		print("columns: %i" %cols)
		print("rows: %i" %rows)
		print("bands: %i" %bands)
	
		print('~~~~~~~~~~~~~~')
		print('Get georeference information')
		print('~~~~~~~~~~~~~~')
		geotransform = inDs.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		print("origin x: %i" %originX)
		print("origin y: %i" %originY)
		print("width: %2.2f" %pixelWidth)
		print("height: %2.2f" %pixelHeight)
	
		# Set pixel offset.....
		print('~~~~~~~~~~~~~~' )
		print('Convert image to 2D array')
		print('~~~~~~~~~~~~~~')
		band = inDs.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		print(type(image_array))
		print(image_array.shape)
		
		return [geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name]

def ENVI_raster_binary_to_2d_array(file_name):
	'''
	Converts a binary file of ENVI type to a numpy arra.
	Lack of an ENVI .hdr file will cause this to crash
	
	Retunrs: 

	geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name
	'''
	driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
	driver.Register()

	inDs = gdal.Open(file_name, GA_ReadOnly)
	
	if inDs is None:
		print("Couldn't open this file: " + file_name)
		print('\nPerhaps you need an ENVI .hdr file? A quick way to do this is to just open the binary up in ENVI and one will be created for you.')
		sys.exit("Try again!")
	else:
		print("%s opened successfully" %file_name)
			
		print('~~~~~~~~~~~~~~')
		print('Get image size')
		print('~~~~~~~~~~~~~~')
		cols = inDs.RasterXSize
		rows = inDs.RasterYSize
		bands = inDs.RasterCount
	
		print("columns: %i" %cols)
		print("rows: %i" %rows)
		print("bands: %i" %bands)
	
		print('~~~~~~~~~~~~~~')
		print('Get georeference information')
		print('~~~~~~~~~~~~~~')
		geotransform = inDs.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		print("origin x: %i" %originX)
		print("origin y: %i" %originY)
		print("width: %2.2f" %pixelWidth)
		print("height: %2.2f" %pixelHeight)
	
		# Set pixel offset.....
		print('~~~~~~~~~~~~~~' )
		print('Convert image to 2D array')
		print('~~~~~~~~~~~~~~')
		band = inDs.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		print(type(image_array))
		print(image_array.shape)
		
		return geotransform, inDs, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name

def load_envi(file_name):
	'''
	Loads an ENVI binary as a numpy image array also returning a tuple including map and projection info

	Returns: 

	image_array, post, (geotransform, inDs)
	'''
	geotransform, inDs, _, _, _, _, _, post, _, image_array, _ = ENVI_raster_binary_to_2d_array(file_name)
	return image_array, post, (geotransform, inDs)

# Prerequisite to "ENVI_raster_binary_from_2d_array" if output image is different to original input for which geotransform was set
def xy_dimensions_Geotransform_update(geotransform, image_in_x_px, image_in_y_px, new_x_px, new_y_px):
	'''
	DEPRECATED: JUST USE ENVI_raster_binary_from_2d_array
	
	Recalculates xy dimensions of an image following resampling 
	- prior step to outputting a resampled array as a binary
	'''		
	print("Updating pixelHeight and Width values")
	pixelWidth_original = geotransform[1]
	pixelHeight_original = geotransform[5]
	pixel_width_new_image = (image_in_x_px * pixelWidth_original) / new_x_px ## gives pixel size in metres
	pixel_height_new_image =  (image_in_y_px * pixelHeight_original) / new_y_px ## gives pixel size in metres
	
	return pixel_width_new_image, pixel_width_new_image


## Creates an output image as an ENVI binary - this can be a different size to the original input image from which the output array has been developed
## When vieiwing in ENVI, if the image is smaller, you'll need to increase the magnification to view it - a geographic link will be possible (but not just a spatial link)

def ENVI_raster_binary_from_2d_array(envidata, file_out, post, image_array):
	'''
	Converts a numpy array back to an ENVI binary - requires geotransform and projection 
	information as imported using ENVI_raster_binary_to_2d_array() or load_ENVI(). If 
	resampling has taken place between the initial ENVI load (for which getransform and 
	projection info is specific) then the new posting size must also be passed in to 
	enable rescaling of pixels accordingly 

	Returns:

	new_geotransform,new_projection,file_out
	'''
	util.check_output_dir(file_out)
	original_geotransform, inDs = envidata

	rows, cols = image_array.shape
	bands = 1

	# Creates a new raster data source
	outDs = driver.Create(file_out, cols, rows, bands, gdal.GDT_Float32)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post])
	outDs.SetProjection(inDs.GetProjection())

	#Write raster datasets
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)
	
	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print("Output binary saved: ", file_out)
	
	return new_geotransform,new_projection,file_out


def ARC_ASCII_from_2d_array(original_geotransform, inds, file_out, post, image_array):
	'''
	Saves an input array as an ASCII file

	Returns:

	---
	'''

	driver = gdal.GetDriverByName('ASCII') ## Seems to work better if you use the driver that you originally read in 'image_array' with...
	driver.Register()

	rows, cols = image_array.shape
	bands = 1

	outDs = driver.Create(file_out, cols, rows, bands, 6)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	#outDs.SetGeoTransform(inds.GetGeoTransform()) ### this needs amending to take in the new post size ( == pixel_width_new_image)
	outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post]) ### this needs amending to take in the new post size ( == pixel_width_new_image)
	outDs.SetProjection(inds.GetProjection())

	#Write raster datasets
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)

	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print("Output binary saved: ", file_out)


def tiff_back_from_2d_array(tiffdata, file_out, post, image_array):
	'''
	Converts a numpy array back to a tiff - requires geotransform and projection 
	information as imported using ENVI_raster_binary_to_2d_array() or load_ENVI(). If 
	resampling has taken place between the initial ENVI load (for which getransform and 
	projection info is specific) then the new posting size must also be passed in to 
	enable rescaling of pixels accordingly 

	Returns:

	new_geotransform,new_projection,file_out
	'''
	driver = gdal.GetDriverByName('GTIFF') ## Seems to work better if you use the driver that you originally read in 'image_array' with...
	driver.Register()
	
	original_geotransform, inDs = tiffdata

	rows, cols = image_array.shape
	bands = 1

	# Creates a new raster data source
	outDs = driver.Create(file_out, cols, rows, bands, gdal.GDT_Float32)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post])
	outDs.SetProjection(inDs.GetProjection())

	#Write raster datasets
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)
	
	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print("Output binary saved: ", file_out)
	
	return new_geotransform,new_projection,file_out

#############################
#############################
## CREATE RASTER FROM SCRATCH
#############################
#############################

def define_geotransform_info(tl_x, tl_y, post, rotation=0):
	'''
	Set up geotransform info

	Returns: 

	Geotransform tuple object 

	geotransform[0] /* top left x */
	geotransform[1] /* w-e pixel resolution */
	geotransform[2] /* rotation, 0 if image is "north up" */
	geotransform[3] /* top left y */
	geotransform[4] /* rotation, 0 if image is "north up" */
	geotransform[5] /* n-s pixel resolution */
	'''

	geotransform = np.zeros(6)
	geotransform[0] = tl_x
	geotransform[1] = post
	geotransform[2] = rotation
	geotransform[3] = tl_y
	geotransform[4] = rotation
	geotransform[5] = -post

	geotransform=geotransform.tolist()

	return geotransform


#def define_projections(test):
	#'''
	#Set the projection of the raster to be created: http://www.gdal.org/osr_tutorial.html
	#'''

	#outRasterSRS = osr.SpatialReference()
    #outRasterSRS.ImportFromEPSG(4326)
    #outRaster.SetProjection(outRasterSRS.ExportToWkt())
	
	#return projection


def tiff_from_array_SET_GEO_INFO(geotransform, file_out, image_array, cols, rows):
	'''
	Creates a tiff from a numpy array - requires geortransform and projection info to be set

	Requires the geotransform to have been preset using 'define_geotransform'

	NB/ Can't get projection to work

	Returns:

	NOTHING
	'''

	driver = gdal.GetDriverByName('GTIFF')
	outRaster = driver.Create(file_out, cols-1, rows-1, 1, GDT_Float32)
	outRaster.SetGeoTransform(geotransform)

	### THIS IS THE BIT I'M STUCK ON!!!
	'''
	proj = osr.SpatialReference()
	proj.SetWellKnownGeogCS( "EPSG:3995" )	# http://www.spatialreference.org/ref/epsg/3995/
	#set standard parallel = 71
	#set central meridian = -39
	outRaster.SetProjection(proj.ExportToWkt())
	'''
	### THIS IS WHERE THE BIT I'M STUCK ON ENDS!!

	outband = outRaster.GetRasterBand(1)
	outband.WriteArray(image_array)

	print("Output tiff created: ", file_out)

	#return new_geotransform,new_projection,file_out
	
def tiff_from_array(file_out, image_array, cols, rows):
	'''
	Creates a tiff from a numpy array

	Returns:

	NOTHING
	'''

	driver = gdal.GetDriverByName('GTIFF')
	outRaster = driver.Create(file_out, cols, rows, 1, GDT_Float32)
	
	outband = outRaster.GetRasterBand(1)
	outband.WriteArray(image_array)

	print*("Output tiff created: ", file_out)

def subset_raster_to_extent_of_other(src_filename, match_filename, dst_filename):
	"""
	Takes in 2 rasters - one that needs clipping (src_filename) and another (match_filename).
	You will be clipping src_filename to the extent and post size of match_filename

	Also, pass in a path and filename to define where to keep your output.

	RETURN: nothing

	Modified from this post: http://stackoverflow.com/questions/10454316/how-to-project-and-resample-a-grid-to-match-another-grid-with-gdal-python
	@date 24/03/16
	"""

	# Source
	src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
	src_proj = src.GetProjection()
	src_geotrans = src.GetGeoTransform()

	# We want a section of source that matches this:
	match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
	match_proj = match_ds.GetProjection()
	match_geotrans = match_ds.GetGeoTransform()
	wide = match_ds.RasterXSize
	high = match_ds.RasterYSize

	# Output / destination
	dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
	dst.SetGeoTransform( match_geotrans )
	dst.SetProjection( match_proj)

	# Do the work
	gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

	del dst # Flush


	

def xy_mesh(nx, ny, x_min=0, x_max=1, y_min=0, y_max=1):
	"""
	Creates a mesh grid of an input array
	VARIABLES
		nx      array columns 
		ny      array rows
	
	RETURN
		xv		x coordinate mesh of same dimensions as array
		yv		y coordinate mesh of same dimensions as array
	"""

	x = np.linspace(x_min, x_max, nx)
	y = np.linspace(y_min, y_max, ny)
	xv, yv = np.meshgrid(x, y)
	
	return xv, yv

def raster_cell_centres_as_xy(extent, raster_cols, raster_rows, raster_post, plot=0):
	"""
	"""
	# These max/min extent values are for the corners  of the raster
	# Half of the post is subtracted to get the coordinates at the centre 
	# of the corner cells
	xmin=extent[0]+np.round(raster_post)/2
	xmax=extent[1]-np.round(raster_post)/2
	ymin=extent[2]+np.round(raster_post)/2
	ymax=extent[3]-np.round(raster_post)/2

	xv, yv = xy_mesh(raster_cols, raster_rows, \
					 xmin, xmax, ymin, ymax)

	if plot==1:
		fig=plt.figure()
		ax1=fig.add_subplot(121)
		ax2=fig.add_subplot(122)
		ax1.imshow(xv, extent=[xmin, xmax, xmin, xmax]), ax1.set_title("x grid"), ax1.set_yticklabels("")
		ax2.imshow(yv, extent=[ymin, ymax, ymin, ymax]), ax2.set_title("y grid"), ax2.set_xticklabels("")
		plt.show()

	return xv, yv

def xyz_triple(xv, yv, zv):
	"""
	Takes in three grids of the same dimension (e.g. x, y and z) and formats 
	them as a nx3 array (where n is the number of triplets/observations/locations)

	VARIABLES 

	xv 	- 	xv can be created using raster_cell_centres_as_xy 
	yv	-	yv can be created using raster_cell_centres_as_xy 
	zv	-	the n-dimensional array of the raster you should have already read in.

	RETRUN

	raster_xyz
	"""
	try:
		assert xv.shape == yv.shape
	except AssertionError:
		print("xv and yv not of equal diomensions")

	try:
		assert xv.shape == zv.shape
	except AssertionError:
		print("zv not of the same dimensions as xv and yv")
	
	raster_xyz=np.vstack([xv.flatten(),yv.flatten(),zv.flatten()]).transpose()

	return raster_xyz


def xyz_triple_as_pandas_df(numpy_xyz):
	"""
	Takes in an nx3 numpy array representing an xyz triplet array and convert it to a pandas dataframe

	VARIABLES

	numpy_xyz 	an nx3 numpy array representing an xyz triplet array (create using xyz_triple)

	RETURN

	xyz_df	
	"""
		
	indx=np.arange(0, numpy_xyz.shape[0])
	xyz_df = pd.DataFrame(numpy_xyz, index=indx)
	xyz_df.columns = ['x','y','z']

	return xyz_df


def xyz_from_grid(x,y,z, pnts_out):
	"""
	Takes in three grids of the same dimension (e.g. x, y and z) and 
	writes out their values as a csv in the format x,y,z. The x and y 
	grids can be created using raster_cell_centres_as_xy().

	RETURN:
		nothing
	"""
	x_flt=x.flatten()
	y_flt=y.flatten()[::-1]
	z_flt=z.flatten()

	util.check_output_dir(pnts_out)
	fout = open(pnts_out, 'w')
	fout.write("x,y,z\n")

	print("Writing out %i xyz triples to %s" %(len(z_flt),pnts_out))
	for i in range(0, len(z_flt)):
		if not np.isnan(z_flt[i]):
			fout.write("%.6f,%.6f,%.2f\n" %(x_flt[i], y_flt[i], z_flt[i]))

	fout.close()

def tiff_from_2d_array(original_dataset, file_out, post, image_array):
	'''
	Converts a numpy array back to a tiff.

	Pass in a rasterdatset object (i.e. your array to write will match the geotransform of an 
	existing raster dataset).

	The post variable allwos for resampling of your new array, and modification of a copy of the 
	geotransform of the exisiting original dataset you pass in.

	Returns:
		Nothing
	
	'''
	driver = gdal.GetDriverByName('GTIFF') ## Seems to work better if you use the driver that you originally read in 'image_array' with...
	driver.Register()
	
	inDs = original_dataset
	original_geotransform = inDs.GetGeoTransform()

	rows, cols = image_array.shape
	bands = 1

	# Creates a new raster data source
	outDs = driver.Create(file_out, cols, rows, bands, gdal.GDT_Float32)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post])
	outDs.SetProjection(inDs.GetProjection())

	#Write raster datasets
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)
	
	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print("Output binary saved: ", file_out)
	
	#return new_geotransform,new_projection,file_out

if __name__  == "__main__":

	print("Various raster related geoprocessing fucntions.")
	print("Must be run from import.")