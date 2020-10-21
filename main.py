#main run module
#update channel
#   check voltage1
#   update list1
#   compare former/latter avg
#...2,3,4
#sum delta averages
#if sum delta > XX, comb thru to find which
#save out peak waveform to file
#repeat
###
#numChannel = 4
#rollingAvg = 20
#def readVoltage (ch)
    #readIO
#def updateChannel (ch)
#    avgList = []

# Uses the smbus2 library to send and receive data from a Jrk G2.
# Works on Linux with either Python 2 or Python 3.
#
# NOTE: The Jrk's input mode must be "Serial / I2C / USB".
# NOTE: For reliable operation on a Raspberry Pi, enable the i2c-gpio
#   overlay and use the I2C device it provides (usually /dev/i2c-3).
# NOTE: You might nee to change the 'SMBus(3)' line below to specify the
#   correct I2C device.
# NOTE: You might need to change the 'address = 11' line below to match
#   the device number of your Jrk.

import time
import smbus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x08

# Register addresses
reg_temp = 0x00
reg_config = 0x01

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Send write bit
bus.write_i2c_block_data(i2c_address, reg_config, val)

# Read CONFIG to verify that we changed it
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("msg:", val)