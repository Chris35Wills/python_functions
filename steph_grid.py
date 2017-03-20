# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:20:43 2016

@author: steph
"""

class Grid:
    
    
    """
    n dimensional grid class. Provides cell / node-centered 
    slices, co-ordinates, and meshes
    Initialize with two corners and a mesh spacing, all as n-tuples
    """     
    
    import numpy as np
    
    def __init__(self, lo, hi, delta):
        
        if ( (type(lo) != tuple) or (type(hi) != tuple) or  (type(delta) != tuple) ):
            raise TypeError("lo, hi, delta must be tuples")
         
        if ( ( len(lo) != len(hi) ) |  ( len(lo) != len(delta) ) ):
            raise ValueError("lo, hi, delta must be tuples of the same length")
           
           
        self.__ndim = len(lo)   
        self.__slice_centre = list()
        self.__slice_node = list()
        for l,h,d in zip(lo,hi,delta):    
            self.__slice_centre.append( slice(l+0.5*d,h,d)  )
            self.__slice_node.append( slice(l,h+0.5*d,d)  )   
            
    def nodal(self):
        return True
        
    def central(self):
        return False
        
    def axis_slice( self, n, nodal ):
        """ slice along axis n """
        if (type(nodal) != bool):
            raise TypeError("nodal must be bool")
        if (type(n) != int ):
            raise TypeError("n must be int")
        
        if (nodal):
            return self.__slice_node[n]
        else:
            return self.__slice_centre[n] 
            
    def axis_x( self, n, nodal ):
        """ 1D array along axis n """
        return np.mgrid(self.axis_slice(n,nodal))
        
    def mesh_slice( self, nodal):
        """ list of slices, mixed nodal and central """
        if (type(nodal) != tuple):
            raise TypeError("nodal must be tuple")

        if (len(nodal) != self.__ndim ):
            raise ValueError('len(nodal) != {}'.format(self.__ndim))
        
        slicel = list()
        for k,n in zip(range(0,self.__ndim), nodal):
            slicel.append(self.axis_slice(k,n))
        
        return slicel
        
    def mesh(self, nodal):
        """ mesh of x,y,z,... values """
        return tuple(np.mgrid[ self.mesh_slice(nodal)])
       
#3D grid exmample
import matplotlib.pyplot as plt
import numpy as np
       
lo = (0.0,0.0,0.0)
hi = (12.0,6.0,3.0) 
delta = (0.2, 0.1 , 1.0)            
grid = Grid( lo,  hi, delta)
            
xn,yn,zn = grid.mesh ( (grid.nodal(), grid.nodal(), grid.nodal()) ) 
xc,yc,zc = grid.mesh ( (grid.central(), grid.central(), grid.central()) ) 

print ( 'xn = ', xn[:,0,0] )
print ( 'yn = ', yn[0,:,0] )
print ( 'zn = ', zn[0,0,:] )
print ( 'xc = ', xc[:,0,0] )
print ( 'yc = ', yc[0,:,0] )
print ( 'zc = ', zc[0,0,:] )



r = np.sqrt( xc**2 + yc**2 + zc**2)

plt.figure(figsize=(4,8))
for k in range(0,3):
    sp = 311+k*10
    plt.subplot(311+k, aspect = 'equal' )
    #plt.pcolormesh(xn[:,0,k], yn[0,:,k], np.transpose(r[:,:,k]))
    cs = plt.contour(xc[:,0,k], yc[0,:,k], np.transpose(r[:,:,k]), range(2,13,2),color='k')
    plt.clabel(cs)
    plt.ylabel('y')
    plt.text(9,1,'z = {}'.format(zc[0,0,k]))
    


       