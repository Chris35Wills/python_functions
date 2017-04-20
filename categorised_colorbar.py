import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np

def colorbar(min_val, max_val, interval, cmap='', label='Elevation (m)', save_it=False, ofile='./TEMP_colorbr.png', dpi=300, disable_rc_overwrite=True, horizontal=True, long_side=8, short_side=3, extend_ends='both'):
	"""
	Create a colorbar for a given range - can pass in your own custom cmap (must match length of the range you are trying to map though)
	"""
	if disable_rc_overwrite:
		mpl.rcParams.update({'font.size': 22})
		hfont = {'fontname':'Calibri'}
	
	if horizontal:
		orientation='horizontal'
		fig=plt.figure(figsize=(long_side,short_side))  # horizontal
	else:	
		orientation='vertical'
		fig=plt.figure(figsize=(short_side,long_side)) # vertical

	ax=fig.add_subplot(111)

	vals=np.arange(min_val, max_val+interval, interval)
	print(vals)

	#if cmap:
	norm = mpl.colors.BoundaryNorm(vals, cmap.N)
	#if not cmap: # if cmap not set, creat vidiris cmap using vals
	#	print("cmap not provided -- using viridis")
	#	cmap=cm.viridis(vals)
	#	norm = mpl.colors.BoundaryNorm(vals, vals.shape)

	cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, 
									norm=norm, 
									spacing='uniform', 
									orientation=orientation, 
									#boundaries=([-1000] + vals + [2500]), 
									extend=extend_ends, 
									ticks=vals)
		
	cb.set_label(label, **hfont)
	if orientation == 'horizontal':
		ax.set_position((0.1, 0.45, 0.8, 0.1))
	elif orientation == 'vertical':
		cb.set_label('Elevation (m)', rotation=-90, labelpad=20)
		ax.set_position((0.45, 0.1, 0.1, 0.8))

	if save_it:
		ofile="C:/Github/Bristol_data/Bristol_data/Conferences/AGU2016/Chris_poster/ground_ice_DEM_colourbar.png"
		plt.savefig(ofile, dpi=dpi, transparent=True)
	else:
		plt.show()


def example():
	print("Creates a colorbar like this...")

	# Example
	min_val=-500
	max_val=2000
	interval=500
	label='Elevation (m)'
	cmap = mpl.colors.ListedColormap(['#2c7bb6','#0a793a','#77a353','#f1d499','#c96a33','#975114'])

	colorbar(min_val, max_val, interval, label=label, cmap=cmap, horizontal=True)	

	print("On import, can be run using the following...")
	print("min_val=-500")
	print("max_val=2000")
	print("interval=500")
	print("label='Elevation (m)'")
	print("cmap = mpl.colors.ListedColormap(['#2c7bb6','#0a793a','#77a353','#f1d499','#c96a33','#975114'])")
	print("colorbar(min_val, max_val, interval, label=label, cmap=cmap, horizontal=True)	")


if __name__ == "__main__":
	
	example()
