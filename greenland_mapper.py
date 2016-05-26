'''
Creates a basic black and white map of Greenland
Contains method "polar_stere" which returns a basemap object - check help

Modified by Chris Williams 12/03/15
'''

import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as basemap


def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.

    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.

    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = basemap.Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='c')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return basemap.Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                           llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                           urcrnrlon=ur_lon, urcrnrlat=ur_lat, **kwargs)


if __name__ == '__main__':
    nps = polar_stere(-60, -25, 59, 85, resolution='l')
    
    nps.drawmapboundary(fill_color='white')
    nps.fillcontinents(color='black', lake_color='white')

    mer = np.arange(-100, 120, 10.)
    par = np.arange(0, 90, 10.)
    nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
    nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
       
    ## Plot a point...  
    '''
    lon_helheim = -38.2
    lat_helheim = 66.35
    x_helheim,y_helheim = nps(lon_helheim,lat_helheim)
    nps.plot(x_helheim, y_helheim, 'ro', markersize=15)    
    '''

    #plt.show()
    plt.savefig("O:/Documents/CHRIS_Bristol/Mapping/greenland_overview.png", dpi=300, transparent=True)