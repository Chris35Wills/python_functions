from __future__ import division

"""
FT analysis and plotting library

Various tools to assist in the calculation and plotting of FT analysis

Help with FTs can be found here:
	http://www.imagemagick.org/Usage/fourier/
	http://www.revisemri.com/tutorials/what_is_k_space/
	http://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/
	https://plot.ly/matplotlib/fft/

"""
import sys
import numpy as np
import matplotlib.pyplot as plt

#############
# Quick tests

# easy test to write: result of conversion from k space to x space MUST be <= half of the maximum input distance

def test_space_space_wavelength(sample_spacing, min_xf_space_space):
	"""
	For conversion of k space back to space space, the minimum converted value (min_xf_space_space) 
	cannot be less than the initial sample spacing.

	VARIABLES
	min_xf_space_space
	sample_spacing
	"""

	print("What I can see...")
	print("Sample spacing: %f (float)" %np.around(sample_spacing, decimals=2))
	print("Min xf spacing (space space): %f (float)" %(np.round(min_xf_space_space, decimals=2)))

	try:
		print("Asserting whether min_xf_space_space (%f) >= sample_spacing (%f)" %(np.round(min_xf_space_space, decimals=2), np.around(sample_spacing, decimals=2)))
		assert np.round(min_xf_space_space, decimals=2) >= np.round(sample_spacing, decimals=2)
	except AssertionError:
		print("Yikes!")
		print("Sample spacing: %f" %np.round(sample_spacing, decimals=2))
		print("Min xf spacing (space space): %f" %np.round(min_xf_space_space, decimals=2))
		sys.exit("Sample spacing is greater than k value converted back to space space ")

def test_length_equality(x,y):
	"""Assertion test of the length of 2 arrays"""
	try:
		assert len(x) == len(y)
	except AssertionError:
		print("Length of x: %i" %len(x))
		print("Length of y: %i" %len(y))
		sys.exit("x and y vectors are of different length")

################
# Main functions

# <<<<<<<<<<<<<<<< replace with np.fft.rfftfrq # rfftfrq only gives the positive half of the frequencies as oposed to fftfrq
# <<<<<<<<<<<<<<<< np.fft.rfft will give the correspondoing half of the fft amplitudes (np.fft.fft gives you both halves but you only want one side)
# <<<<<<<<<<<<<<<< getting back to real space is still calculated correctly using: (1/k)/2
def map_k_from_x(x, sample_spacing, return_x_units=False, n=''):
	"""
	Maps k in frequency space from x in space space.

	Units of k will be 1/whatever units x is provided in (and halved as code caters for Nyquist frequency)

	x might be your incremental sample spacing or pixel position or fid or...

	CONFUSED??? Look at this: http://www.revisemri.com/tutorials/what_is_k_space/

	VARIABLES

	x       		: array of x in space space (e.g. cumulative sample spacing)
	spacing 		: spacing between elements (in space space)
	return_x_units	: if True, returns an additional vecor of k in units of x	
	n               : number of elements to be created in xf - if not set, 
					  creates len(x)/2 elements
	
	RETURN

	xf
	xf_units (if return_x_units == True)* 

	*if plotting an ft against xf_units, the x axis will have the shortest 
	wavelengths (highest frequencies) closest to the origin)
	"""
	
	# if no number of elements set, just take half of the length of x (the Nyqvist frequency)
	if n == '': 
		N=len(x)
		#xf = np.linspace(x_min, 1.0/(2.0*sample_spacing), N/2) # start vector at x_min - defaults to 0 if not set
		#xf = np.linspace(x[0], 1.0/(2.0*sample_spacing), N/2)  # start vector at first element of x
		xf = np.linspace(0.0, 1.0/(2.0*sample_spacing), N/2)    # << THIS IS A ONE WAY FREQUENCY RANGE
		#xf = np.linspace(0.0, 1.0/(2.0*sample_spacing), N)     # << THIS IS A TWO WAY FREQUENCY RANGE
		
	# if a number of elements set (n), create n elements in xf
	else:
		xf = np.linspace(0.0, 1.0/(2.0*sample_spacing), n)  # start vector at 0
		#xf = np.linspace(x[0], 1.0/(2.0*sample_spacing), n) # start vector at first element of x
		#xf = np.linspace(x_min, 1.0/(2.0*sample_spacing), n) # 1/2*sample_spacing is used to convert from 
														   # space space to k space, cutting off at the 
														   # nyquist frequency which has a value of half the input points
		
	if not return_x_units:
		#print("Just returning linearly spaced array in frequency units (1/x units)")
		return xf

	elif return_x_units:
		
		#print("Returning linearly spaced array in frequency units (1/x units) and space space units (units of input x vector)")
		xf_units=(1/xf)/2 # 1/2*sample_spacing is used to convert from space space to k space, cutting off at the 
						  # nyquist frequency which has a value of half the input points
		return xf, xf_xunits

