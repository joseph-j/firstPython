from time import sleep
from smbus2 import SMBus

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_conv = 0x00
reg_config = 0x01

#config msg
config_block = [0x00, 0xE0]
dataList = [0]*1100

# Initialize I2C (SMBus)
bus = SMBus(i2c_ch)

#writes and confirms  configs
bus.write_i2c_block_data(i2c_address, reg_config, config_block)
print(bus.read_i2c_block_data(i2c_address, reg_config, 2))

# Send write bit
for j in range(0,1000):
	print(j, end=": ")
	val = bus.read_i2c_block_data(i2c_address, 0, 2)
	valSum = val[0] * 16 + val[1]
	if valSum > 2000:
		valSum = valSum - 3900
	#print(valSum)
	#dataList[0,j] = j
	dataList[j] = valSum
#write to datafile
f = open('datafile.txt', 'w')
#s = str(dataList)
for item in dataList:
	f.write("%s/n" % item)
f.close()

print(" ")
bus.close()
