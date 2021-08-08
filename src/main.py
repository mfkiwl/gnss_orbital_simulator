#!/usr/bin/env python3
# -*- coding: utf-8 -*-
%matplotlib tk
import matplotlib.pyplot as plt
import scipy
import numpy as np
import os

import classDefinitions
import orbitalMechanicsRoutines
import timeRoutines
import simulatorRoutines
import math
from datetime import datetime,timedelta

#Define GNSS Sampling frequency
sampFreq = 5 #In Hertz
timeStep = 0.2
simTime = 24*3600 #in seconds


# gravParamEarth = 3.986004418E14
# n = 15.48787420 * (2*math.pi/86400)
# sma = (gravParamEarth**(1/3))/(n**(2/3))
# #sma = 778194564622.574
# M0 = math.radians(210.8470)
# perigeeTime = M0/math.sqrt(gravParamEarth/(sma**3))
# ephDate = datetime(2021, 1, 1) + timedelta(191.89452546 - 1)
# Date = ephDate - datetime(2000,1,1,12)
# time = Date.total_seconds()
# ecc = 0.00020

from dataParsing import parseTLE


#Create the satellite list
#Open the TLE file
#File path is hardcoded for testing only, change!
filename = "tle.txt"
    
#Check if file exists, then open it or close the program
if os.path.isfile(filename):
    fidTLE = open(filename, "r", encoding='utf8')
    print("File opened successfully\n")
    
inputs = []

line = fidTLE.readline()
while line:
    inputs.append(str(line))
    line = fidTLE.readline()
    

array = parseTLE(inputs)
satList = []




for entry in array:
    simulatorRoutines.addSatellite(satList,"TLE","kepler",**entry)


perigeeTime = 0
sma = 6000000
ecc = 0
i = math.radians(55)
Omega = math.radians(35)
w0 = math.radians(60)

# x = np.zeros([simTime/timeStep])
# y = np.zeros([simTime/timeStep])
# z = np.zeros([simTime/timeStep])
# t = np.zeros([simTime/timeStep])

#Call the main simulation routine
[r,t] = simulatorRoutines.simulationMain(satList,timeStep,simTime)

t = np.arange(0, int(simTime/timeStep), 1)

fig = plt.figure()
ax = plt.axes(projection='3d')
for i in range(0,len(satList)):
    ax.plot3D(r[i][:,0], r[i][:,1], r[i][:,2])
    #fig1, ax1 = plt.subplots()
    #ax1.plot(t, x)
    #fig2, ax2 = plt.subplots()
    #ax2.plot(t, y)
    ax.grid()
    ax.axes.set_xlim3d(left=-3E7, right=3E7) 
    ax.axes.set_ylim3d(bottom=-3E7, top=3E7) 
    ax.axes.set_zlim3d(bottom=-3E7, top=3E7) 
    #ax1.grid()
    #ax2.grid()
    #plt.xlim(-6.5E7, 6.5E7)
    #plt.ylim(-6.5E7, 6.5E7)
    #plt.zlim(-6.5E7, 6.5E7)
    #fig.gca().set_aspect('equal', adjustable='box')
    
plt.show()

# fig1, ax1 = plt.subplots()
# ax1.plot(t, x)
# fig2, ax2 = plt.subplots()
# ax2.plot(t, y)
# fig3, ax3 = plt.subplots()
# ax3.plot(t, z)
# ax1.grid()
# ax2.grid()
# ax3.grid()
# plt.show()