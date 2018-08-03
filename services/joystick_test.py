#!/usr/bin/env python

import smbus
import time

# i2c address of PCF8574
PCF8574=0x20

# open the bus (0 -- original Pi, 1 -- Rev 2 Pi)
b=smbus.SMBus(1)

# make certain the pins are set high so they can be used as inputs
b.write_byte(PCF8574, 0xff)

while 1:
    pins = b.read_byte(PCF8574)
    print("%02x" % pins)
    time.sleep(0.2)

