"""
Functions to deal with dates
"""

__author__ = "Chris Wiliams"
__email__ = "chris.neil.wills@gmail.com"
__date__ = "20th October 2016"
__version__ = "1.0"

try:
	time.Time()
except NameError:
	from astropy import time
except ImportError:
	sys.exit("You need to install the astropy module")



def change_date_format(date_arr, input_format="jd", output_format="iso"):
	"""
	Takes in an array of dates (default: julian day) and retunrs them in a different format (default: TimeISO)

	Date formats are as for astropy.time: http://docs.astropy.org/en/stable/time/#using-astropy-time

	e.g. default 

		2451544.5 --> 2000-01-01 00:00:00.000

	e.g.

	dates=time_jd_to_timeISO(df['date'].values)
	"""

	# add check to see if date array is actually dates!

	t=time.Time(date_arr, format=input_format)
	t.format=output_format
	
	return t # returns a Time object



if __name__ == "__main__":
	print("Run date_format from import")