def frequency_plot(fft_1d_snip, ax, skip_first_value=True, x_label="", y_label="", log=False):
	"""
	Plots a 1d FFT (pass in the absolute number rather than real+imaginery pair)

	VARIABLES

	skip_first_value : set to True to ignore the 0 wavelength value (which is just noise)
	
	RETURN
	
	x_label
	y_label
	plot_type
	ax
	"""
	if x_label == "": x_label = 'Index position'
	if y_label == "": y_label = 'Magnitude'
	plot_type = "frequency_space"
	
	if skip_first_value: 
		x=np.linspace(1, len(fft_1d_snip[1:]), len(fft_1d_snip[1:]))
		y=fft_1d_snip[1:]

		test_length_equality(x,y)

		if log:
			ax.plot(x,np.log(y)) 
		elif not log:
			ax.plot(x,y) 

		ax.set_xlim(0, len(fft_1d_snip[1:])+1) # removed as diff length...

	else: 
		ax.plot(fft_1d_snip) 
		ax.set_xlim(0, len(fft_1d_snip[1:])+1)
	
	return x_label, y_label, plot_type, ax
	

#<<<<<<<<<< plt.loglog   to replace
#<<<<<<<<<< plt.semilogx to replace
def plot_ft_against_frq_space(fft_1d_clip, x_clip, sample_spacing,n='', ax='', log=False, log_log=False):
	"""
	Plots the results of an ft in frequency space (1/units of original input (x)) (FREQUENCY space)

	e.g.

	x is 500 m -> 5000 m   (perhaps distance along a transect)
	y is -1000 m -> +200 m (perhaps bathymetric elevation)

	your plot will be log(FT mgnitude) vs wavelength in m

	Remember, if you have x/y data where x is 500 m - 5000 m and y is -1000m - +200m, 
	your FT v swavelength (m) plot will start at your step size and not at the min value 
	of your input x axis as it illustrates wavelengths in x units, not location! This may 
	seem basic, but I spent 3 hours trying to get my head around that.

	VARIABLES
	fft_1d_clip      : absolute component of an ft - must be same length as x_clip
	x_clip           : x axis - such as distance along a transect
	sample_spacing   : sample spacing between x axis values
	ax               : axis object - if none passed, function just shows plot
	log 			 : if True displays log magnitude
	log_log 		 : if True displays log magnitude (y) and log frequency (x) - this 
					   can be useful for identifying power laws from detrended data (to 
					   do this, plot a linear trend to the data if appropriate and consider 
					   the gradient - make sure to consider the strength of your trend though 
					   - maybe there isn;t even one there!!)

	RETURN

	if ax_mod = True:
		ax object
		xf vector    NOT LOG (units of 1/input x units - this will be one element less than the input fft_1d_clip vector as the first value is ignored)
	if ax_mod = False:
		xf vector    NOT LOG (units of 1/input x units - this will be one element less than the input fft_1d_clip vector as the first value is ignored)
	"""

	test_length_equality(fft_1d_clip, x_clip)

	if ax == '':
		ax_mod=False
		print("No axis object passed so creating figure")
		fig=plt.figure()
		ax=fig.add_subplot(111)
	else:
		ax_mod=True
		print("Axis object passed so modifying object")

	# calculate k from x 	
	xf = map_k_from_x(x_clip, sample_spacing)

	# only consider half of fft <<< 
	fft_1d_clip=fft_1d_clip[:len(fft_1d_clip)/2] #<< THIS IS A ONE WAY FREQUENCY RANGE
	#fft_1d_clip=fft_1d_clip[:len(fft_1d_clip)] #<< THIS IS A TWO WAY FREQUENCY RANGE (xf must also be two range frequency if you use this)
	
	test_length_equality(fft_1d_clip, xf)

	#plot ft against frequency (1/m)
	#ax2.plot(xf, np.log(fft_1d[:len(fft_1d)/2]))
	if log and not log_log:
		print("Logging the magnitude (y axis)")
		ax.plot(xf[1:], np.log(fft_1d_clip)[1:])
		ax.set_xlabel("Frequency (1/m)")
		ax.set_ylabel("log(Magnitude)")
	elif log_log or (log_log and log):
		print("Logging the magnitude (y axis) and frequency (x axis)")
		ax.plot(np.log(xf[1:]), np.log(fft_1d_clip)[1:])
		ax.set_xlabel("log(Frequency (1/m))")
		ax.set_ylabel("log(Magnitude)")
	elif not log and not log_log:
		print("Not logging either axis")
		ax.plot(xf[1:], fft_1d_clip[1:])
		ax.set_xlabel("Frequency (1/m)")
		ax.set_ylabel("Magnitude")

	if ax_mod:
		print("Axis object passed so returning axis object")
		return ax, xf[1:]
	else:
		print("No axis object passed so should plot image")
		plt.show()
		return xf[1:]


