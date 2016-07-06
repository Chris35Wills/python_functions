import sys
import concave_hull_funcs
reload(concave_hull_funcs)

'''
Calculates the density perimeter of a pre-calculated density surface
Plots are provided for review and to check the efficacy of the process
Outputs the xy coordinates of the contours in the projection of the input point file

REQUIRMENTS:
density xyz tab delimited file 
point xy space delimited file
output path for images if to be saved and contour xy output files
density boundary limit i.e. the log of the point density you wish to use as the boundary
'''

def density_hull_approximator(density_xyz_file, points_xy_file, opath, opath_no_file, itr, density_boundary=-16.500, save_contours_xy=0):
	
	xx,yy,zz = concave_hull_funcs.get_density_xyz(density_xyz_file) 
	resamp_pnt_xx, resamp_pnt_yy = concave_hull_funcs.get_points_xy_resamp(points_xy_file) 

	Z_log = concave_hull_funcs.grid_log_density(xx,yy,zz) 

	smooth, extent = concave_hull_funcs.smooth_density_surface_points(Z_log, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr) ## PLOT GAUSSIAN FILTERED DENSITY SURFACE [WITH POINTS]
	#smooth, extent = concave_hull_funcs.smooth_density_surface_sans_points(Z_log, resamp_pnt_xx, resamp_pnt_yy)

	#cs = concave_hull_funcs.grid_contour_specified(smooth, extent, density_boundary, resamp_pnt_xx, resamp_pnt_yy)	## SURFACE CONTOUR
	cs = concave_hull_funcs.grid_contour_specified_input_points(smooth, extent, density_boundary, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr)
	#cs = concave_hull_funcs.grid_contour(smooth, extent, resamp_pnt_xx, resamp_pnt_yy)

	contour_x_list, contour_y_list = concave_hull_funcs.contour_vertices(cs) 	
	concave_hull_funcs.contour_points_check_plot(smooth, contour_x_list, contour_y_list, density_boundary, extent, opath_no_file, itr)

	if save_contours_xy==1:
		concave_hull_funcs.write_contour_verts(opath, contour_x_list, contour_y_list)



def density_CONTOURS(density_xyz_file, points_xy_file, opath, opath_no_file, itr, save_contours_xy=0, show=0):
	'''
	Just saves a contoured density image with overlying points - useful to estimate the density_boundary value	
	'''
	xx,yy,zz = concave_hull_funcs.get_density_xyz(density_xyz_file) 
	resamp_pnt_xx, resamp_pnt_yy = concave_hull_funcs.get_points_xy_resamp(points_xy_file) 

	Z_log = concave_hull_funcs.grid_log_density(xx,yy,zz) 

	smooth, extent = concave_hull_funcs.smooth_density_surface_points(Z_log, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr) ## PLOT GAUSSIAN FILTERED DENSITY SURFACE [WITH POINTS]
	#smooth, extent = concave_hull_funcs.smooth_density_surface_sans_points(Z_log, resamp_pnt_xx, resamp_pnt_yy)

	cs = concave_hull_funcs.grid_contour(smooth, extent, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr, show=show)

def density_CONTOURS_xy(density_xyz_file, points_x, points_y, opath, opath_no_file, itr, save_contours_xy=0, show=0):
	'''
	Just saves a contoured density image with overlying points - useful to estimate the density_boundary value	
	'''
	xx,yy,zz = concave_hull_funcs.get_density_xyz(density_xyz_file) 
	resamp_pnt_xx = points_x[1::100]
	resamp_pnt_yy = points_y[1::100]

	Z_log = concave_hull_funcs.grid_log_density(xx,yy,zz) 

	smooth, extent = concave_hull_funcs.smooth_density_surface_points(Z_log, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr) ## PLOT GAUSSIAN FILTERED DENSITY SURFACE [WITH POINTS]
	#smooth, extent = concave_hull_funcs.smooth_density_surface_sans_points(Z_log, resamp_pnt_xx, resamp_pnt_yy)

	cs = concave_hull_funcs.grid_contour(smooth, extent, resamp_pnt_xx, resamp_pnt_yy, opath_no_file, itr, show=show)