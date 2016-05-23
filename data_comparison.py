import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
##from ~github/roll_your_own_py/src/geospatial
import nearest_neighbour
##from ~github/python_functions
import data_comparison
import georaster
import raster_functions
import util

def point_differences(data_1, data_2, search_dist=100, output_csv='', plot=True, plot_title='', fig_outpath='', verbose=True):
	"""
	Takes in two datasets of points and calculates the differences between them. 
	Nearest neighbours from data set 1 to data set 2 are found and then subtracted to assess agreement.
	Plots a quick overview and writes out the data as a pandas dataframe.

	VARIABLES
	
	data_1 			= points which will be used to compare to data_2, from which neighbours 
					  will be sought - expects column headers to be x, y and z
	data_2 			= dataset which will be used to associated neighbours too (i.e. 
					  the maximum comparisons you can have will be equal to the length 
					  of this dataset, assuming they are within the tolerance set by 
					  the search_dist variable) - expects column headers to be x, y and z
	search_dist		= (defaults to 100)
	output_csv 		= path to save csv of data comparison (format data_1_x|data_1_y|data_1_z|data_1_x|data_1_y|data_1_z|data_2 - data_1 difference)
						default is '' and no csv is saved
	plot 			= if True, displays a quick overview plot of the differences (default = True)
	plot_title 		= title of overview plot - only used if plot is True
	verbose 		= print out sanity check messages (default=True)

	RETURN 

	difference_df

	@author	: Chris Williams
	@date	: 26th April 2016
	"""
	
	print("\nCalculating nearest neighbours...")
	dists_nn, indxs_nn = nearest_neighbour.get_nn(data_1, data_2, nn=1, radius=search_dist) # outputs are same length as data_2, index values in indxs_nn are of the data_1 dataset

	#keep only observations that are within the "search_dist" of a gridded point
	infinity=float("inf")
	indx_of_observations_wth_no_nn = (dists_nn == infinity).nonzero() # see here: http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.nonzero.html

	if verbose: print("Total (data_2) observations within extent: %f" %(len(data_2)))
	if verbose: print("\nNumber of observations (data_2) with no nn from data_1: %i" %(len(indx_of_observations_wth_no_nn[0])))
	if verbose: print("Only considering observations with neighbours from data_1 within the set search distance of %i units" %(search_dist))
	if verbose: print("Observations (data_2) to ignore: %f" %(len(indx_of_observations_wth_no_nn[0])))
	if verbose: print("Observations (data_2) to remain: %f" %(len(data_2)-len(indx_of_observations_wth_no_nn[0])))

	if verbose: print("\nBefore removal of (data_2) points with no nn...")
	if verbose: print(len(data_2))

	points_after_drop = data_2.drop(data_2.index[list(indx_of_observations_wth_no_nn[0])])
	points_after_drop=points_after_drop.reset_index() # reset the index (so index matches row number)
	points_after_drop=points_after_drop.drop(points_after_drop.columns[0], axis=1) # remove first column which wil be the inidices

	if verbose: print("\nAfter removal of (data_2) points with no nn...")
	if verbose: print(len(points_after_drop))

	assert (len(data_2)-len(indx_of_observations_wth_no_nn[0])) == len(points_after_drop)

	#remove any items in dists_nn and indxs_nn where dists_nn==Inf
	if verbose: print("\nBefore removal of points with no nn...")
	if verbose: print(len(indxs_nn))
	if verbose: print(len(dists_nn))
	indxs_nn=indxs_nn[dists_nn!=infinity]
	dists_nn=dists_nn[dists_nn!=infinity]
	if verbose: print("\nAfter removal of points with no nn...")
	if verbose: print(len(indxs_nn))
	if verbose: print(len(dists_nn))

	assert len(dists_nn) == len(points_after_drop)

		# get x, y and z value of nn
	x_nn = data_1['x'].iloc[indxs_nn]
	y_nn = data_1['y'].iloc[indxs_nn]
	z_nn = data_1['z'].iloc[indxs_nn]

	#calculate differences
	diffs=points_after_drop['z'].values-z_nn.values
	
	if plot:
		plt.scatter(np.arange(0, len(diffs), 1), diffs)
		if plot_title != '': plt.title(plot_title)#plt.title("Summary of Gravity/MBES differences \n (relative to the DEM provided by I. Fenty (April 2016))")
		plt.ylabel("Elevation difference (m)")
		plt.axhline(0, color='red', linestyle='--', lw=1)
		
		if fig_outpath != '':
			util.check_output_dir(fig_outpath)
			plt.savefig(fig_outpath)

		plt.show()
	
	# output a new dataframe
	points_after_drop['data2_x'] = x_nn.values
	points_after_drop['data2_y'] = y_nn.values
	points_after_drop['data2_z'] = z_nn.values
	points_after_drop['DIFF_data_2_minus_data_1'] = diffs

	# write dataframe to csv
	if output_csv != "":
		util.check_output_dir(output_csv)
		points_after_drop.to_csv(output_csv)
	else:
		print("\nNo csv output path set so not saving")

	#if modify_header:

	return points_after_drop
