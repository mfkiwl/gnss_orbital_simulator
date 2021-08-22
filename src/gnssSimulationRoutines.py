# -*- coding: utf-8 -*-
"""
gnssSimulationRoutines.py

This file contains the functions required for simulating the GNSS signal propagation and reception
"""

def computeLOS(satellitePos, receiverPos):
    #This function computes the line of sight distance (in a cartesian frame) between
    #a satellite and a receiver.
    
    from numpy import sqrt
    
    LOS = sqrt((satellitePos[0]-receiverPos[0])**2 + (satellitePos[1]-receiverPos[1])**2 + (satellitePos[2]-receiverPos[2])**2)
    
    return LOS


def elevationMask(satellitePos,receiverPos,maskAngle):
    #This function computes the elevation of every satellite and applies an elevation mask to
    #remove satellites whose elevation is bellow a cutoff angle. This is achieved by
    #returning a satellite mask vector that can be used in conjunction with the index
    #of the satellite list to ignore a given satellite. FIXME
    
    from geodesyRoutines import ecef2enu,enu2AzEl #Add ecef2llh #FIXME
    from numpy import zeros
    
    #Get the number of satellites in the simulation
    nSats = len(satellitePos)
    
    #Prepare a satellite mask array for all the satellites in the simulation
    satMask = zeros(nSats)
    
    #Compute the receiver position in LLH coordinates
    #receiverPosLLH = ecef2llh(receiverPos) #FIXME
    receiverPosLLH = receiverPos #FIXME
    
    #Compute the position of all satellites in an ENU frame centered in the receiver
    satellitePosENU = ecef2enu(satellitePos,receiverPosLLH)
    
    #Compute the elevation of all the satellites
    satelliteEl = enu2AzEl(satellitePosENU)[1]
    
    #Compare the elevation angle with the elevation mask to obtain the satellite mask
    for i in range(nSats-1):
        if satelliteEl[i] > maskAngle:
            satMask[i] = 1
    
    return satMask
    
    
    
    
    
    