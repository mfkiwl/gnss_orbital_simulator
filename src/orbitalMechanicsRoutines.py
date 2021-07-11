# -*- coding: utf-8 -*-
"""
orbitalMechanicsRoutines.py

Functions that compute orbital parameters
"""



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
    
    #Rename input data to their orbital paramameter nomenclature
    a = sma
    e = ecc
    v = trueAnom
    
    r = (a * (1 - e**2))/(1 + e*math.cos(v))
    
    return r
    