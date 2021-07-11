#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import scipy
import numpy as np

#import classDefinitions.py
import orbitalMechanicsRoutines
import math
from datetime import datetime,timedelta

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
sma = 6500000
ecc = 0

x = np.zeros([3600*8])
y = np.zeros([3600*8])

for t in range(0,3600*8):
    trueAnom = orbitalMechanicsRoutines.computeTrueAnomaly(perigeeTime,t,sma,ecc)
    r = orbitalMechanicsRoutines.computeRadius(sma,ecc,trueAnom)
    
    x[t] = r*math.cos(trueAnom)
    y[t] = r*math.sin(trueAnom)


t = np.arange(0, 3600*8, 1)
fig, ax = plt.subplots()
ax.plot(x, y)
ax.grid()
#plt.axis('equal')
plt.show()