

#import time
import smbus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x90

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
