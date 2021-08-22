#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classDefinitions.py

This file stores the classes used by the program.
"""

from dataclasses import dataclass

@dataclass
class satellite:
    name: str = None
    satID: int = None
    dataSource: str = None      #Data source for orbital parameters: TLE, YUMA, etc
    simType: str = None         #Simulation type. Currently only Keplerian
    #planet: str = None         #For possible later use?
    #gravParam: float = None    #For possible later use?
    ecc: float = None
    inc: float = None
    raan: float = None
    sma: float = None
    argPer: float = None
    anomTrue: float = None
    epoch: float = None
    meanMotion: float = None
    anomMeanEpoch: float = None
    period: float = None
    orbitRadius: float = None
    perigeeTime: float = None