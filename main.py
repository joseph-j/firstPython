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

#import time
import smbus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x08

# Register addresses
reg_temp = 0x00
reg_config = 0x01

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Initialize msg list
val = [0] * 10
# Send write bit
bus.write_i2c_block_data(i2c_address, reg_config, val)

# Read CONFIG to verify that we changed it
val = bus.read_i2c_block_data(i2c_address, reg_config, 10)
print("msg:", val)
