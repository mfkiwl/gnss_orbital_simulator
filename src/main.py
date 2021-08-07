#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%matplotlib tk
import matplotlib.pyplot as plt
import scipy
import numpy as np

import classDefinitions
import orbitalMechanicsRoutines
import timeRoutines
import simulatorRoutines
import math
from datetime import datetime,timedelta

#Define GNSS Sampling frequency
sampFreq = 5 #In Hertz
timeStep = 0.2
simTime = 3600


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

array = parseTLE(["ISS (ZARYA)             ","1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927","2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"])
satList = []

for entry in array:
    simulatorRoutines.addSatellite(satList,"TLE",**entry)


perigeeTime = 0
sma = 6000000
ecc = 0
i = math.radians(55)
Omega = math.radians(35)
w0 = math.radians(60)

x = np.zeros([3600*8*sampFreq])
y = np.zeros([3600*8*sampFreq])
z = np.zeros([3600*8*sampFreq])
t = np.zeros([3600*8*sampFreq])

#Create satellite list
inputs= {'name':"ISS", 'epochY':2021, 'epoch':202.66605324, 'inc':math.radians(51.6429) , 'raan':math.radians(172.2233) , 'ecc':0.0001549 , 'argPer':math.radians(182.0461) , 'anomMeanEpoch':math.radians(157.9175) , 'meanMotion':15.48829759293939*(2*math.pi/86400)}
satList = []
satList = simulatorRoutines.addSatellite(satList,"TLE",**inputs)

#Call the main simulation routine
[r,t] = simulatorRoutines.simulationMain(satList,timeStep,simTime)

t = np.arange(0, 3600*8*sampFreq, 1)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z)
#fig1, ax1 = plt.subplots()
#ax1.plot(t, x)
#fig2, ax2 = plt.subplots()
#ax2.plot(t, y)
ax.grid()
#ax1.grid()
#ax2.grid()
plt.xlim(-6.5E6, 6.5E6)
plt.ylim(-6.5E6, 6.5E6)
#fig.gca().set_aspect('equal', adjustable='box')
plt.show()

fig1, ax1 = plt.subplots()
ax1.plot(t, x)
fig2, ax2 = plt.subplots()
ax2.plot(t, y)
fig3, ax3 = plt.subplots()
ax3.plot(t, z)
ax1.grid()
ax2.grid()
ax3.grid()
plt.show()