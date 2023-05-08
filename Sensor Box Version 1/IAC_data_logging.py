# -*- coding: utf-8 -*-
"""
This program is used to load the data from the USB serial.
 Whenever the serial port receives data, it will be placed in
 the "line" variable. From here, it needs to be parsed and saved.
 
You can enable a "development" mode which will feed fake data 
 by setting dev = True
"""
import time
import serial
import csv
import os
import time
from IAC_helper import port_scan, development_data
from fileHandler import initWrite

time0_set = False
callibrated = False
kgperr = 0
r0 = 0
testload = 0
dev = False              # Development mode
usbPort = "editMe"      # Your USB port, obtain using port_scan()

def calcDist(tof):
    return 0.5*299792458*tof/1000

def parse(line):
    row = line.split(" ")
    return [row[1], calcDist(float(row[3]))]


raw, csvwriter = initWrite(dev, "output")
try:
    if not dev:
        ser = serial.Serial(usbPort, 9600)
    running = True
    print("Serial initialized succesfully!")
    
except:
    print("Issue with serial! Aborting...")

if dev:
    currentTime = time.time()

 

    fields = ['load_cell', 'Distance(meters)']
    csvwriter.writerow(fields)
    while running:
        # Delay 1 second
        while currentTime + 1 > time.time():
            pass


        currentTime = time.time()
        line = development_data()[:-2].decode('utf-8')
        if time0_set == False:
            time0 = time.time()
            time0_set = True
        line += str(' time: ')
        line += str(time.time() - time0)
        print(line)
    
        raw.write(f"{line}\n")
        csvwriter.writerow(parse(line))
        

else:
    while True:

        if callibrated == False:
            if input("press 1 when no load is applied") == 1:
                r0 = parse(line)[0] # sensor value when no load is applied
                testload = input("Apply load to sensor and enter how much (N).")
                line = ser.readline()[:-2].decode('utf-8')
                kgperr = testload / (parse(line)[0] - r0) # the loading in kg that one lil sensor value is worth
                callibrated = True 

        line = ser.readline()[:-2].decode('utf-8')
        if time0_set == False:
            time0 = time.time()
            time0_set = True
        line += str(' time: ')
        line += str(time.time() - time0)
        load = 9.81(kgperr*parse(line)[0] - r0) # in newton
        csvwriter.writerow([load , parse(line)])
        
        ####################
        ###YOUR CODE HERE###
        ####################
#print("Readyyyyyyyyyyyy")