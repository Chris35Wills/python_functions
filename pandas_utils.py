"""
Wrappers to make pandas functionality even more specific

@author Chris
@date June 2nd 2016 onwards...
"""

import numpy as np
import pandas as pd
import util

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


import pandas as pd
import numpy as np
run="run_3"
pnt_path="C:/GitHub/synthetic_channels/FENTY_DEM_along_track_FT/%s/good_paths" %run
pnt_f='%s/densified_path_3_clipped_with_elev.csv' %pnt_path
pnts=pd.read_csv(pnt_f, sep=',')
pnts['z_cubic'][120:]=np.nan # set nans at end
pnts['z_cubic'][0:10]=np.nan # set nans at head

def location_of_nan(df, col_name):
	"""
	Gets indicies for np.nan values in specific column of dataframe

	VARIABLES
	df : Pandas DataFrame
	col_name : column name to consider
	
	RETURN
	nan_loc : indicies for nan values in specified column (pandas.core.index.Int64Index)
	bools : 1/0 boolean (pandas.core.series.Series)
	"""
	
	bools=np.isnan(df[col_name])
	
	nan_loc=bools[bools==True].index

	return nan_loc, bools.astype(int)

def skip_nan_at_head(df, col_name):
	"""
	Cuts all rows from top of file if specificed col contains
	np.nan values until first row where the value != np.nan

	VARIABLES
	df : Pandas DataFrame
	col_name : column name to consider
	noVal : data to use to omit rows (default = np.nan)

	RETURN
	df_clipped : df with noVal rows ommited from top of file
	"""
	
	#get nan locations
	nan_loc, bools = location_of_nan(df, col_name)

	# check if first value in df (first position = 0) is nan
	first_is_nan=nan_loc.sort_values()[0]==0

	# if yes, check spacing between indicies

	if first_is_nan:
		print("first value isn't no value - skipping until next non-noVal instance...")

		# get space between index locations (of nan locations)
		spacing = np.ediff1d(nan_loc)
		#get values that are not in consequitive index locations (i.e. index spacing != 1)
		not_nextdoor= spacing[spacing!=1]#.sort()
		#get preceding index of first value present in not_nextdoor 
		#array of 1,2,3,4,5,6,10 gives 1d diffs of 1,1,1,1,1,4 (array is one shorter as it has gone, 2-1, 3-2 ... 10-6)
		ix=int(util.get_index_1d(spacing, not_nextdoor[0])[0]) # index in spacing of first non-consequitive index pair
		preceding_index=nan_loc[ix] # value in nan_loc
		# drop rows from first row until row before first row where distance !=1
		df=df.drop(df.index[0: preceding_index+1])

		return df
	
	else:
		print("first value isn't no value")
	
		return None

def skip_nan_at_tail():
	"""
	Cuts all rows from bottom of file if specificed col 
	has a value == noVal (default is np.nan) until first 
	row where value != noVal

	VARIABLES
	df : Pandas DataFrame
	col_name : column name to consider
	noVal : data to use to omit rows (default = np.nan)

	RETURN
	df_clipped : df with noVal rows ommited from bottom of file
	"""
	#get nan locations
	nan_loc, bools = location_of_nan(df, col_name, noVal)

	# check if last value in df (last position = len(df)-1) is nan
	last_is_nan=nan_loc.sort_values()[len(nan_loc)-1]==(len(df)-1)

	if last_is_nan:
		print("first value isn't no value - skipping until next non-noVal instance...")

	else:
		print("last value isn't no value")
	
		return None

#drop rows where kill value == 0

# create column called kill
	# z == NaN gives kill value of 1
	# z != NaN gives kill value of 0
# drop head if nan:
# if kill[0] is 1, drop all rows until preceding row before kill is 1
# drop tail if nan:
# if kill[len(df)-1] is 1, drop all rows until preceding row before kill is 1

pnt_test=points.copy()
pnt_dropped=pnt_test.drop(pnt_test[pnt_test.kill == 0].index)

pnt_dropped['index_current'] = pnt_dropped.index

"""
# plot indicies to identify any step changes...
indicies=pnt_dropped['index_current'].values
xs=np.arange(0,len(indicies), 1)
plt.scatter(xs, indicies), plt.title("ID where to drop points"), plt.show()
"""

# calculate differences between indicies - drop all rows including and following the 
# first difference that is not 1 (i.e. indicies are not contiguous)
pnt_dropped = pnt_dropped.assign(diffs=pd.rolling_apply(pnt_dropped['index_current'],2,lambda x: x[1]-x[0])) 
	# assign creates a new column as part of a dataframe
	# rolling_apply implements a moving function
		# as applied above, this requires the column to use, 
		# the size of the mvoing window (in this case 2) and 
		# in this case a fucntion (subtracting the preceding 
		# element from each current element)

drop_index = pnt_dropped.where(pnt_dropped['diffs'] > 1).dropna()
	# returns the index of the first element in diffs greater 
	# than 1 (implying non-contiguous indexing in this case)

if not drop_index.empty:

	pnt_dropped = pnt_dropped.loc[:drop_index.index[0]-1]
		# subsets the dataframe up to the preceding row 
		# before the index of drop_index

	#pnt_dropped_xy = pnt_dropped.drop('ix', 1)
	#pnt_dropped_xy = pnt_dropped_xy.drop('iy', 1)
	pnt_dropped_xy = pnt_dropped.drop('kill', 1)
	pnt_dropped_xy = pnt_dropped_xy.drop('index_current', 1)
	pnt_dropped_xy = pnt_dropped_xy.drop('diffs', 1)
