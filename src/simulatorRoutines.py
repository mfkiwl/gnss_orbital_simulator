# -*- coding: utf-8 -*-
"""
simulatorRoutines.py

Functions used to run the simulator
"""

from classDefinitions import satellite
from timeRoutines import timedate2epoch
from orbitalMechanicsRoutines import computeSMA, computeTrueAnomaly, computeRadius, computePerigeeTime, computeOrbitalPeriod

def addSatellite(satList, parameterType, **kwargs):
    #Create new satellite object
    satelliteNew = satellite()
    
    #For TLEs
    if parameterType == "TLE":
        #All parameters except epoch
        for key in ('name', 'inc', 'raan', 'ecc', 'argPer', 'anomMeanEpoch', 'meanMotion'):
            if key in kwargs:
                setattr(satelliteNew, key, kwargs[key])
        
        #Compute the epoch in J2000
        for key,value in kwargs.items():
            if key == 'epochY':
                epochY = value
            if key == 'epoch':
                epochD = value
                
        satelliteNew.epoch = timedate2epoch(year=epochY, DoY=epochD)
        
        #Fill the missing data    
        satelliteNew.sma = computeSMA(satelliteNew.meanMotion)
        satelliteNew.perigeeTime = computePerigeeTime(satelliteNew.anomMeanEpoch,satelliteNew.meanMotion,satelliteNew.epoch)
        satelliteNew.anomTrue = computeTrueAnomaly(satelliteNew.perigeeTime, satelliteNew.epoch, satelliteNew.sma, satelliteNew.ecc)
        satelliteNew.period = computeOrbitalPeriod(satelliteNew.sma)
        satelliteNew.orbitRadius = computeRadius(satelliteNew.sma, satelliteNew.ecc, satelliteNew.anomTrue)
        
            
            
    
    #For YUMA data
    
    
    #For other data
    
    
    #Add the satellite to the list
    satList.append(satelliteNew)
    
    return satList
    

from math import radians,degrees,pi
satList = []
parameterType = "TLE"
inputs= {'name':"ISS", 'epochY':2021, 'epoch':202.66605324, 'inc':radians(51.6429) , 'raan':radians(172.2233) , 'ecc':0.0001549 , 'argPer':radians(182.0461) , 'anomMeanEpoch':radians(157.9175) , 'meanMotion':15.48829759293939*(2*pi/86400)}
addSatellite(satList, parameterType, **inputs)

print("ISS TLE Data:\n")
print("Eccentricity = ",satList[0].ecc,"\n")
print("Inclination = ",degrees(satList[0].inc),"\n")
print("RAAN = ",degrees(satList[0].raan),"\n")
print("SMA = ",satList[0].sma,"\n")
print("ArgPer = ",degrees(satList[0].argPer),"\n")
print("Mean Motion (rad/s) = ",satList[0].meanMotion,"\n")
print("Mean Motion (rev/day) = ",satList[0].meanMotion/(2*pi/86400),"\n")
print("Mean Anomaly at Epoch = ",degrees(satList[0].anomMeanEpoch),"\n")
print("Orbital Period (s) = ",satList[0].period,"\n")
print("Orbital Period (min) = ",satList[0].period/60,"\n")


