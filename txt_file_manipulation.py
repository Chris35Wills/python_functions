"""
txt_file_manipulation.py 

Various methods for working with txt and csv formatted files 

@author  : Chris Williams 
@date    : 14/04/16 onwards
"""

import util
import pandas as pd
import numpy as np
from astropy.time import Time

def resample_csv_file(file_in, file_out, n=2):
	"""
	Reads in a file and subsamples it by skipping every skip_every_n line

	VARIABLES

	file : a column formatted file
	n    : number of lines to skip between each line (e.g. if set to 2, keep every 2nd line)
	"""

	data=pd.read_csv(file_in, sep=',', header=0) # skip header row (and keep it as variable)
	sub_data=data.iloc[::n, :]
	
	util.check_output_dir(file_out)
	sub_data.to_csv(file_out, sep=',', index=False)

	print("Data subsampled, missing every %i lines" %(n))
	print("Output file: %s" %(file_out))


def concat2csv(in_file, out_file):
	"""
	Takes in a sopace delimited file and outputs it as a csv
	"""
	
	f=pd.read_csv(in_file, delim_whitespace=True, skiprows=0)
	np.savetxt(out_file, f, delimiter=',')


def check_date_range(data, date_column, sep_type="", skip_rows=0, date_format="jd"):
    """
    Reads in a text file containg date information and prints out the min and max years of data present.

    VARIABLES
	
    data 	 = a text file
    date_column  = the column containg time stamp information
    sep_type	 = separator type (defaults to white space delimited)
    skip_rows    = number of header rows to skip (defaults to zero)
    date_format	 = date format type (see here for types: http://docs.astropy.org/en/stable/time/#using-astropy-time)

    RETURNS

    Nothing
    """

    if sep_type=="":
        info=pd.read_csv(data, skiprows=skip_rows, header=None, delim_whitespace=True) 
    else:
        info=pd.read_csv(data, skiprows=skip_rows, header=None, sep=sep_type)

    dates=Time(info[int(date_column)].values, format=date_format)
    years=dates.byear

    print("Earliest year record: %f" %(years.min()))
    print("Latest year record: %f" %(years.max()))


def read_header(in_file, num_header_rows, sep_type =""):
    """
    Reads in the header rows of a text file.

    VARIABLES
	
    in_file	= a text file
    out_file	= an output file
    sep_type	= separator type (defaults to white space delimited)
    skip_rows   = number of header rows to skip (defaults to zero)

    RETURNS

    header (pandas dataframe object)
    """

    if sep_type=="":
        header=pd.read_csv(in_file,delim_whitespace=True, header = None, chunksize=1).read(num_header_rows)
    else:
        header=pd.read_csv(in_file, sep=sep_type, header = None, chunksize=1).read(num_header_rows)
    
    return header


def check_duplicates(in_file, sep_type="", header_rows=0):
    """
    Checks for duplicated rows in a given file.

    VARIABLES
    in_file	= a text file
    sep_type	= separator type (defaults to white space delimited)
    header_rows = number of header rows to skip (defaults to zero i.e. no header)
	
    RETURNS

    Nothing
    """

    if sep_type=="":
        data=pd.read_csv(in_file, skiprows=header_rows, header=None, delim_whitespace=True) 
    else:
        data=pd.read_csv(in_file, skiprows=header_rows, header=None, sep=sep_type)

    dup=data.duplicated(keep='first')
    dup_True=np.where(dup==True)
    len_dup_True_indx=len(dup_True[0])

    if len_dup_True_indx == 0:
	print("No duplicated rows in %s" %(in_file))
    else:	
	print("%i duplicated rows found in %s" %(len_dup_True_indx, in_file))


def strip_duplicates(in_file, out_file, sep_type="", header_rows=0):
    """
    Read in text file and output new version of the file without duplicates (retaining only the first instance).

    VARIABLES

    in_file	  = a text file
    out_file	  = an output file
    sep_type      = separator type (defaults to white space delimited)
    header_rows   = number of header rows to skip (defaults to zero i.e. no header)
	
    RETURNS

    Nothing
    """

    util.check_output_dir(out_file)

    if header_rows !=0: header=read_header(in_file, num_header_rows=header_rows, sep_type ="")

    if sep_type=="":
        data=pd.read_csv(in_file, skiprows=header_rows, header=None, delim_whitespace=True) 
    else:
        data=pd.read_csv(in_file, skiprows=header_rows, header=None, sep=sep_type)

    dup=data.duplicated(keep='first')
    dup_False=np.where(dup==False)
	
    no_dup=data.loc[dup_False]

    len_no_dup=no_dup.shape[0]
    len_dup_False_indx=len(dup_False[0])

    try:
        assert len_no_dup == len_dup_indx
    except AssertionError:
  	print("Removal of duplicates and creation of new output failed.")
	print("Length of no duplicated indices does not match the subsampled main dataframe... fucntion failiure :(")

	
    if header_rows !=0: 
 	frames = [header, no_dup]
	no_dup = pd.concat(frames)

    if sep_type=="":
	no_dup.to_csv(out_file, sep="\t", header=False, index=False)
    else:
 	no_dup.to_csv(out_file, sep=sep_type, header=False, index=False)


		
