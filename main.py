from time import sleep
from smbus2 import SMBus
import RPi.GPIO as GPIO
import signal
import sys


i2c_ch = 1
interrupt_GPIO = 7

# ADC address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_conv = 0x00
reg_config = 0x01

#config msg
config_block = [0x00, 0xE0]
dataList = [0]*1100

# Initialize I2C (SMBus)
bus = SMBus(i2c_ch)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def captureData(dataList):
	listCounter = 0
	for item in dataList:
		listCounter = listCounter + 1
		if item = "#":
			listStart = listCounter
			break
	j = 0
	for i in range(listCounter, 1000):
		shiftedList[j] = datalist[i]
		j = j + 1
	j = 0
	for i in range 0, listCounter):
		shiftedList[j] = datalist[i]
		j = j + 1
	writeToFile(shiftedlist)

def updateDataList(j, dataList):
	val = bus.read_i2c_block_data(i2c_address, 0, 2)
	valSum = val[0] * 16 + val[1]
	if valSum > 3500:
		valSum = valSum - 3900
	dataList[j] = valSum
	datalist[j+1] = "#"
	return dataList

def writeToFile(datalist):
	#write to datafile
	f = open('datafile.csv', 'w')
	#s = str(dataList)
	for item in dataList:
		f.write("%s/n" % item)
	f.close()

if __name__ == '__main__':
    #sets GPIO interrupt pin details
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(interrupt_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(interrupt_GPIO, GPIO.FALLING, callback=captureData(), bouncetime=100)

	#writes and confirms  configs
	bus.write_i2c_block_data(i2c_address, reg_config, config_block)
	print(bus.read_i2c_block_data(i2c_address, reg_config, 2))
	while True:
		for j in range(0,1000):
			#print(j, end=": ")
			updateDataList(j, datalist)



	bus.close()
