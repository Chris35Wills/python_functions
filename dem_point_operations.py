import sys
import numpy as np
import pandas as pd
sys.path.append('./georaster')
import georaster 

"""
DEM and point operations
"""

def extract_values(dem, points):
		"""
		Extracts points from a dem at point locations - binds them to a pandas dataframe

		Variables:	
		dem    : a georaster object
		points : a pandas dataframe with headers of "x" and "y"

		Returns:
		points (pandas dataframe)
		"""

		dem_tl_x=dem.extent[0] *-1 #-800000 #*-1 << must do this
		dem_tl_y=dem.extent[3]     #-599500.
		post=dem.xres

		pnt_x=points['x'].values
		pnt_y=points['y'].values

		ix=np.floor((pnt_x+dem_tl_x)/post)   # origin is top left
		iy=np.floor(((dem_tl_y)-pnt_y)/post) # origin is top left

		dem_values=dem.r[list(iy),list(ix)]

		points['z']=pd.Series(dem_values, index=points.index)

		return points