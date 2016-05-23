from __future__ import division

import numpy as np

def get_first_index(arr, value):
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

def get_index_1d(array, select_array):
	"""
	Get the index of values from select_array in array

	Variables:
	array        : 	a 1d numpy array
	select array : 	a 1d numpy array
	
	Return:
	1d array of indicies

	Example:
	a=np.array([1,2,3,4,5,6,6,6,6,7,7,8,9,9])
	b=np.array([6,7,9])
	In  : get_index_1d(a, b)
	Out : (array([ 5,  6,  7,  8,  9, 10, 12, 13], dtype=int64),)
	"""
	idx = np.in1d(array.ravel(), select_array.ravel())
	x_indx = np.where(idx.reshape(array.shape))
	return x_indx


def get_index_2d(array, select_array):
	"""
	Get the index of values from select_array in array

	Variables:
	array        : 	a 2d numpy array
	select array : 	a 2d numpy array

	Return:
	array of indicies in x
	array of indicies in y

	Example:
	a=np.array([1,2,3,4,5,6,6,6,6,7,7,8,9,9],[1,2,3,4,5,6,6,6,6,7,7,8,9,9])
	b=np.array([6,7,9])
	In  : get_index_1d(a, b)
	Out : (array([ 5,  6,  7,  8,  9, 10, 12, 13], dtype=int64),)
	"""
	idx = np.in1d(array.ravel(), select_array.ravel())
	y_indx, x_indx = np.where(idx.reshape(array.shape))
	return y_indx, x_indx