from time import sleep
from smbus2 import SMBus
import RPi.GPIO as GPIO
import signal
import sys
import random


i2c_ch = 1
interrupt_GPIO = 7

# ADC address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_conv = 0x00
reg_config = 0x01
threshHi_config = 0x11

#config msg
config_block = [0x00, 0xE0]
threshHi_block = [0x3C, 0xC0] ##[0x3C, 0xC0]

# Initialize I2C (SMBus)
bus = SMBus(i2c_ch)

#trigger for voltage spike
thresholdTrigger = False

#data window size
dataWindow = 1000

def triggerSwitch():
	thresholdTrigger = True
	print("triggered!")

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)

def captureData(dataList):
	listCounter = 0
	shiftedList = [0]*dataWindow
	for item in dataList:
		listCounter = listCounter + 1
		if item == "#":
			listStart = listCounter
			break

	j = 0
	for i in range(listCounter, dataWindow):
		shiftedList[j] = dataList[i]
		j = j + 1
	for i in range(0, listCounter):
		shiftedList[j] = dataList[i]
		j = j + 1
	writeToFile(shiftedList)
	##print(shiftedList[500])

def updateDataList(j, dataList):
	val = bus.read_i2c_block_data(i2c_address, 0, 2)
	valSum = (val[0]) * 16 + val[1]
	#valSum = j
	if valSum > 1000:
		valSum = 4335 - valSum
	if valSum > 10:
		##print(valSum)
		print(val)
		triggerSwitch()
		##prinxt(hex(val[0]), hex(val[1]))
	dataList[j] = valSum
	dataList[j+1] = "#"
	#print(valSum)
	return dataList

def writeToFile(dataList):
	#write to datafile
	f = open('datafile.csv', 'w')
	for item in dataList:
		f.write("%s\n" % item)
	f.close()

if __name__ == '__main__':
	#sets GPIO interrupt pin details
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(interrupt_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(interrupt_GPIO, GPIO.RISING, callback=triggerSwitch, bouncetime=100)
	#writes and confirms  configs
	bus.write_i2c_block_data(i2c_address, reg_config, config_block)
	print(bus.read_i2c_block_data(i2c_address, reg_config, 16))

	#writes and confirms threshold high values
	bus.write_i2c_block_data(i2c_address, threshHi_config, threshHi_block)
	print(bus.read_i2c_block_data(i2c_address, threshHi_config, 16))

	dataList = [0] * (dataWindow + 1)
	maxList = [0] * 990
	k = 190
	for l in range(0, 300):
	##while not thresholdTrigger:
		k = k + 1
		threshHi_block = [62, 192]

		bus.write_i2c_block_data(i2c_address, threshHi_config, threshHi_block)
		##print(bus.read_i2c_block_data(i2c_address, threshHi_config, 2))
		dataListSum = 0
		for i in range(10, 400):
			dataListSum = dataListSum + dataList[i]
		#dataListAvg = dataListAvg / 50
		print(dataListSum)
		maxList[l] = dataListSum
		for j in range(0, dataWindow):
			dataList = updateDataList(j, dataList)
			if thresholdTrigger:
				j = dataWindow
		for j in range(0, 500):
			dataList = updateDataList(j, dataList)
		captureData(dataList)

	##writeToFile(maxList)
	bus.close()
