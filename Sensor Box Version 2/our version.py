# Just in case the environment variables were not properly set
# Just in case the environment variables were not properly set
from cedargrove_nau7802 import NAU7802
import adafruit_vl53l0x
import time
import busio
import board
import os
from fileHandler import initWrite

os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"


# Load cell
loadCelSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

calibrated = False
kgperr = 0
testload = 0
r0 = 0
load = 0
t = 0
raw, csv = initWrite(False, "output")

print("Starting measurements. \n")

# Perform measurements
try:
    while True:
        # Get sensor readings

        tofValue = tofSensor.range
        
        if calibrated == False:
            if input("press 1 when no load is applied") == "1":
                r0 = loadCelSensor.read()  # sensor value when no load is applied
                testload = float(input(
                    "Apply load to sensor and enter how much (kg)."))*9.81
                # the loading in kg that one lil sensor value is worth
                kgperr = testload / (loadCelSensor.read()-r0)
                calibrated = True
                t=0
            else:
                print("Incorrect key")

        loadCellValue = loadCelSensor.read()
        load = (loadCellValue-r0)*kgperr  # in newton
        
        # Output sensor data
        print(f"Time: {t}, Load cell: {loadCellValue}, Distance: {tofValue}, Load: {load}")
        # print("Load cell: {:.0f}".format(loadCellValue))
        raw.write(f"Time: {t}, Load cell: {loadCellValue}, Distance: {tofValue}, Load: {load}\n")
        csv.writerow([t, loadCellValue, tofValue, load])
        # Sleep
        time.sleep(1)
        t=t+1

# Exit
except KeyboardInterrupt:
    print("\nexiting...\n")
