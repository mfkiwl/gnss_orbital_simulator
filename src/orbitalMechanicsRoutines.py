# -*- coding: utf-8 -*-
"""
orbitalMechanicsRoutines.py

Functions that compute orbital parameters
"""

def computeSMA(meanMotion):
    
    gravParamEarth = 3.986004418E14
    
    #Rename input data to their orbital paramameter nomenclature
    n = meanMotion
    
    #Compute the semi-major axis
    a = (gravParamEarth / (n**2))**(1/3)
    
    return a
    

def computePerigeeTime(anomMeanEpoch,meanMotion,epoch):
    
    #Rename input data to their orbital paramameter nomenclature
    n = meanMotion
    M0 = anomMeanEpoch
    t0 = epoch
    
    #Compute the perigee time
    T0 = t0 - M0/n 
    
    return T0
    

def computeOrbitalPeriod(sma):
    
    from math import pi,sqrt
    
    gravParamEarth = 3.986004418E14
    
    #Rename input data to their orbital paramameter nomenclature
    a = sma
    
    #Compute the orbital period
    T = 2 * pi * sqrt((a**3)/gravParamEarth)
    
    return T
    
    
    

def computeTrueAnomaly(perigeeTime,time,sma,ecc):
    
    import math
    
    gravParamEarth = 3.986004418E14
    
    #Rename input data to their orbital paramameter nomenclature
    a = sma
    t = time
    t0 = perigeeTime
    e = ecc
    
    #Compute the mean motion
    n=math.sqrt(gravParamEarth/(a**3))
    
    #Compute the mean anomaly
    M = n*(t-t0)

    #Compute the eccentric anomaly using the Newton-Raphson method
    dEk = 1
    Ek = M
    E = M
    while abs(dEk) > 10E-10:
        dMk = Ek - e * math.sin(Ek) - M    
        dEk = -dMk/(1 - e*math.cos(Ek))
        Ek = Ek + dEk
    
    #Compute the true anomaly
    v = 2 * math.atan(math.sqrt((1 + e)/(1 - e)) * math.tan(E/2))
    
    return v


def computeRadius(sma,ecc,trueAnom):
    
    import math
    
    #Rename input data to their orbital parameter nomenclature
    a = sma
    e = ecc
    v = trueAnom
    
    r = (a * (1 - e**2))/(1 + e*math.cos(v))
    
    return r
    

def computeSatellitePositionECEF(satelliteObject):
    
    import numpy as np
    from math import sin,cos
    
    #Unwrap the satellite object fields and name them according to orbital parameter nomenclature
    i = satelliteObject.inc
    Omega = satelliteObject.raan
    w0 = satelliteObject.argper
    v = satelliteObject.anomTrue
    r = satelliteObject.orbitRadius
    
    #Obtain the satellite position vector in the orbital plane
    x = r*cos(v)
    y = r*sin(v)
    z = 0
    
    r_orbital = np.matrix([x,y,z])
    
    
    #Define the rotation matrices from the orbital reference frame to the ECEF frame
    rotX = np.array([[1,0,0],
                     [0,cos(-i),sin(-i)],
                     [0,-sin(-i),cos(-i)]])

    rotZ = np.array([[cos(-Omega),sin(-Omega),0],
                     [-sin(-Omega),cos(-Omega),0],
                     [0,0,1]])
    
    rotZ2 = np.array([[cos(-w0),sin(-w0),0],
                      [-sin(-w0),cos(-w0),0],
                      [0,0,1]])
    
    #Use rotation matrices to obtain the satellite position in an ECEF frame 
    r_ECEF = np.array(np.matmul(rotZ,np.matmul(rotX,np.matmul(rotZ2,r_orbital))))
    
    return r_ECEF
    