def plot_ft_against_frq_space_space(fft_1d_clip, x_clip, sample_spacing, ax='', log=False):
	"""
	Plots the results of an ft in the units of the original input (x) data (SPACE space)

	Based on a k scale calculated using map_k_from_x, x is converted back from the frequency 
	domian using (1/k)/2

	e.g.

	x is 500 m -> 5000 m   (perhaps distance along a transect)
	y is -1000 m -> +200 m (perhaps bathymetric elevation)

	your plot will be log(FT mgnitude) vs wavelength in m

	Remember, if you have x/y data where x is 500 m - 5000 m and y is -1000m - +200m, 
	your FT v swavelength (m) plot will start at your step size and not at the min value 
	of your input x axis as it illustrates wavelengths in x units, not location! This may 
	seem basic, but I spent 3 hours trying to get my head around that.

	VARIABLES
	fft_1d_clip      : absolute component of an ft - must be same length as x_clip
	x_clip           : x axis - such as distance along a transect
	sample_spacing   : sample spacing between x axis values
	ax               : axis object - if none passed, function just shows plot

	RETURN
	if ax_mod = True:
		ax object
		xf_m vector   NOT LOG (units of m (or whatever x was originally supplied in) - this will be one element less than the input fft_1d_clip vector as the first value is ignored)
	if ax_mod = False:
		xf_m vector   NOT LOG (units of m (or whatever x was originally supplied in) - this will be one element less than the input fft_1d_clip vector as the first value is ignored)
	"""

	test_length_equality(fft_1d_clip, x_clip)

	if ax == '':
		ax_mod=False
		print("No axis object passed so creating figure")
		fig=plt.figure()
		ax=fig.add_subplot(111)
	else:
		ax_mod=True
		print("Axis object passed so modifying object")

	# calculate k from x 	
	#xf = map_k_from_x(x_clip, sample_spacing, n=len(x_clip))
	xf = map_k_from_x(x_clip, sample_spacing)
	
	#plot ft against frequency (1/m)
	########## CONVERT WAVELENGTHS TO METRES ################
	xf_m=1/xf[1:]       # <<< 1/xf gives wavelength in metres
						# <<< The first value of 1/xf will be nan or 
						# infinity as 0 wavelengths have no length 
						# and 1/0 is infinity! Therefore, ignore value [0]
						# hence only considering elements [1:]

	#print("Just before min test")
	#print("Sample spacing: %f" %sample_spacing)
	#print("Min xf spacing (space space): %f" %min(xf_m/2))

	test_space_space_wavelength(sample_spacing, min(xf_m/2))

	# only consider half of fft <<< 
	fft_1d_clip=fft_1d_clip[1:len(fft_1d_clip)/2] #<< THIS IS A ONE WAY FREQUENCY RANGE
	#fft_1d_clip=fft_1d_clip[:len(fft_1d_clip)] #<< THIS IS A TWO WAY FREQUENCY RANGE (xf must also be two range frequency if you use this)
	
	test_length_equality(fft_1d_clip, xf_m)

	if log:
		ax.plot((xf_m/2), np.log(fft_1d_clip))   # map_k_from_x considers the nyquist frency which divides by a factor of 2, so k to x 
		ax.set_xlabel("Wavelength (m)")
		ax.set_ylabel("log(Magnitude)")												 # space is (1/k) / 2 (otheriwse your new max xf_m value will be twice as big as your max input x_clip value)

	elif not log:
		ax.plot((xf_m/2), fft_1d_clip)   # map_k_from_x considers the nyquist frency which divides by a factor of 2, so k to x 
										 # space is (1/k) / 2 (otheriwse your new max xf_m value will be twice as big as your max input x_clip value)
	
		ax.set_xlabel("Wavelength (m)")
		ax.set_ylabel("Magnitude")

	if ax_mod:
		print("Axis object passed so returning axis object")
		return ax, xf_m/2
	else:
		print("No axis object passed so should plot image")
		plt.show()
		return xf_m/2


