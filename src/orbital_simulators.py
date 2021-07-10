#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Keplerian orbit simulator

This function simulates the orbital movement of the satellites by using a
keplerian approach, i.e. the orbit is static and the satellite position is a
function of time only.
"""

def simulation_keplerian(satellites):
    for i in satellites:
        