# -*- coding: utf-8 -*-
"""
dataParsing.py

Functions used to parse TLE, YUMA and other kinds of data
"""

def parseTLE(tleInput):
    
    import re
    from math import radians,pi
    
    #Go through all the TLE lines and create an array of TLE data
    tleArray = []
    i = 0 #Counter for the current line of each TLE set
    for line in tleInput:
        if i == 0:
            name = re.match(".{24}", line)
            name = name.group(0)
            name = name.rstrip()
            i += 1
            continue
           
        if i == 1:
            tleLine = re.match("(.{1}) (.{5})(.{1}) (.{2})(.{3})(.{3}) (.{2})(.{12}) (.{10}) (.{8}) (.{8}) (.{1}) (.{4})(.{1})", line)
            if tleLine:
                #Map the matches to variables
                
                #NORAD ID
                noradID = int(tleLine.group(2))
                
                #Satellite Classification
                classification = tleLine.group(3)
                
                #COSPAR ID
                if int(tleLine.group(4)) > 57: #The first COSPAR item is the sputnik, launched in 1957. Use it to convert 2-digit year to 4-digit
                    cosparID = "19"+tleLine.group(4)+"-"+tleLine.group(5)+tleLine.group(6)
                else:
                    cosparID = "20"+tleLine.group(4)+"-"+tleLine.group(5)+tleLine.group(6)
                
                #Epoch Year
                if int(tleLine.group(7)) > 50: #Convert the epoch year from 2-digit to 4-digit
                    epochYear = 1900 + int(tleLine.group(7))
                else:
                    epochYear = 2000 + int(tleLine.group(7))
                    
                #Epoch day of the year with fractional part of the day
                epoch = float(tleLine.group(8))
                
                #First time derivative of the Mean Motion
                firstDerivMeanMotion = float(tleLine.group(9))
                
                #Second Time Derivative of Mean Motion (with decimal point)
                secondDerivMeanMotion = float(tleLine.group(10)[0]+"0."+tleLine.group(10)[1:-2]+"e"+tleLine.group(10)[-2:])
                
                #Drag Term aka Radiation Pressure Coefficient
                dragTerm = float(tleLine.group(11)[0]+"0."+tleLine.group(11)[1:-2]+"e"+tleLine.group(11)[-2:])
                
                #Ephemeris type
                ephType = int(tleLine.group(12))
                
                #Element set number
                elemSetNum = int(tleLine.group(13))
                
                #Checksum
                checksum1 = int(tleLine.group(14))
                
                i += 1
                    
                continue
            
        if i == 2:
            tleLine = re.match("(.{1}) (.{5}) (.{8}) (.{8}) (.{7}) (.{8}) (.{8}) (.{11})(.{5})(.{1})", line)
            if tleLine:
                #Map the matches to variables
                
                #Line number and satellite check
                if tleLine.group(1) != "2" or int(tleLine.group(2)) != noradID:
                    print("Mismatched TLE line entries\n")
                    break
                
                #Inclination (degrees->radians)
                inclination = radians(float(tleLine.group(3)))
                
                #Right Ascension of the Ascending Node (degrees->radians)
                RAAN = radians(float(tleLine.group(4)))
                
                #Eccentricity
                ecc = float("0."+tleLine.group(5))
                
                #Argument of perigee(degrees->radians)
                argPerigee = radians(float(tleLine.group(6)))
                
                #Mean Anomaly (degrees->radians)
                meanAnomally = radians(float(tleLine.group(7)))
                
                #Mean Motion (revolutions per day->rad/s)
                meanMotion = (2*pi/(24*3600))*float(tleLine.group(8))
                
                #Revolution number at epoch (revolutions)
                revolutionNumber = int(tleLine.group(9))
                
                #Checksum
                checksum2 = int(tleLine.group(10))
                
                i = 0 #Reset the counter
                
                #Save the data to the TLE array
                tleArray.append({'name':name, 'satID':noradID, 'epochY':epochYear, 'epoch':epoch, 'inc':inclination , 'raan':RAAN , 'ecc':ecc , 'argPer':argPerigee , 'anomMeanEpoch':meanAnomally , 'meanMotion':meanMotion})
                    
    return tleArray
                
            
#def parseYUMA()

def parse_receiver_data(receiver_file_id):
# This function parses the receiver data file and outputs the different parameters
# required for the simulation.
#
# Input:  TextIOWrapper
# Output: return_code (int)
#         receiver_name (str)
#         receiver_type (str)
#         receiver_observables (list of str)
#         receiver_clock_parameters (TBD, placeholder)
#         receiver_noise (float)
#         if receiver_type == static: #Single position
#             receiver_position (numpy array 1x3)
#         if receiver_type == moving: #Time series with PVA
#             receiver_position (numpy array nx10)
#         if receiver_type == satellite: #TLE
#             receiver_position (list of str)

    import numpy as np
    
    i = 0 #line counter
    for line in receiver_file_id:
        line = line.split("=")      #Split the line
        line[0] = line[0].rstrip()  #Remove trailing whitespace on the field description
        
        if line[0] == "Receiver Name":
            receiver_name = line[1]
            i += 1
            continue
        
        if line[0] == "Receiver Type":
            receiver_type = line[1]
            i += 1
            continue
        
        if line[0] == "Receiver Observables":
            receiver_observables = line[1].split(",")
            i += 1
            continue
        
        if line[0] == "Receiver Clock Parameters":
            #To implement, placeholder
            receiver_clock_parameters = 0
            i += 1
            continue
        
        if line[0] == "Receiver Noise":
            receiver_noise = float(line[1])
            i += 1
            continue
        
        if line[0] == "Receiver Position":
            if receiver_type == "static":
                xyz = line[1].split(",")                                                            #Split the CSV field
                receiver_position = np.array([float(xyz[0]),float(xyz[1]),float(xyz[2])])           #Convert to float and store as numpy array
                receiver_position = receiver_position[np.newaxis,:]                                 #Convert array to row vector
            
            if receiver_type == "moving":
                #Not yet implemented, placeholder
                break
            
            if receiver_type == "satellite":
                #Not yet implemented, placeholder
                break
            
            i += 1
            continue
        
    
            
            
            
    #Input file sanity check
    try: receiver_name
    except NameError: return_code = -1
    
    try: receiver_type
    except NameError: return_code = -1
    
    try: receiver_observables
    except NameError: return_code = -1
    
    #Receiver clock parameters isn't required, skip
    
    try: receiver_noise
    except NameError: return_code = -1
    
    try: receiver_position
    except NameError: return_code = -1
    
    
    return(return_code, receiver_name, receiver_type, receiver_observables, receiver_clock_parameters, receiver_noise, receiver_position)
        