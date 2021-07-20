#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classdefinitions.py

This file stores the classes used by the program.
"""

from dataclasses import dataclass
from orbitalMechanicsRoutines import computeTrueAnomaly

@dataclass
class satellite:
    name: str
    satID: int
    ecc: float = None
    inc: float = None
    raan: float = None
    sma: float = None
    argper: float = None
    anomTrue: float = None
    epoch: float = None
    meanMotion: float = None
    anomMean: float = None
    period: float = None
    
    
    
    
    
        