# Just in case the environment variables were not properly set
import os
os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

import board
import busio
import time

import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802


kgperr = 0
testload = 0
r0 = 0
load = 0

# Load cell
loadCelSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

print("Starting measurements. \n")

# Perform measurements
try:
    while True:
        # Get sensor readings
        loadCellValue = loadCelSensor.read()
        tofValue = tofSensor.range

        if callibrated == False:
            if input("press 1 when no load is applied") == 1:
                r0 = loadCellValue# sensor value when no load is applied
                testload = input("Apply load to sensor and enter how much (N).")
                kgperr = testload / loadCelSensor.read() # the loading in kg that one lil sensor value is worth
                callibrated = True 
           
     
        load = 9.81(kgperr*loadCelSensor.read() - r0) # in newton
        

        # Output sensor data
        print("Load cell: {:.0f}, Distance: {:.0f}".format(load, tofValue))
        # print("Load cell: {:.0f}".format(loadCellValue))

        # Sleep
        time.sleep(1)

# Exit
except KeyboardInterrupt:
    print("\nexiting...\n")
