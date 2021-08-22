# -*- coding: utf-8 -*-
"""
geodesyRoutines.py

This file contains the functions required for conversion between several reference 
frames and other geodetic methods. Note that most of them are taken from 
https://github.com/JGManito/gnss_positioning_routines but are repeated here to
avoid dependencies for such simple functions and to promote easiness of reading
"""

import numpy as np

def rotX(alpha):
    #rotX implements the rotation matrix around the X axis by a given angle alpha, 
    #in radians. The output is a 3x3 numpy array.
    
    from math import cos,sin
    
    output = np.array([[1,0,0],
                       [0,cos(alpha),-sin(alpha)],
                       [0,sin(alpha),cos(alpha)]])
    
    return output


def rotY(beta):
    #rotY implements the rotation matrix around the Y axis by a given angle beta, 
    #in radians. The output is a 3x3 numpy array.
    
    from math import cos,sin
    
    output = np.array([[cos(beta),0, sin(beta)],
                       [0, 1, 0],
                       [-sin(beta),0,cos(beta)]])
    
    return output
    

def rotZ(gamma):
    #rotZ implements the rotation matrix around the Z axis by a given angle gamma, 
    #in radians. The output is a 3x3 numpy array.
    
    from math import cos,sin
    
    output = np.array([[cos(gamma),-sin(gamma),0],
                       [sin(gamma),cos(gamma),0],
                       [0,0,1]])
    
    return output


def llh2ecef(llh: np.array):
    #LLH2ECEF Converts geodetic coordinates (in degrees) to cartesian coordinates, using WGS-84 as
    #the reference ellipsoid. The input must be a numpy array with each coordinate set taking
    #a single line of the array in the order [latitude, longitude, height]
    
    #Define the WGS-84 ellipsoid constants
    a = 6378137
    f = 1/298.257223563
    
    
    #Split the input llh array into lat, lon and h for easier reading
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


def ecef2enu(ecefTarget: np.array, llhRef: np.array):
    #LLH2ENU converts geocentric coordinates (ECEF frame) to a local ENU reference frame, 
    #with origin at llhRef. Both the inputs must be numpy arrays with each coordinate set taking
    #a single line of the array in the order [x, y, z] for the target coordinates and [lat, lon, height]
    #for the reference coordinates. The ecefTarget variable can accept multiple
    #positions, but the llhRef variable must be a single 3x1 array.
    
    from math import pi,radians
    
    #Convert the reference position to ECEF coordinates
    ecefRef = llh2ecef(llhRef)
    
    #Split the arrays into column vectors for easier reading
    xTarget = ecefTarget[:,0]
    yTarget = ecefTarget[:,1]
    zTarget = ecefTarget[:,2]
    
    latOrigin = llhRef[0,1]
    lonOrigin = llhRef[0,1]
    
    xOrigin = ecefRef[0,0]
    yOrigin = ecefRef[0,1]
    zOrigin = ecefRef[0,2]
    
    #Obtain the position vector from the reference position 
    #the target
    dX = xTarget - xOrigin
    dY = yTarget - yOrigin
    dZ = zTarget - zOrigin
    dPosition = np.column_stack([dX,dY,dZ])
    
    
    #Apply the rotation matrix to obtain the target vector(s) in the ENU frame
    enuTarget = np.matmul(dPosition,np.matmul(rotX(radians(latOrigin)-pi/2),rotZ(-radians(lonOrigin)-pi/2)))
    
    return enuTarget
    
    
def enu2AzEl(enu: np.array):
    #enu2AzEl converts local frame coordinates (ENU frame) to azimuth and elevation
    #angles. The input must be a numpy array with each coordinate set taking
    #a single line of the array in the order [east, north, up]
    
    from numpy import arctan2,sqrt
    
    #Split the arrays into column vectors for easier reading
    east = enu[:,0]
    north = enu[:,1]
    up = enu[:,2]
    
    #Compute the elevation
    elevation = arctan2(up,sqrt(north**2 + east**2))
    
    #Compute the azimuth
    azimuth = arctan2(east,north)
    
    return azimuth,elevation
    
    


#def ecef2eci(ecef: numpy.array):
    #ECEF2ECI Converts geocentric coordinates (ECEF frame) to inertial coordinates (ECI frame), using WGS-84 as
    #the reference ellipsoid. The input must be a numpy array with each coordinate set taking
    #a single line of the array in the order [latitude, longitude, height]
    