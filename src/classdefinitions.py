#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classdefinitions.py

This file stores the classes used by the program.
"""

from datetime import datetime,timedelta
from orbitalMechanicsRoutines import computeTrueAnomaly

class satellite:
    def __init__(self,satName,satID,ecc,inc,raan,sma,argper,anomMean,anomTrue,\
                 ephToD,ephDoY,ephY,simulationType):
        #Direct mapping of input data
        self.name = satName
        self.id = satID 
        self.ecc = ecc
        self.inc = inc
        self.rra = raan
        self.sma = sma
        self.argper = argper
        self.anomTrue = anomTrue
        
        
        #Processing of input data to obtain new parameters
        #Convert the epoch to J2000.0
        ephDate = datetime(ephY, 1, 1) + timedelta(ephDoY - 1)
        epochDate = ephDate - datetime(2000,1,1,12)
        self.epoch = epochDate.total_seconds()
        
        