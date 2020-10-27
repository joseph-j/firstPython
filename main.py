

from time import sleep
import smbus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_conv = 0x00
reg_config = 0x01

#config msg
config = [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0]

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Initialize msg list
val = [0] * 16

# Send write bit
bus.write_byte_data(i2c_address, 0, config)


# Read CONFIG to verify that we changed it
#val = bus.read_i2c_block_data(i2c_address, reg_conv, 10)
for i in range(0, 1000):
	val = bus.read_i2c_block_data(i2c_address, 0, 16)
	#print("msg:", val[0], ", ", val[1])
	#print(i, val[0]*16 + val[1])
	print(i, end=": ")
	#sleep(0.03)
	for j in range(0, 2):
		print(val[j], end=', ')
	print("sum: ", val[0]*16 + val[1])
