import time
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
	fileCounter = dataList[0]
	listCounter = 0
	shiftedList = [0]*dataWindow
	for item in dataList:
		listCounter = listCounter + 1
		if item == "#":
			listStart = listCounter
			break
	j = 0
	for i in range(listStart, dataWindow):
		shiftedList[j] = dataList[i]
		j = j + 1
	for i in range(0, listStart):
		shiftedList[j] = dataList[i]
		j = j + 1
	writeToFile(shiftedList, fileCounter)

def updateDataList(j, dataList):
	val = bus.read_i2c_block_data(i2c_address, 0, 2)
	valSum = (val[0]) * 16 + val[1]
	#valSum = j
	if valSum > 1000:
		valSum = 4335 - valSum
	if valSum > 10:
		##print(valSum)
		print(val)
		valSum = 100
		##triggerSwitch()
		dataList[0] = True
	dataList[j] = valSum
	dataList[j+1] = "#"
	#print(valSum)
	return dataList

def writeToFile(dataList, fileCounter):
	#write to datafile
	f = open('datafile' + str(fileCounter) + '.csv', 'w')
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
	dataList[0] = False
	thresholdTrigger = dataList[0]
	halfWindow = int(dataWindow / 4)
	threshHi_block = [62, 192]
	bus.write_i2c_block_data(i2c_address, threshHi_config, threshHi_block)
	for i in range(0, 10):
		thresholdTrigger = False
		while not thresholdTrigger:
			dataListSum = 0
			#for k in range(400, 800):
				#dataListSum = dataListSum + dataList[k]
			#print(dataListSum)
			print(i)
			for j in range(1, dataWindow):
				dataList = updateDataList(j, dataList)
				if dataList[0]:
					for h in range(1, halfWindow):
						dataList = updateDataList(h, dataList)
					j = dataWindow + 1
					break
			thresholdTrigger = dataList[0]
		dataList[0] = i
		captureData(dataList)
		time.sleep(3)
	bus.close()
