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
    #remove satellites whose elevation is bellow a cutoff angle
    
    from numpy import arctan2
    
    