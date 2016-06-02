"""
Wrappers to make pandas functionality even more specific

@author Chris
@date June 2nd 2016 onwards...
"""

import numpy as np
import pandas as pd

#tests
def test_xy_dist():

	x=np.arange(0,100,1)
	y=np.arange(0,100,1)
	index=np.arange(0, len(x), 1)
	columns=['x','y']
	df=pd.DataFrame(index=index, columns=columns)
	df['x']=x
	df['y']=y

	try:
		spacing, cumulative = pandas_xy_dist(df)
	except:
		print("pandas_xy_dist failed")

#fucntions
def pandas_xy_dist(df, x_col='x', y_col='y'):
	"""
	Takes in a pandas dataframe containing x and y coordinates. Calculates the euclidean distance between point pairs as wella s the cumulative distance. 

	VARIABLES

	df : a pandas dataframe
	x_col : x column header (default 'x')
	y_col : y column header (default 'y')

	RETURN

	Neighbour didtance array
	Cumulative didtance array
	"""

	df=df.assign(x_diff=pd.rolling_apply(df[x_col], 2, \
	  lambda x : x[1]-x[0])) 

	df=df.assign(y_diff=pd.rolling_apply(df[y_col], 2, \
	  lambda y : y[1]-y[0]))

	df['xy_distance']=np.hypot(df['y_diff'], df['x_diff'])

	spacing = df['xy_distance'].values
	cumulative = np.asarray(np.cumsum(df['xy_distance']))
	cumulative[0]=0

	df = df.drop('x_diff', 1)
	df = df.drop('y_diff', 1)

	df['cumulative']=cumulative
	
	return spacing, cumulative, df

