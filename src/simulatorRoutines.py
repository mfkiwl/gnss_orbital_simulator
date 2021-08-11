# -*- coding: utf-8 -*-
"""
simulatorRoutines.py

Functions used to run the simulator
"""

from classDefinitions import satellite
from timeRoutines import timedate2epoch
from orbitalMechanicsRoutines import computeSMA, computeTrueAnomaly, computeRadius, computePerigeeTime, computeOrbitalPeriod

def addSatellite(satList, dataSource, simulationType, **kwargs):
    #Create new satellite object
    satelliteNew = satellite()
    
    #For TLEs
    if dataSource == "TLE":
        
        #Add type of input parameter data to the satellite object
        satelliteNew.dataSource = dataSource
        
        #Add type of simulation to use with this satellite object
        satelliteNew.simType = simulationType
        
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
    


def addStaticReceiver(coordinatesWGS84):
    #This function converts the receiver position in WGS84 to the ECI frame used in the satellite simulation
    
    #Unwrap the coordinates and assign them to dedicated variables for easier reading
    lat = coordinatesWGS84[1]
    lon = coordinatesWGS84[2]
    height = coordinatesWGS84[3]    #This is the altitude above the WGS84 elipsoid, not above MSL
    
    
    #Convert these coordinates to ECI
    


def simulationKepler(satellite,time):
    
    from orbitalMechanicsRoutines import computeTrueAnomaly,computeRadius
    import numpy as np
    import math
    
    #Unwrap the satellite object fields and name them according to orbital parameter nomenclature
    i = satellite.inc
    Omega = satellite.raan
    w0 = satellite.argPer
    
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
    r_ECI = np.array(np.matmul(rotZ,np.matmul(rotX,np.matmul(rotZ2,r_ORF))))
    
    #Convert to line vector
    r_ECI = r_ECI.transpose()
    
    return r_ECI

        
    return



def simulationMain(satelliteList,timeStep,simTime):
    
    import numpy as np
    
    #Create a position vector for each satellite
    r=[]
    for n in range(0,len(satelliteList)):
        r.append(np.zeros((simTime * int((1/timeStep)),3)))
    
    #Create a simulation time vector
    t = np.zeros(simTime*int(1/timeStep))
    
    
#     x = np.zeros([3600*8*sampFreq])
# y = np.zeros([3600*8*sampFreq])
# z = np.zeros([3600*8*sampFreq])
# t = np.zeros([3600*8*sampFreq])

    #Run the simulation
    
    for nIter in range(0,int(simTime*(1/timeStep))):
        
        #Compute the clock time of the simulation step
        time = nIter * timeStep
        t[nIter] = time
        
        #print(f"Simulation step: Time={time:.1f} (iteration #{nIter:d} of {int(simTime/timeStep):d})\n")
        
        #Choose simulator based on satellite class simType field
        n=0
        for sat in satelliteList:
            if sat.simType == "kepler":
                #print("Simulating satellite ",sat.name,"\n")
                r[n][nIter] = simulationKepler(sat,time)
                n +=1
            #elif: #Other simulation types
            else:
                print("Simulation Type not defined")
                
    return [r,t]