def plot_ft_different_x_scales(fft_1d_clip, x_clip, sample_spacing,n=''):
	"""
	Plots results of ft against different x axis

	plot 1: ft magnitude vs ft value index (from ft vector)
	plot 2: ft magnitude vs frequency (1/units of x)
	plot 3: ft magnitude vs wavelength (units of x OR 1/frequency)

	VARIABLES
	
	fft_1d_clip      : a 1d FT vector (absolute value not real/imaginery pair) perhaps clipped to highligh certain values (e.g. first 20)
	x_clip           : an x axis vector - perhaps cumulative distance of ovbservations - perhaps clipped to highligh certain values (e.g. first 20)
	sample_spacing   : sample spacing of elements of x
	n 				 : number of elements to be in the linspace x vector (must be same length as the input x_clip or fft_1d_clip arrays)

	RETURN 

	Nothing
	"""

	test_length_equality(fft_1d_clip,x_clip)

	if n == '':
		n=len(x_clip)
	
	fft_1d_clip, x_clip, sample_spacing

	fig=plt.figure()
	ax1=fig.add_subplot(411)
	ax2=fig.add_subplot(412)
	ax3=fig.add_subplot(413)
	ax4=fig.add_subplot(414)

	_, _, _, ax1 = frequency_plot(fft_1d_clip, ax1, x_label="Index", y_label="log(Magnitude)", log=True)
		
	ax2 = plot_ft_against_frq_space(fft_1d_clip, x_clip, sample_spacing, ax=ax2, log=True)

	ax3 = plot_ft_against_frq_space(fft_1d_clip, x_clip, sample_spacing, ax=ax3, log=True, log_log=True)

	ax4 = plot_ft_against_frq_space_space(fft_1d_clip, x_clip, sample_spacing, ax=ax4, log=True)

	

	plt.show()


def plot_input_AND_ft_space_space(z_clip, fft_1d_clip, x_clip, sample_spacing):
	"""
	Plots results of ft against wavelength (space space i.e. units of input x axis) as well as a plot of the original z data (space space) for comparison

	plot 1: z vs x (space space units e.g. metres)
	plot 2: ft magnitude vs wavelength (units of x OR 1/frequency)

	VARIABLES

	z_clip           : 'raw' z data (clipped to same indicies as the fft_1d_clip and x_clip arrays)
	fft_1d_clip      : a 1d FT vector (absolute value not real/imaginery pair) perhaps clipped to highligh certain values (e.g. first 20)
	x_clip           : an x axis vector - perhaps cumulative distance of ovbservations - perhaps clipped to highligh certain values (e.g. first 20)
	sample_spacing   : sample spacing of elements of x

	RETURN 

	Nothing
	"""

	fig=plt.figure()
	ax1=fig.add_subplot(211)
	ax2=fig.add_subplot(212)

	ax1.plot(x_clip, z_clip)
	ax1.set_xlabel("Distance along transect (m)") ## pass in title as option - default is x
	ax1.set_ylabel("Bathymetric elevation (m a.s.l.)") ## pass in title as option - default is y
	ax1.set_title("Fjord centreline elevation transect") ## pass in title as option - default is nothing 

	ax2, _ =plot_ft_against_frq_space_space(fft_1d_clip, x_clip, sample_spacing, ax=ax2)
	ax2.set_xlabel("Wavelength (m)")
	ax2.set_ylabel("log(Magnitude)")
	ax2.set_title("Fjord FT: log(magnitude) vs wavelength(m)") ## pass in title as option - default is nothing 
	
	plt.show()


