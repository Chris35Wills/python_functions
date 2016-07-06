import os
import sys
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import pandas as pd
from scipy import ndimage

import util


def get_density_xyz(density_xyz_file):
	sep='\t'
	f = open(density_xyz_file, 'r')
	df = pd.read_csv(f, sep=sep, names=[ 'xx', 'yy', 'zz' ], header=0)
	xx = df['xx']
	yy = df['yy']
	zz = df['zz']

	### Get a list
	## xx_list = xx.tolist()
	## Pandas df to array
	xx = xx.values
	yy = yy.values
	zz = zz.values
	return xx, yy, zz


def get_points_xy_resamp(points_xy_file, sep=','):
	points = open(points_xy_file, 'r')
	df_points = pd.read_csv(points, sep=sep, names=[ 'xx_points', 'yy_points'], header=None)
	pnt_xx = df_points['xx_points']
	pnt_yy = df_points['yy_points']
	
	pnt_xx = pnt_xx.values
	pnt_yy = pnt_yy.values

	resamp_pnt_xx = pnt_xx[0::5000]
	resamp_pnt_yy = pnt_yy[0::5000]

	return resamp_pnt_xx, resamp_pnt_yy
	#return resamp_pnt_xx, resamp_pnt_yy, points, df_points, pnt_xx, pnt_yy


def grid_log_density(xx,yy,zz):
	xi = np.linspace(min(xx), max(xx))
	yi = np.linspace(min(yy), max(yy))
	X, Y = np.meshgrid(xi, yi)
	zz_log = np.log(zz)
	Z_log = ml.griddata(xx, yy, zz_log, xi, yi, interp='linear')
	
	return Z_log


   
def smooth_density_surface_points(Z_log, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr, density_to_nan_limit=-40):

	extent = (resamp_pnt_xx.min(), resamp_pnt_xx.max(), resamp_pnt_yy.min(), resamp_pnt_yy.max())
	
	#sys.exit("check inputs")
	#plt.figure()

	smooth = ndimage.filters.gaussian_filter(Z_log, sigma=1.0, order=0, mode='reflect')
	smooth[smooth<=density_to_nan_limit] = np.nan
	
	plt.imshow(smooth, origin='lower', extent=extent)
	plt.set_cmap('cool')
	plt.colorbar()
	plt.scatter(resamp_pnt_xx, resamp_pnt_yy, marker='+')

	file_opath = "%s/contour_input_points_SMOOTH_DENSITY_INPUT_POINTS_%s.png" %(opath_no_file, itr) 
	util.check_output_dir(file_opath)	
	plt.savefig(file_opath, bbox_inches='tight')

	########## repeat to display

	plt.imshow(smooth, origin='lower', extent=extent)
	plt.set_cmap('cool')
	plt.colorbar()
	plt.scatter(resamp_pnt_xx, resamp_pnt_yy, marker='+')

	plt.show()

	return smooth, extent


def smooth_density_surface_sans_points(Z_log, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr, density_to_nan_limit=-40):
	plt.figure()
	smooth = ndimage.filters.gaussian_filter(Z_log, sigma=1.0, order=0, mode='reflect')
	smooth[smooth<=density_to_nan_limit] = np.nan
	extent = (resamp_pnt_xx.min(), resamp_pnt_xx.max(), resamp_pnt_yy.min(), resamp_pnt_yy.max())
	plt.imshow(smooth, origin='lower', extent=extent)
	plt.set_cmap('cool')
	plt.colorbar()

	file_opath = "%s/contour_input_points_SMOOTH_DENSITY_%s.png" %(opath_no_file, itr) 
	util.check_output_dir(file_opath)	
	plt.savefig(file_opath, bbox_inches='tight')

	#plt.show()

	return smooth, extent


def grid_contour(surface, extent, xx, yy, opath_no_file, itr, show=0):
	cs = plt.contour(surface, linewidth = 5, extent=extent)
	plt.clabel(cs, inline=0, fontsize=10, colors='black')
	plt.gca().format_coord = util.live_view_z_extent(surface, extent)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.axis('equal')

	if show == 0:
		file_opath = "%s/contour_input_points_CONTOURS_%s.png" %(opath_no_file, itr) 
		util.check_output_dir(file_opath)	
		plt.savefig(file_opath, bbox_inches='tight')
	elif show== 1:
		plt.show()

	return cs


def grid_contour_specified(surface, extent, density_boundary, xx, yy, opath_no_file, itr):
	cs = plt.contour(surface, levels=[density_boundary], linewidth = 5, extent=extent)
	plt.clabel(cs, inline=0, fontsize=10, colors='black')
	#plt.gca().format_coord = util.live_view_z(smooth)
	plt.gca().format_coord = util.live_view_z_extent(surface, extent)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.axis('equal')
	#plt.show()

	file_opath = "%s/contour_input_points_CONTOUR_AT_%s_%s.png" %(opath_no_file, density_boundary, itr) 
	util.check_output_dir(file_opath)	
	plt.savefig(file_opath, bbox_inches='tight')

	#plt.show()

	return cs


def grid_contour_specified_input_points(surface, extent, density_boundary, xx, yy, opath_no_file, itr):
	cs = plt.contour(surface, levels=[density_boundary], linewidth = 5, extent=extent)
	plt.clabel(cs, inline=0, fontsize=10, colors='black')
	#plt.gca().format_coord = util.live_view_z(smooth)
	plt.gca().format_coord = util.live_view_z_extent(surface, extent)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.axis('equal')

	plt.scatter(xx, yy, marker='+')

	file_opath = "%s/contour_input_points_CHECK_EXTENT_%s.png" %(opath_no_file, itr) 
	util.check_output_dir(file_opath)
	plt.savefig(file_opath, bbox_inches='tight')

	#plt.show()

	return cs


def contour_vertices(cs):
	p = cs.collections[0].get_paths()[0]
	v = p.vertices
	contour_x = v[:,0]
	contour_y = v[:,1]
	contour_x_list = contour_x.tolist()
	contour_y_list = contour_y.tolist()

	return contour_x_list, contour_y_list


def contour_points_check_plot(smooth, contour_x, contour_y, density_boundary, extent, opath_no_file, itr):
	cs = plt.contour(smooth, levels=[density_boundary], linewidth = 5, extent=extent)
	plt.clabel(cs, inline=0, fontsize=10, colors='black')
	plt.scatter(contour_x, contour_y, marker='+')
	
	file_opath = "%s/contour_point_VERTICES_%s.png" %(opath_no_file, itr) 
	util.check_output_dir(file_opath)	
	plt.savefig(file_opath, bbox_inches='tight')

	#plt.show()

def write_contour_verts(filename, xvals, yvals):
	util.check_output_dir(filename)

	if os.path.exists(filename):
		f = open(filename, 'a')
	else:
		f = open(filename, 'w')
		f.write("x, y\n")

	for xval, yval in zip(xvals, yvals):
		f.write("%s, %s\n" %(xval, yval))
	f.close()