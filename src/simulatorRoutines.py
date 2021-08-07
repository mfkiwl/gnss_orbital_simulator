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
        
        #Add type of input parameter data to the satellite object
        satelliteNew.simtype = parameterType
        
        #All parameters except epoch
        for key in ('name', 'satID', 'inc', 'raan', 'ecc', 'argPer', 'anomMeanEpoch', 'meanMotion'):
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
    

# from math import radians,degrees,pi
# satList = []
# parameterType = "TLE"
# inputs= {'name':"ISS", 'epochY':2021, 'epoch':202.66605324, 'inc':radians(51.6429) , 'raan':radians(172.2233) , 'ecc':0.0001549 , 'argPer':radians(182.0461) , 'anomMeanEpoch':radians(157.9175) , 'meanMotion':15.48829759293939*(2*pi/86400)}
# addSatellite(satList, parameterType, **inputs)

# print("ISS TLE Data:\n")
# print("Eccentricity = ",satList[0].ecc,"\n")
# print("Inclination = ",degrees(satList[0].inc),"\n")
# print("RAAN = ",degrees(satList[0].raan),"\n")
# print("SMA = ",satList[0].sma,"\n")
# print("ArgPer = ",degrees(satList[0].argPer),"\n")
# print("Mean Motion (rad/s) = ",satList[0].meanMotion,"\n")
# print("Mean Motion (rev/day) = ",satList[0].meanMotion/(2*pi/86400),"\n")
# print("Mean Anomaly at Epoch = ",degrees(satList[0].anomMeanEpoch),"\n")
# print("Orbital Period (s) = ",satList[0].period,"\n")
# print("Orbital Period (min) = ",satList[0].period/60,"\n")



def simulationKepler(satellite,time):
    
    from orbitalMechanicsRoutines import computeTrueAnomaly,computeRadius
    import numpy as np
    import math
    
    #Unwrap the satellite object fields and name them according to orbital parameter nomenclature
    i = satellite.inc
    Omega = satellite.raan
    w0 = satellite.argper
    
    #Compute the true anomaly of the satellite (i.e. the "true angle")
    trueAnom = computeTrueAnomaly(satellite.perigeeTime,time,satellite.sma,satellite.ecc)
    
    #Update the true anomaly in the satellite object
    satellite.trueAnom = trueAnom
    
    #Compute the position vector from focus to the satellite
    r = computeRadius(satellite.sma,satellite.ecc,satellite.trueAnom)

    
    x_ORF = r*math.cos(trueAnom)
    y_ORF = r*math.sin(trueAnom)
    z_ORF = 0
    
    r_ORF = np.transpose(np.matrix([x_ORF,y_ORF,z_ORF]))
    
    
    #Define the rotation matrices from the orbital reference frame to the ECEF frame
    rotX = np.array([[1,0,0],
                     [0,math.cos(-i),math.sin(-i)],
                     [0,-math.sin(-i),math.cos(-i)]])

    rotZ = np.array([[math.cos(-Omega),math.sin(-Omega),0],
                     [-math.sin(-Omega),math.cos(-Omega),0],
                     [0,0,1]])
    
    rotZ2 = np.array([[math.cos(-w0),math.sin(-w0),0],
                      [-math.sin(-w0),math.cos(-w0),0],
                      [0,0,1]])
    
    #Use rotation matrices to obtain the satellite position in an ECEF frame 
    r_ECI = np.matmul(rotZ,np.matmul(rotX,np.matmul(rotZ2,r_ORF)))
    
    return r_ECI

        
    return



def simulationMain(satelliteList,timeStep,simTime):
    
    import numpy as np
    
    #Create a position vector for each satellite
    r=[]
    for n in range(0,len(satelliteList)):
        r[n] = np.zeros(simTime * int((1/timeStep)),3)
    
    #Create a simulation time vector
    t = np.zeros(simTime*(1/timeStep))
    
    
#     x = np.zeros([3600*8*sampFreq])
# y = np.zeros([3600*8*sampFreq])
# z = np.zeros([3600*8*sampFreq])
# t = np.zeros([3600*8*sampFreq])

    #Run the simulation
    
    for nIter in range(0,timeStep,simTime*(1/timeStep)):
        
        #Compute the clock time of the simulation step
        time = nIter * timeStep
        t[nIter] = time
        
        #Choose simulator based on satellite class simType field
        n=0
        for sat in satelliteList:
            if sat.simType == "kepler":
                r[n,nIter] = simulationKepler(sat,time)
                n +=1
            #elif: #Other simulation types
            else:
                print("Simulation Type not defined")
                
    return [r,t]