def plot_input_AND_ft_space(z_clip, fft_1d_clip, x_clip, sample_spacing):
	"""
	Plots results of ft against wavelength (space space i.e. units of input x axis) as well as a plot of the original z data (space space) for comparison

	plot 1: z vs x (space space units e.g. metres)
	plot 2: ft magnitude vs wavelength (units of x OR 1/frequency)

	VARIABLES

	z_clip           : 'raw' z data (clipped to same indicies as the fft_1d_clip and x_clip arrays)
	fft_1d_clip      : a 1d FT vector (absolute value not real/imaginery pair) perhaps clipped to highligh certain values (e.g. first 20)
	x_clip           : an x axis vector - perhaps cumulative distance of ovbservations - perhaps clipped to highligh certain values (e.g. first 20)
	sample_spacing   : sample spacing of elements of x

	RETURN 

	Nothing
	"""

	fig=plt.figure()
	ax1=fig.add_subplot(211)
	ax2=fig.add_subplot(212)

	ax1.plot(x_clip, z_clip)
	ax1.set_xlabel("Distance along transect (m)") ## pass in title as option - default is x
	ax1.set_ylabel("Bathymetric elevation (m a.s.l.)") ## pass in title as option - default is y
	ax1.set_title("Fjord centreline elevation transect") ## pass in title as option - default is nothing 

	ax2=plot_ft_against_frq_space(fft_1d_clip, x_clip, sample_spacing, ax=ax2)
	ax2.set_xlabel("Wavelength (1/m)")
	ax2.set_ylabel("log(Magnitude)")
	ax2.set_title("Fjord FT: log(magnitude) vs wavelength(m)") ## pass in title as option - default is nothing 
	
	plt.show()


"""
# plot wavelengths (nb/  in pixels)
def wavelength_plot (wavelengths,fft_1d_snip):
	x_label = 'Wavelength'
	y_label = 'Magnitude'
	plot_type = "freq_vs_wavelengths"
	ax.plot(wavelengths,fft_1d_snip) 
	return x_label, y_label, plot_type, ax
	
def magnitude_metres(fft_1d_snip, array_length):
	mag_m = fft_1d_snip/math.sqrt(array_length)
	return mag_m
	
def wavelength_metres(pixel_size, wavelengths):
	wavelength_m = wavelengths*pixel_size
	return wavelength_m

def FFT_plot(site, ax, transect_number, plot_type, output_path, x_label, y_label, magnitude_units='px', wavelength_units='px'):
	#plt.clf()
	time_stamp = strftime("%H.%M.%S")
	name = "%s_transect_%i_%s_%s.pdf" %(site, transect_number, plot_type, time_stamp) 
	#ax.set_title("Helheim_transect_%i_FFT" %(transect_number))
	output_name = "%s/%s" %(output_path, name)
	plt.xlabel("%s (%s)" %(x_label, wavelength_units))
	plt.ylabel("%s (%s)" %(y_label, magnitude_units))
	#plt.savefig(output_name) 
	plt.show()
"""

