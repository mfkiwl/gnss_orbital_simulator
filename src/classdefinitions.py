#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classdefinitions.py

This file stores the classes used by the program.
"""

class satellite:
    def __init__(self,satName,satID,ecc,inc,rra,sma,argper,anomMean...
                 epochDoY,epochY,simulationType):
        #Direct mapping of input data
        self.name = satName
        self.id = satID 
        self.ecc = ecc
        self.inc = inc
        self.rra = rra
        self.sma = sma
        self.argper = argper
        self.anomMean = anomMean
        
        #Processing of input data to obtain new parameters
        #Convert the epoch to J2000.0
        