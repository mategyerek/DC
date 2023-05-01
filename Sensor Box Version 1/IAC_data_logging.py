# -*- coding: utf-8 -*-
"""
This program is used to load the data from the USB serial.
 Whenever the serial port receives data, it will be placed in
 the "line" variable. From here, it needs to be parsed and saved.
 
You can enable a "development" mode which will feed fake data 
 by setting dev = True
"""

import serial
import csv
import os
import time
from IAC_helper import port_scan, development_data

dev = True              # Development mode
usbPort = "editMe"      # Your USB port, obtain using port_scan()

rawFileName = "raw"
dataFileName = "output"

def calcDist(tof):
    return 0.5*299792458*tof/1000

def parse(line):
    row = line.split(" ")
    return [row[1], calcDist(float(row[3]))]


try:
    if not dev:
        ser = serial.Serial(usbPort, 9600)
    running = True
    print("Serial initialized succesfully!")
    
except:
    print("Issue with serial! Aborting...")


if dev:
    currentTime = time.time()

    try:
        os.remove(rawFileName)
        os.remove(dataFileName)
    except OSError:
        pass

    raw = open(rawFileName, 'a')
    csvfile = open(dataFileName, 'w')
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)

    fields = ['load_cell', 'Distance(meters)']
    csvwriter.writerow(fields)
    while running:
        # Delay 1 second
        while currentTime + 1 > time.time():
            pass
        currentTime = time.time()
        line = development_data()[:-2].decode('utf-8')
        print(line)
    
        raw.write(f"{line}\n")
        csvwriter.writerow(parse(line))
        

else:
    while running:
        line = ser.readline()[:-2].decode('utf-8')
        print(line)
        
        ####################
        ###YOUR CODE HERE###
        ####################