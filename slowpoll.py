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

# config msg
config_block = [0x00, 0xE0]
threshHi_block = [0x3C, 0xC0]

# Initialize I2C (SMBus)
bus = SMBus(i2c_ch)

# trigger for voltage spike
thresholdTrigger = False

# data window size
dataWindow = 1000


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def captureData(dataList):
    fileCounter = dataList[0]
    listCounter = 0
    dataWindow = len(dataList)
    shiftedList = [0] * dataWindow
    listStart = 0
    for item in dataList:
        listCounter = listCounter + 1
        if item == "#":
            listStart = listCounter
            break
    j = 0
    for i in range(listStart, dataWindow):
        shiftedList[j] = dataList[i]
        j = j + 1
    for i in range(0, (listStart - 1)):
        shiftedList[j] = dataList[i]
        j = j + 1
    writeToFile(shiftedList, fileCounter)


def updateDataList(j, dataList):
    val2 = [0] * 2
    val = bus.read_i2c_block_data(i2c_address, 0, 2)
    valSum = (val[0]) * 16 + val[1]
    if valSum > 1000:
        valSum = 4335 - valSum
    val2[0] = valSum
    val = bus.read_i2c_block_data(i2c_address, 4, 2)
    valSum = (val[0]) * 16 + val[1]
    if valSum > 1000:
        valSum = 4335 - valSum
    val2[1] = valSum

    dataList[j] = val2
    dataList[j + 1] = "#"
    return dataList


def writeToFile(dataList, fileCounter):
    # write to datafile
    f = open('slowPoll' + str(fileCounter) + '.csv', 'w')
    print('wrote: datafile' + str(fileCounter) + '.csv')
    for item in dataList:
        f.write("%s\n" % item)
    f.close()


if __name__ == '__main__':
    # sets GPIO interrupt pin details
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(interrupt_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(interrupt_GPIO, GPIO.RISING, callback=triggerSwitch, bouncetime=100)
    # writes and confirms  configs
    bus.write_i2c_block_data(i2c_address, reg_config, config_block)
    print(bus.read_i2c_block_data(i2c_address, reg_config, 16))

    # writes and confirms threshold high values
    bus.write_i2c_block_data(i2c_address, threshHi_config, threshHi_block)
    print(bus.read_i2c_block_data(i2c_address, threshHi_config, 16))
    n = 0
    dataSum = [0] * 10000
    dataList = [0] * (dataWindow + 1)
    dataList[0] = False
    thresholdTrigger = dataList[0]
    halfWindow = int(dataWindow / 2)
    threshHi_block = [62, 192]
    bus.write_i2c_block_data(i2c_address, threshHi_config, threshHi_block)
    bus.write_i2c_block_data(i2c_address, 0, [0, 0])

    for i in range(0, 2400):
        for j in range(1, dataWindow):
            dataList = updateDataList(j, dataList)
            if dataList[0]:
                for h in range(1, halfWindow):
                    dataList = updateDataList(h, dataList)
                j = dataWindow + 1
                break
        dataListSum = 0
        dataListSum2 = 0
        for k in range(10, 400):
            dataListNext = dataList[k][0]
            if isinstance(dataListNext, int):
                dataListSum = dataListSum + dataListNext
            dataListNext = dataList[k][1]
            if isinstance(dataListNext, int):
                dataListSum2 = dataListSum2 + dataListNext
        print(dataListSum, ", ", dataListSum2)
        dataSum[n] = dataListSum
        n = n + 1
        dataList[0] = i
        captureData(dataList)
        dataList = [0] * (dataWindow + 1)
        time.sleep(1)
    writeToFile(dataSum, 1)
    bus.close()
