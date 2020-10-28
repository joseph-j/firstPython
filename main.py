

from time import sleep
from smbus2 import SMBus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_conv = 0x00
reg_config = 0x01

#config msg
config_byte1 = 0
config_byte2 = 224
config_block = [0x00, 0x00, 0xE0]
# Initialize I2C (SMBus)
#bus = smbus.SMBus(i2c_ch)
bus = SMBus(i2c_ch)

# Initialize msg list
val = [0] * 3

# Send write bit
for j in range(0,6):
	print("command = ", j)
	bus.write_byte_data(i2c_address, reg_config, j)
	for i in range(0,6):
		print(i, end=": ")
		print(bus.read_i2c_block_data(i2c_address, i, 3))
#bus.write_i2c_block_data(i2c_address, 0, config_block)
#bus.write_byte_data(i2c_address, 0, config_byte2)

# Read CONFIG to verify that we changed it
#val = bus.read_i2c_block_data(i2c_address, 0, 16)

#for i in range(0, 10):
	#val = bus.read_i2c_block_data(i2c_address, 0, 16)
	#print("msg:", val[0], ", ", val[1])
	#print(i, val[0]*16 + val[1])
	#print(i, end=": ")
	#sleep(0.03)
	#print("sum: ", val[0]*16 + val[1], end=": ")
	#print(val)
print(" ")
bus.close()
