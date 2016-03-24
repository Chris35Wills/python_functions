from __future__ import division

import sys
import os
import time as time # for reading in a timer
import numpy as np # maths functions (arrays etc.)
import math
from matplotlib import pyplot as plt # for ploting
from scipy import signal # for convolution function
from scipy import ndimage # for resampling image
from scipy.fftpack import fft2
from matplotlib import cm # colour mapping
import matplotlib as matplotlib
import matplotlib.pyplot as plt
import copy as cp
from numpy import *
import datetime
import random
from scipy import ndimage
from time import gmtime, strftime
import pylab as pl
from glob import glob
from osgeo import gdal, gdalconst # for reading in raster
from osgeo.gdalconst import * # for reading in raster

# Register driver
#gdal.AllRegister() #<-- useful only if reading in 
driver = gdal.GetDriverByName('ENVI') ## http://www.gdal.org/formats_list.html
driver.Register()

def ARC_ASCII_to_2d_array(file_name):
	
	'''
	Converts an ArcGIS ASCII raster into an array using GDAL - note that the maximum raster file size is 2MB
	The default NoData value is -3.40282347e+38  and so this should be dealt with once the array is acquired 
	(best to use something like: image_array[image_array==image_array.min()] = np.nan)
	'''

	print "~~~~~~~~~~~ WARNING ~~~~~~~~~~~"
	print "Arc's default NoData value is -3.40282347e+38  and so this should be dealt with once the array is acquired"
	print "... best to use something like: image_array[image_array==image_array.min()] = np.nan"
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	
	driver = gdal.GetDriverByName('AAIGrid') ## http://www.gdal.org/formats_list.html
	driver.Register()

	# open file
	inds = gdal.Open(file_name, GA_ReadOnly)
	
	if inds is None:
		print "Really sorry Sir but I couldn't open this blasted file: " + file_name
		print '\nPerhaps you need an ENVI .hdr file? If so, just open the binary up in ENVI and one will be created for you!'
		sys.exit("Try again!")
	else:
		print "%s opened successfully" %file_name
			
		print '~~~~~~~~~~~~~~'
		print 'Get image size'
		print '~~~~~~~~~~~~~~'
		cols = inds.RasterXSize
		rows = inds.RasterYSize
		bands = inds.RasterCount
	
		print "columns: %i" %cols
		print "rows: %i" %rows
		print "bands: %i" %bands
	
		print '~~~~~~~~~~~~~~'
		print 'Get georeference information'
		print '~~~~~~~~~~~~~~'
		geotransform = inds.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
	
		print "origin x: %i" %originX
		print "origin y: %i" %originY
		print "width: %2.2f" %pixelWidth
		print "height: %2.2f" %pixelHeight
	
		# Set pixel offset.....
		print '~~~~~~~~~~~~~~' 
		print 'Convert image to 2D array'
		print '~~~~~~~~~~~~~~'
		band = inds.GetRasterBand(1)
		image_array = band.ReadAsArray(0, 0, cols, rows)
		image_array_name = file_name
		print type(image_array)
		print shape(image_array)
		
		return geotransform, inds, cols, rows, bands, originX, originY, pixelWidth, pixelHeight, image_array, image_array_name
	
# Prerequisite to "ENVI_raster_binary_from_2d_array" if output image is different to original input for which geotransform was set
def xy_dimensions_Geotransform_update(geotransform, image_in_x_px, image_in_y_px, new_x_px, new_y_px):
	print "Updating pixelHeight and Width values"
	pixelWidth_original = geotransform[1]
	pixelHeight_original = geotransform[5]
	pixel_width_new_image = (image_in_x_px * pixelWidth_original) / new_x_px ## gives pixel size in metres
	pixel_height_new_image =  (image_in_y_px * pixelHeight_original) / new_y_px ## gives pixel size in metres
	
	return pixel_width_new_image, pixel_width_new_image


## Creates an output image as an ENVI binary - this can be a different size to the original input image from which the output array has been developed
## When vieiwing in ENVI, if the image is smaller, you'll need to increase the magnification to view it - a geographic link will be possible (but not just a spatial link)

def ARC_ASCII_from_2d_array(original_geotransform, post_original, opath, file_out, cols_new_image, rows_new_image, bands, inds, pixel_width_new_image, pixel_height_new_image, image_array):

	if os.path.isdir(opath):
		print "output_path exists"	
	else:
		print "output_path DOESN'T exist...\n"
		os.makedirs(opath) 
		print "...but it does now"
	
	output_path = "%s/%s" %(opath,file_out)
	
	# Creates a new raster data source
	#outDs = driver.Create(output_path, cols_new_image, rows_new_image, bands, gdal.GDT_Float32)
	print output_path, cols_new_image, rows_new_image, bands, gdal.GDT_Float32
	outDs = driver.Create(output_path, int(cols_new_image), int(rows_new_image), bands, 6)
	
	# Write metadata
	originX = original_geotransform[0]
	originY = original_geotransform[3]

	#outDs.SetGeoTransform(inds.GetGeoTransform()) ### this needs amending to take in the new post size ( == pixel_width_new_image)
	outDs.SetGeoTransform([originX, pixel_width_new_image, 0.0, originY, 0.0, -1*(pixel_height_new_image)]) ### this needs amending to take in the new post size ( == pixel_width_new_image)
	outDs.SetProjection(inds.GetProjection())

	#Write raster datasets
	#for i in range(1):
	outBand = outDs.GetRasterBand(1)
	outBand.WriteArray(image_array)

	# Clear variables
	band = None
	image_array = None
	
	new_geotransform = outDs.GetGeoTransform()
	new_projection = outDs.GetProjection()
	
	print "Output binary saved: ", output_path
	
	return new_geotransform,new_projection,output_path




