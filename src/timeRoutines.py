#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timeRoutines.py

Functions related to date and epoch calculations
"""

from datetime import datetime,timedelta
from math import floor
    
def timedate2epoch(year=None, month=None, day=None, DoY=None, hours=None, minutes=None, seconds=None, secondsofday=None):
    
    #Convert fractional days and seconds
    if isinstance(day, float):
        dayFrac = day - floor(day)
        day = int(floor(day))
        secondsofday = dayFrac * 3600 * 24
        
    if isinstance(DoY, float):
        dayFrac = DoY - floor(DoY)
        DoY = int(floor(DoY))        
        secondsofday = dayFrac * 3600 * 24
        
    if isinstance(seconds,float):
        secondsFrac = seconds - floor(seconds) #will be added to the final epoch because datetime requires int seconds
        seconds = int(floor(seconds))
        
    if isinstance(secondsofday,float):
        secondsFrac = secondsofday - floor(secondsofday) #will be added to the final epoch because datetime requires int seconds
        secondsofday = int(floor(secondsofday))
        
    if 'secondsFrac' in locals():
        pass
    else:
        secondsFrac = 0
    
    #Get the date of the epoch in datetime format
    if year and month and day:
        date = datetime(year,month,day)
    elif year and DoY:
        date = datetime(year, 1, 1) + timedelta(DoY - 1)
    else:
        print("Error: Date not supplied or incorrect")
    
    
    #Get the time of the epoch in datetime format
    if hours and minutes and seconds:
        time = datetime(year=date.year,month=date.month,day=date.day,hours=hours,minutes=minutes,seconds=seconds)
    elif secondsofday is not None:
        hours = secondsofday // 3600
        secondsofday %= 3600
        minutes = secondsofday // 60
        secondsofday %= 60
        seconds = round(secondsofday)
        time = datetime(year=date.year,month=date.month,day=date.day,hour=hours,minute=minutes,second=seconds)
    else:
        print("Error: Time not supplied or incorrect")
    
    
    #Convert date and time to J2000
    epochDate = time - datetime(2000,1,1,12)
    
    #Add the fractional seconds
    epoch = epochDate.total_seconds() + secondsFrac
    
        
    return epoch