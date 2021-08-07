# -*- coding: utf-8 -*-
"""
dataParsing.py

Functions used to parse TLE, YUMA and other kinds of data
"""

def parseTLE(tleInput):
    
    import re
    
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
                if tleLine.group(1) != "2" or tleLine.group(2) != noradID:
                    print("Mismatched TLE line entries\n")
                    break
                
                #Inclination (degrees)
                inclination = float(tleLine.group(3))
                
                #Right Ascension of the Ascending Node
                RAAN = float(tleLine.group(4))
                
                #Eccentricity
                ecc = float("0."+tleLine.group(5))
                
                #Argument of perigee(degrees)
                argPerigee = float(tleLine.group(6))
                
                #Mean Anomaly (degrees)
                meanAnomally = float(tleLine.group(7))
                
                #Mean Motion (revolutions per day)
                meanMotion = float(tleLine.group(8))
                
                #Revolution number at epoch (revolutions)
                revolutionNumber = int(tleLine.group(9))
                
                #Checksum
                checksum2 = int(tleLine.group(10))
                
                i = 0 #Reset the counter
                
                #Save the data to the TLE array
                tleArray.append({'name':name, 'satID':noradID, 'epochY':epochYear, 'epoch':epoch, 'inc':inclination , 'raan':RAAN , 'ecc':ecc , 'argPer':argPerigee , 'anomMeanEpoch':meanAnomally , 'meanMotion':meanMotion})
                    
    return tleArray
                
            
        
        
        