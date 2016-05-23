from __future__ import division

import numpy as np

def get_index(arr, value):
	"""
	Gets the first index of a value (or index of an element closest to a given value) from a numpy array

	VARIABLES
	arr 	: a numpy array
	value 	: a value to search for in arr

	RETURNS

	pos 	: an index
	"""
	
	if value != 0.:
		test= (arr)/np.float(value) 				# want value closest to 1
		test= np.abs(test-1) 						# want value closest to 1
		pos = np.int(np.where(test==test.min())[0]) # get index of element closest to value of interest
	elif value == 0.:
		pos = np.int(np.where(arr==value)[0]) 		# get index of element closest to value of interest

	return pos

