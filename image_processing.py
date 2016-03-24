'''
Image processing functions

Chris 20/03/15
'''

import numpy as np
from scipy import ndimage

def block_mean(ar, fact):
	'''
	Calculates the blockmean of an input array, the block being defined by the factor applied

	E.g., a (100, 200) shape array using a factor of 5 (5x5 blocks) results in a (20, 40) array result:

	ar = np.random.rand(20000).reshape((100, 200))
	block_mean(ar, 5).shape  # (20, 40)

	Taken from: http://stackoverflow.com/questions/18666014/downsample-array-in-python
	'''
    
    assert isinstance(fact, int), type(fact)
    sx, sy = ar.shape
    X, Y = np.ogrid[0:sx, 0:sy]
    regions = sy/fact * (X/fact) + Y/fact
    res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
    res.shape = (sx/fact, sy/fact)
    
    return res

