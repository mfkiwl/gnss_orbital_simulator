# -*- coding: utf-8 -*-
"""
geodesyRoutines.py

This file contains the functions required for conversion between several reference 
frames and other geodetic methods. Note that most of them are taken from 
https://github.com/JGManito/gnss_positioning_routines but are repeated here to
avoid dependencies for such simple functions
"""

def llh2ecef(llh: numpy.array):
    #LLH2ECEF Converts geodetic coordinates (in degrees) to cartesian coordinates, using WGS-84 as
    #the reference ellipsoid. The input must be a numpy array with each coordinate set taking
    #a single line of the array in the order [latitude, longitude, height]
    
    import numpy as np
    
    #Define the WGS-84 ellipsoid constants
    a = 6378137
    f = 1/298.257223563
    
    
    #Split the input llh vector into lat, lon and h for easier reading
    lat = llh[:,0]
    lon = llh[:,1]
    h = llh[:,2]
    
    
    #Compute the radius of curvature in the prime vertical
    RN = a / np.sqrt(1 - f * (2 - f) * np.sin(np.radians(lat))**2)
    
    
    #Compute the cartesian coordinates
    x = (RN + h) * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    y = (RN + h) * np.cos(np.radians((lat))) * np.sin(np.radians((lon)))
    z = ((1 - f)**2 * RN + h) * np.sin(np.radians(lat))
    
    #Create the output vector
    xyz=np.empty_like(llh)
    xyz[:,0:1] = x
    xyz[:,1:2] = y
    xyz[:,2:3] = z

    return xyz


def ecef2eci(ecef: numpy.array):
    #ECEF2ECI Converts geocentric coordinates (ECEF frame) to inertial coordinates (ECI frame), using WGS-84 as
    #the reference ellipsoid. The input must be a numpy array with each coordinate set taking
    #a single line of the array in the order [latitude, longitude, height]
    