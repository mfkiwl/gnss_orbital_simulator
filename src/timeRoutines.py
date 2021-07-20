#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timeRoutines.py

Functions related to date and epoch calculations
"""

from datetime import datetime,timedelta
    
def timedate2epoch(year=None, month=None, day=None, DoY=None, hours=None, minutes=None, seconds=None,
                   secondsofday=None):
    
    #Get the date of the epoch in datetime format
    if year and month and day:
        date = datetime(year,month,day)
    elif year and DoY:
        date = datetime(year, 1, 1) + timedelta(DoY - 1)
    else:
        print("Error: Date not supplied or incorrect")
    
    
    #Get the time of the epoch in datetime format
    if hours and minutes and seconds:
        time = datetime(date.year,date.month,date.day,hours,minutes,seconds)
    elif secondsofday:
        hour = secondsofday // 3600
        secondsofday %= 3600
        minutes = secondsofday // 60
        secondsofday %= 60
        seconds = round(secondsofday)
        time = datetime(date.year,date.month,date.day,hour,minutes,seconds)
    else:
        print("Error: Time not supplied or incorrect")
    
    
    #Convert date and time to J2000
    epoch = time - datetime(2000,1,1,12)
        
    return epoch.total_seconds()