if __name__ == "__main__":

	#some toy data
	dist = np.array([  0.00000000e+00,   2.11111116e+02,   2.11111110e+02, 2.11111110e+02,   2.11111110e+02,   2.11111110e+02,
	         2.11111117e+02,   2.11111110e+02,   2.11111110e+02, 2.11111110e+02,   2.11111110e+02,   2.11111110e+02,
	         2.11111117e+02,   2.11111110e+02,   2.11111110e+02, 2.11111110e+02,   2.00000003e+02,   2.11111107e+02,
	         2.11111115e+02,   2.11111107e+02,   2.11111115e+02, 2.11111107e+02,   2.11111115e+02,   2.11111107e+02,
	         2.11111115e+02,   2.11111107e+02,   2.11111115e+02, 2.11111107e+02,   2.11111115e+02,   2.11111107e+02,
	         2.11111115e+02,   2.11111107e+02,   2.11111115e+02, 2.11111107e+02,   2.11111115e+02,   2.00000002e+02,
	         2.10526312e+02,   2.10526319e+02,   2.10526312e+02, 2.10526319e+02,   2.10526319e+02,   2.10526312e+02,
	         2.10526319e+02,   2.10526312e+02,   2.10526319e+02, 2.10526312e+02,   2.10526319e+02,   2.10526312e+02,
	         2.10526319e+02,   2.10526312e+02,   2.10526319e+02, 2.10526319e+02,   2.10526312e+02,   2.10526319e+02,
	         2.10526312e+02,   2.11111113e+02,   2.11111108e+02, 2.11111114e+02,   2.11111108e+02,   2.11111113e+02,
	         2.11111108e+02,   2.11111114e+02,   2.11111113e+02, 2.11111108e+02,   2.11111113e+02,   2.11111109e+02,
	         2.11111113e+02,   2.11111108e+02,   2.11111113e+02, 2.11111109e+02,   2.11111113e+02,   2.11111113e+02,
	         2.11111108e+02,   2.00000000e+02,   2.10526316e+02, 2.10526316e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526315e+02, 1.00006582e-06,   2.11111111e+02,   2.11111112e+02,
	         2.11111111e+02,   2.11111111e+02,   2.11111111e+02, 2.11111112e+02,   2.11111111e+02,   2.11111111e+02,
	         2.11111112e+02,   2.11111111e+02,   2.11111111e+02, 2.11111110e+02,   2.11111112e+02,   2.11111111e+02,
	         2.11111111e+02,   2.11111112e+02,   2.11111111e+02, 2.11111111e+02,   2.00000000e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526315e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526315e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526315e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526315e+02,   1.00000761e-06,   2.11111112e+02, 2.11111110e+02,   2.11111112e+02,   2.11111113e+02,
	         2.11111109e+02,   2.11111113e+02,   2.11111109e+02, 2.11111113e+02,   2.11111112e+02,   2.11111109e+02,
	         2.11111113e+02,   2.11111109e+02,   2.11111113e+02, 2.11111112e+02,   2.11111110e+02,   2.11111112e+02,
	         2.11111110e+02,   2.11111112e+02,   2.00000000e+02, 2.10526316e+02,   2.10526316e+02,   2.10526315e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526315e+02, 2.10526316e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526315e+02,   2.10526316e+02, 2.10526316e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526315e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526316e+02,   2.10526315e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526315e+02, 2.10526316e+02,   2.10526316e+02,   2.11111111e+02,
	         2.11111112e+02,   2.11111111e+02,   2.11111111e+02, 2.11111111e+02,   2.11111112e+02,   2.11111111e+02,
	         2.11111111e+02,   2.11111112e+02,   2.11111111e+02, 2.11111110e+02,   2.11111111e+02,   2.11111112e+02,
	         2.11111111e+02,   2.11111111e+02,   2.11111112e+02, 2.11111111e+02,   2.11111111e+02,   2.00000000e+02,
	         2.10526316e+02,   2.10526315e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526315e+02,
	         2.10526316e+02,   2.10526315e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526315e+02,
	         2.10526316e+02,   2.10526315e+02,   2.10526316e+02, 2.10526315e+02,   2.10526316e+02,   2.10526316e+02,
	         2.10526315e+02,   9.99891199e-07,   2.11111111e+02, 2.11111112e+02,   2.11111111e+02,   2.11111111e+02,
	         2.11111111e+02,   2.11111112e+02,   2.11111110e+02, 2.11111111e+02,   2.11111112e+02,   2.11111111e+02,
	         2.11111111e+02,   2.11111111e+02,   2.11111112e+02, 2.11111111e+02,   2.11111111e+02,   2.11111112e+02,
	         2.11111111e+02,   2.11111111e+02,   2.00000000e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526316e+02,   2.10526315e+02,   2.10526316e+02,
	         2.10526316e+02,   2.10526316e+02,   2.10526316e+02, 2.10526315e+02,   1.00000761e-06,   2.10526314e+02,
	         2.10526314e+02,   2.10526315e+02,   2.10526318e+02, 2.10526314e+02,   2.10526314e+02,   2.10526318e+02,
	         2.10526315e+02,   2.10526314e+02,   2.10526318e+02, 2.10526314e+02,   2.10526314e+02,   2.10526319e+02,
	         2.10526314e+02,   2.10526314e+02,   2.10526318e+02, 2.10526314e+02,   2.10526315e+02,   2.10526318e+02,
	         2.11111109e+02,   2.11111113e+02,   2.11111112e+02, 2.11111110e+02,   2.11111112e+02,   2.11111110e+02,
	         2.11111112e+02,   2.11111113e+02,   2.11111109e+02, 2.11111112e+02,   2.11111110e+02,   2.11111112e+02,
	         2.11111113e+02,   2.11111109e+02,   2.11111113e+02, 2.11111109e+02,   2.11111113e+02,   2.11111112e+02,
	         2.00000000e+02,   2.10526314e+02,   2.10526314e+02, 2.10526319e+02,   2.10526314e+02,   2.10526314e+02,
	         2.10526318e+02,   2.10526314e+02,   2.10526315e+02, 2.10526314e+02,   2.10526318e+02,   2.10526314e+02,
	         2.10526314e+02,   2.10526319e+02,   2.10526314e+02, 2.10526314e+02,   2.10526318e+02,   2.10526314e+02,
	         2.10526315e+02,   2.10526318e+02,   2.11111110e+02, 2.11111109e+02,   2.11111114e+02,   2.11111110e+02,
	         2.11111113e+02,   2.11111110e+02,   2.11111114e+02, 2.11111109e+02,   2.11111114e+02])
	z = np.array([ -804.09002686,  -827.23999023,  -801.48999023,  -745.77001953, -700.60998535,  -700.09997559,  -647.23999023,  -583.92999268,
	        -594.27001953,  -611.92999268,  -726.28997803,  -777.10998535, -811.44000244,  -846.69000244,  -859.51000977,  -879.89001465,
	        -900.76000977,  -910.22998047,  -924.64001465,  -917.85998535, -920.35998535,  -948.20001221,  -937.84997559,  -967.65997314,
	        -969.2800293 ,  -965.10998535,  -979.38000488,  -999.58001709, -1006.58001709, -1006.83001709, -1011.59002686, -1019.5       ,
	       -1025.01000977, -1026.81994629, -1034.72998047, -1037.91003418, -1042.70996094, -1052.31994629, -1053.90002441, -1056.72998047,
	       -1058.45996094, -1059.33996582, -1062.0300293 , -1065.38000488, -1065.38000488, -1070.5       , -1070.54003906, -1074.81005859,
	       -1076.36999512, -1082.86999512, -1085.13000488, -1086.81994629, -1087.98999023, -1089.93005371, -1090.45996094, -1091.09997559,
	       -1091.80004883, -1092.36999512, -1095.36999512, -1099.18005371, -1101.55004883, -1104.19995117, -1107.41003418, -1109.14001465,
	       -1109.81005859, -1111.93005371, -1113.13000488, -1114.26000977, -1116.38000488, -1116.59997559, -1116.88000488, -1117.68994141,
	       -1118.35998535, -1118.2199707 , -1119.73999023, -1121.95996094, -1122.56005859, -1122.        , -1121.65002441, -1121.26000977,
	       -1121.65002441, -1121.05004883, -1120.86999512, -1120.86999512, -1119.48999023, -1120.55004883, -1114.90002441, -1115.56994629,
	       -1113.63000488, -1116.44995117, -1115.56994629, -1115.01000977, -1113.31005859, -1113.31005859, -1108.32995605, -1109.25      ,
	       -1104.76000977, -1103.69995117, -1104.08996582, -1103.63000488, -1102.85998535, -1106.        , -1107.93994141, -1109.2800293 ,
	       -1083.64001465, -1097.94995117, -1094.56005859, -1112.18005371, -1110.93994141, -1099.40002441, -1085.33996582, -1084.73999023,
	       -1067.5       , -1002.34002686,  -979.23999023, -1024.31005859, -1096.25      , -1113.44995117, -1121.2199707 , -1121.2199707 ,
	       -1120.52001953, -1115.29003906, -1005.40997314, -1090.84997559, -1109.45996094, -1123.41003418, -1120.22998047, -1117.93994141,
	       -1125.5300293 , -1128.18005371, -1128.95996094, -1130.85998535, -1128.5       , -1126.47998047, -1104.97998047, -1125.2800293 ,
	       -1111.02001953, -1117.68994141, -1097.20996094, -1093.35998535, -1069.61999512, -1042.81005859, -1013.82000732,  -960.59002686,
	        -940.03997803,  -958.29998779,  -954.79998779,  -895.25      , -888.60998535,  -884.13000488,  -933.42999268,  -933.42999268,
	        -986.86999512, -1041.60998535, -1060.68994141, -1097.06005859, -1118.89001465, -1124.05004883, -1123.80004883, -1123.80004883,
	       -1087.31994629, -1035.40002441, -1050.57995605,  -975.25      , -830.65997314,  -787.98999023,  -769.40997314,  -738.40002441,
	        -721.40997314,  -710.17999268,  -712.65997314,  -752.34997559, -794.23999023,  -850.40002441,  -867.88000488,  -903.15997314,
	        -934.        ,  -936.11999512,  -966.14001465, -1014.34997559, -1122.2800293 , -1125.81994629, -1132.22998047, -1130.11999512,
	       -1131.32995605, -1120.59997559, -1104.42004395, -1074.93005371, -974.19000244,  -962.07000732,  -847.88000488,  -752.76000977,
	        -684.02001953,  -645.32000732,  -619.59002686,  -611.05999756, -605.14001465,  -564.48999023,  -539.72998047,  -516.80999756,
	        -561.07000732,  -598.67999268,  -654.38000488,  -751.7199707 , -706.26000977,  -663.80999756,  -699.27001953,  -768.34997559,
	        -762.5300293 ,  -748.01000977,  -773.19000244,  -794.23999023, -824.04998779,  -824.04998779,  -827.76000977,  -827.76000977,
	        -824.11798096,  -818.54888916,  -811.40740967,  -803.04815674, -793.82574463,  -784.09484863,  -774.21002197,  -762.04998779,
	        -745.54998779,  -734.23999023,  -692.03997803,  -699.08001709, -709.2199707 ,  -710.15002441,  -718.61999512,  -704.45001221,
	        -706.51000977,  -703.64001465,  -722.64001465,  -703.08001709, -689.96002197,  -675.5       ,  -655.59002686,  -630.59997559,
	        -584.07000732,  -523.94000244,  -498.16000366,  -485.17001343, -500.42999268,  -484.04000854,  -481.1499939 ,  -481.1499939 ,
	        -473.22000122,  -464.69000244,  -444.82998657,  -420.20001221, -429.42001343,  -439.1000061 ,  -436.6000061 ,  -440.97000122,
	        -436.54998779,  -432.76998901,  -427.23999023,  -424.79998779, -407.89001465,  -414.83999634,  -412.95001221,  -400.47000122,
	        -384.        ,  -374.26998901,  -383.67001343,  -393.84851074, -399.45742798,  -400.84213257,  -398.34799194,  -392.32037353,
	        -383.10467529,  -371.04623413,  -356.490448  ,  -339.78268433, -321.26828003,  -301.29266357,  -280.20120239,  -258.3392334 ,
	        -236.05212402,  -213.68528748,  -191.58407593,  -170.09384155, -149.55999756,  -134.53999329,  -134.53999329,  -136.52000427,
	        -161.27999878,  -151.16999817,  -175.6000061 ,  -207.99887085, -234.94364929,  -256.32974243,  -272.05258179,  -282.00759888,
	        -286.09020996,  -284.19586182,  -276.22000122,  -265.54000854, -263.33999634,  -264.20001221,  -274.57000732,  -295.32000732,
	        -298.48999023,  -300.89001465,  -318.22000122,  -333.48001099, -337.89001465,  -373.08999634,  -389.11999512,  -413.04000854,
	        -425.26000977,  -427.73999023,  -434.58999634,  -442.77209473, -450.61578369,  -458.06750488,  -465.07376099,  -471.58105469,
	        -477.53582764,  -482.88464356,  -487.57391357,  -491.55014038, -494.75982666,  -497.1494751 ,  -498.66552734,  -499.25448608,
	        -498.862854  ,  -497.43710327,  -494.92373657,  -491.26919556, -486.42001343,  -480.25      ,  -476.54000854,  -484.86999512,
	        -485.73001099,  -485.45001221,  -484.20001221,  -484.63000488, -483.17999268,  -486.45001221,  -494.10998535,  -501.85205078,
	        -514.07159424,  -518.21063232,  -520.8102417 ,  -521.70117188, -520.7142334 ,  -517.68023682,  -512.42999268,  -506.94000244,
	        -512.15002441]) 

	#ignore any points where spacings are < a threshold
	z    = z[dist>50]
	dist = dist[dist>50]

	sample_spacing= np.mean(dist)
	dist=dist.cumsum() # cumulative distance 
	dist=dist-dist[0] # subtracts first index from cumulative sum - first index should be 0m

	plt.plot(z), plt.title('Bathymetry data slice (m)'), plt.show() # negative elevations -> bathymetry data
	plt.plot(dist), plt.title('Cumulative distance'), plt.show() # negative elevations -> bathymetry data

	# calculate ft
	fft_1d = np.absolute(np.fft.fft(z))

	# clip ft and x axis (dist which is in metres) to a range of interest
	fft_1d_clip=fft_1d[0:20]
	x_clip=dist[0:20]    # as spacing is ~200m, 0:20 will be the first 4000m
	z_clip=z[0:20]

	print("Max distance: %i" %x_clip.max())
	
	# plot the ft using different x axis
	#plot_ft_different_x_scales(fft_1d_clip, x_clip, sample_spacing)
	plot_input_AND_ft_space_space(z_clip, fft_1d_clip, x_clip, sample_spacing)
	#plot_input_AND_ft_space(z_clip, fft_1d_clip, x_clip, sample_spacing)
	#plot_ft_against_frq_space(fft_1d_clip, x_clip, sample_spacing, log=True, log_log=True) ## log log plots allow id of linear regions - linear regions imply no one wavelength dominates - try and get the slope of the linear region (kind of like a weighting factor)
