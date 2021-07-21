#!/usr/bin/env python3
# -*- coding: utf-8 -*-
%matplotlib qt
import matplotlib.pyplot as plt
import scipy
import numpy as np

import classDefinitions
import orbitalMechanicsRoutines
import timeRoutines
import math
from datetime import datetime,timedelta

#Define GNSS Sampling frequency
sampFreq = 5 #In Hertz


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

perigeeTime = 0
sma = 6000000
ecc = 0

x = np.zeros([3600*8*sampFreq])
y = np.zeros([3600*8*sampFreq])
z = np.zeros([3600*8*sampFreq])
t = np.zeros([3600*8*sampFreq])

for i in range(0,3600*8*sampFreq):
    time = i/sampFreq
    trueAnom = orbitalMechanicsRoutines.computeTrueAnomaly(perigeeTime,time,sma,ecc)
    r = orbitalMechanicsRoutines.computeRadius(sma,ecc,trueAnom)
    
    
    
    x[i] = r*math.cos(trueAnom)
    y[i] = r*math.sin(trueAnom)
    z[i] = 0
    t[i] = time


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
ax1.grid()
ax2.grid()
plt.show()