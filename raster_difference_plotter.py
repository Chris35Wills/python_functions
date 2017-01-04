"""
Takes in 2 rasters, calcs difference and plots it with a diverging colorbar
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import georaster as geo
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

# matplotlib settings

matplotlib.rc('xtick', labelsize=8)#5) 
matplotlib.rc('ytick', labelsize=8)#5) 
contour_label_size=8#5
title_size=10
axis_label_size=8

def add_colorbar(ax, im):
	"""
	Adds colorbar to fig on new axis

	im = an imshow handle (e.g. im= ax1.imshow(blah, blah...))
	"""

	# add colorbar
	##plt.colorbar(title=cbar_tile, cb = 
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	cb = plt.colorbar(im, cax=cax)
	cb.set_label('Difference (m)', rotation=270)
	cb.ax.get_yaxis().labelpad=15 # add padding to move color bar label away

	return ax

def diff_plot(ax, z_array, extent,  contour_min, contour_max, contour_interval=100, cmap=plt.cm.gist_earth, underlay_array=''):

	###########
	# Enable normalisation of colorbar to centre it on 0
	# See: http://matplotlib.org/users/colormapnorms.html
	class MidpointNormalize(colors.Normalize):
		def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
			self.midpoint = midpoint
			colors.Normalize.__init__(self, vmin, vmax, clip)

		def __call__(self, value, clip=None):
			# I'm ignoring masked values and all kinds of edge cases to make a
			# simple example...
			x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1] # x is your range and y is your idealised range
			return np.ma.masked_array(np.interp(value, x, y), np.isnan(value)) # the interp fucntion translates a value to the normalised scale (y), the np.isnan(value)a acts as a mask to prevent plotting of nan values

	if underlay_array != '':
		ax.imshow(underlay_array, cmap=plt.cm.YlGn, alpha=0.5, extent=extent)

	im = ax.imshow(z_array, extent=extent, interpolation='none', cmap=cmap, origin='upper', clim=(contour_min, contour_max), norm=MidpointNormalize(midpoint=0.,vmin=contour_min, vmax=contour_max))
	#im = ax.imshow(z_array, extent=extent, interpolation='none', cmap=cmap, origin='upper', clim=(contour_min, contour_max))

	###########
	# add contours
	contourBars=np.arange(contour_min, contour_max, contour_interval)
	CS=ax.contour(z_array, levels=contourBars, origin='upper', extent=extent, linewidths=0.8, linestyle='solid', colors='0.2')

	###########
	# add colorbar
	#ax = add_colorbar(ax, im)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	cb = plt.colorbar(im, cax=cax)#, ticks=v) # can also add tick marks: http://stackoverflow.com/questions/5826592/python-matplotlib-colorbar-range-and-display-values
	cb.set_label('Difference (m)', rotation=270)
	cb.ax.get_yaxis().labelpad=15 # add padding to move color bar label away

	return ax

def plot_it(ras1, ras2, contour_min=-800, countour_max=800, unq_nan=-1.6999999999999999e+308, ofile='./diff_plot_temp.png', save_it=False):
	'''
	Creates a difference plot where positive values occur where ras1 > ras2
	Assumes projected coordinates (northing and easting) in metres

	
	contour_min = min conotur that will be used in color scaling
	contour_max = max conotur that will be used in color scaling
	unq_nan  	= other value in ras1 or ras2 to treat as NaN - used to mask equivalent regions in the difference surface
	save_it 	= if True, file will be saved to ofile, otherwise, figure will plot on screen 
	ofile 		= destination of plot
	'''

	##############
	# read in data
	ras_1 = geo.SingleBandRaster(ras1)
	ras_2 = geo.SingleBandRaster(ras2)

	#if ras_1.extent!=ras_2.extent:
	#	sys.exit("Raster extents differ - they must be the same \n >>> Exiting difference plotting")
	#else:
		
	##############
	# calc difference
	diff=ras_1.r-ras_2.r

	diff[ras_1.r==np.nan]=np.nan   				# if synth == nan, then diff == nan
	diff[ras_2.r==np.nan]=np.nan 				# if bed2013 == nan, then diff == nan
	diff[diff==unq_nan]=np.nan 	# if R no data value (-1.6999999999999999e+308), present then diff == nan

	print(diff)

	##############
	# plot settings (apply to all)
	cmap=cm.RdBu#plt.cm.gist_earth
	extent=np.array(ras_1.extent)/1000  # extent with values at 10^-3

	##############
	# create plot
	fig=plt.figure()

	ax1=fig.add_subplot(111)
	ax1=diff_plot(ax1, diff, extent, contour_min, contour_max, cmap=cmap, underlay_array='')

	ax1.set_ylabel(r'Northing (m x 10$^{-3}$)', fontsize=axis_label_size)
	ax1.set_xlabel(r'Easting (m x 10$^{-3}$)', fontsize=axis_label_size)

	#fig.suptitle("Synthetic (IBCAO) differences")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	
	if save_it:
		print("Saving plot")
		#plt.savefig(ofile, figsize=(3, 5), transparent=True, dpi=300, format='pdf')
	else:
		plt.show(block=False)


# EXAMPLE

new_F="C:/analysis_outputs_TEMP/Godthabsfjord_SYNTH_output/out_I_and_II/synth_dem.tif"
original_F="C:/analysis_outputs_TEMP/Godthabsfjord_SYNTH_output/bamber_2013_dem_to_Godthabsjord_extent.tif"
ofile="C:/analysis_outputs_TEMP/Godthabsfjord_SYNTH_output/diffPlot.pdf"

plot_it(ras1=new_F, ras2=original_F, \
		ofile=ofile, contour_min=-800, countour_max=800, \
		unq_nan=-1.6999999999999999e+308, save_it=False)