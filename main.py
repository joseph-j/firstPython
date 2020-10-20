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

from smbus2 import SMBus, i2c_msg


class JrkG2I2C(object):
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    # Sets the target.  For more information about what this command does,
    # see the "Set Target" command in the "Command reference" section of
    # the Jrk G2 user's guide.
    def set_target(self, target):
        command = [0xC0 + (target & 0x1F), (target >> 5) & 0x7F]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    # Gets one or more variables from the Jrk (without clearing them).
    # Returns a list of byte values (integers between 0 and 255).
    def get_variables(self, offset, length):
        write = i2c_msg.write(self.address, [0xE5, offset])
        read = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(write, read)
        return list(read)

    # Gets the Target variable from the Jrk.
    def get_target(self):
        b = self.get_variables(0x02, 2)
        return b[0] + 256 * b[1]

    # Gets the Feedback variable from the Jrk.
    def get_feedback(self):
        b = self.get_variables(0x04, 2)
        return b[0] + 256 * b[1]


# Open a handle to "/dev/i2c-3", representing the I2C bus.
bus = SMBus(3)

# Select the I2C address of the Jrk (the device number).
address = 11

jrk = JrkG2I2C(bus, address)

feedback = jrk.get_feedback()
print("Feedback is {}.".format(feedback))

target = jrk.get_target()
print("Target is {}.".format(target))

new_target = 2248 if target < 2048 else 1848
print("Setting target to {}.".format(new_target))
jrk.set_target(new_target)