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


# TOY DATA
"""
run="run_3"
pnt_path="C:/GitHub/synthetic_channels/FENTY_DEM_along_track_FT/%s/good_paths" %run
pnt_f='%s/densified_path_3_clipped_with_elev.csv' %pnt_path
pnts=pd.read_csv(pnt_f, sep=',')
#pnts['z_cubic'][120:]=np.nan # set nans at end
pnts['z_cubic'][0:10]=np.nan # set nans at head
pnts['z_cubic'][70:73]=np.nan # set nans at head
"""

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
	#reset index so it starts at 0	
	df = df.reset_index(drop=True)

	#get nan locations
	nan_loc, bools = location_of_nan(df, col_name)

	# check if first value in df (first position = 0) is nan
	if len(nan_loc) != 0:
		first_is_nan=nan_loc.sort_values()[0]==0

		if first_is_nan:
			print("first value is no value - removing all noVal instances at top of dataframe...")
			# get space between index locations (of nan locations)
			spacing = np.ediff1d(nan_loc)
			#get values that are not in consequitive index locations (i.e. index spacing != 1)
			not_nextdoor= spacing[spacing!=1]#.sort()
			
			#get preceding index of first value present in not_nextdoor 
			#array of 1,2,3,4,5,6,10 gives 1d diffs of 1,1,1,1,1,4 (array is one shorter as it has gone, 2-1, 3-2 ... 10-6)
			if len(not_nextdoor)!=0:
				ix=int(util.get_index_1d(spacing, not_nextdoor[0])[0]) # index in spacing of first non-consequitive index pair
				# drop rows from first row until row before first row where distance !=1
				df=df.drop(df.index[0: nan_loc[ix]+1])
			elif len(not_nextdoor)==0: # i.e. all nan indicies are consequitive
				df=df.drop(df.index[0: nan_loc[len(nan_loc)-1]])

			return df
	
		else:
			print("first value isn't no value")
			return df

	elif len(nan_loc) == 0:
		print("No nan values :)")
		return df

def skip_nan_at_tail(df, col_name):
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

	#reset index so it starts at 0
	df = df.reset_index(drop=True)

	#get nan locations
	nan_loc, bools = location_of_nan(df, col_name)

	# check if last value in df (last position = len(df)-1) is nan
	if len(nan_loc) != 0:
		last_is_nan=nan_loc.sort_values()[len(nan_loc)-1]==(len(df)-1)

		if last_is_nan:
			print("last value is no value - removing all noVal instances at end of dataframe...")
			#nan_loc=nan_loc[::-1] # flip locations (last is first)
			spacing = np.ediff1d(nan_loc) # calc index spacing
			not_nextdoor= spacing[np.abs(spacing)!=1]#.sort()

			if len(not_nextdoor)!=0:
				ix=int(util.get_index_1d(spacing, not_nextdoor[len(not_nextdoor)-1])[0]) # index in spacing of last non-consequitive index pair
				# drop rows from first row until row before first row where distance !=1
				df=df.drop(df.index[nan_loc[ix+1]: nan_loc[len(nan_loc)-1]+1]) # ix will be the index of the pair partner that is non-consequitive relative to consequitive partners e.g. 39, 40, 43, 44 << index of 40 will be returned...
			else:
				df=df.drop(df.index[nan_loc[0]: nan_loc[len(nan_loc)-1]+1]) 

			return df

		else:
			print("last value isn't no value")
		
			return df

	elif len(nan_loc) == 0:
		print("No nan values :)")
		return df

def bin_data(df, bin_width, min_bin, max_bin, column_to_bin=''):
	"""
	Bins data in dataframe accordinging to defined bins.
	Inspiration from here: http://chrisalbon.com/python/pandas_binning_data.html

	VARIABLES
	df : a pandas dataframe
	bin_width : width of each bin
	min_bin : minimum bin edge
	max_bin : maximum bin edge
	column_to_bin : column to use to sort dataframe based on defined bins

	RETURN
	df : + new columns containing category info according to the data defined by column_to_bin
	"""

	bin_width=200.
	min_bin=0
	max_bin=37400.
	column_to_bin='wavelength_m'

	bins = np.arange(0, (max_bin+bin_width), bin_width)

	# create bin names
	nummerical_names=np.arange(0, max_bin, bin_width)
	#group_names= ["%.2f" % x for x in nummerical_names]

	#string_names=[str(i) for i in nummerical_names]
	#string_names_PLUS=[str(i) for i in nummerical_names+bin_width]
	#group_names = ["%s - %s" %(x for x in string_names, y for y in string_names_PLUS)]
	group_names= ["%.2f" % x for x in nummerical_names]

	# categories specific data according to bins (applies across the row so everything is kept together)
	df['categories_str'] = pd.cut(df[column_to_bin], bins, labels=group_names)
	df['categories_int'] = pd.cut(df['wavelength_m'], bins, labels=nummerical_names)

	return df, (group_names, nummerical_names)



if __name__ == "__main__":
	print("Run from import.")