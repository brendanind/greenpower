#!/usr/bin/env python
# read abelectronics ADC Pi V2 board inputs with repeating reading from each channel.
# # Requries Python 2.7
# Requires SMBus
# I2C API depends on I2C support in the kernel

# Version 1.0  - 06/02/2013
# Version History:
# 1.0 - Initial Release

#
# Usage: changechannel(address, hexvalue) to change to new channel on adc chips
# Usage: getadcreading(address, hexvalue) to return value in volts from selected channel.
#
# address = adc_address1 or adc_address2 - Hex address of I2C chips as configured by board header pins.

from smbus import SMBus
import re

adc_address1 = 0x68
adc_address2 = 0x69

# create byte array and fill with initial values to define size
adcreading = bytearray()

adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)

# LSB = 15.625 * 10**(-6) # uV
# LSB = 62.5 * 10**(-6) # uV
Vref = 2.048
LSB = (2 * Vref) / 2 ** 12

# voltage_divider = (9.99 / (9.99 + 6.8))
voltage_divider = (6.8 / (9.99 + 6.8))

# detect i2C port number and assign to i2c_bus
# for line in open('/proc/cpuinfo').readlines():
#     m = re.match('(.*?)\s*:\s*(.*)', line)
#     if m:
#         (name, value) = (m.group(1), m.group(2))
#         if name == "Revision":
#             if value [-4:] in ('0002', '0003'):
#                 i2c_bus = 0
#             else:
#                 i2c_bus = 1
#             break

shunt_r = 54.7
bus = SMBus(1)


def changechannel(address, adcConfig):
    tmp = bus.write_byte(address, adcConfig)


def quickadcreading(address, adcConfig):
    adcreading = bus.read_i2c_block_data(address, adcConfig)
    h = adcreading[0]
    m = adcreading[1]
    s = adcreading[2]

    # shift bits to product result
    t = ((h & 0b00111111) << 8) | (m)
    # check if positive or negative number and invert if needed
    if (h > 0b01000000):
        t = ~(0x004000 - t)
    return t


def getadcreading(address, adcConfig):
    adcreading = bus.read_i2c_block_data(address, adcConfig)
    h = adcreading[0]
    m = adcreading[1]
    s = adcreading[2]
    # wait for new data
    while (s & 128):
        adcreading = bus.read_i2c_block_data(address, adcConfig)
        h = adcreading[0]
        m = adcreading[1]
        s = adcreading[2]

    # shift bits to product result
    t = ((h & 0b00111111) << 8) | (m)
    # check if positive or negative number and invert if needed
    if (h > 0b01000000):
        t = ~(0x004000 - t)
    return t


while True:
    v = getadcreading(adc_address1, 0xB0) * LSB / voltage_divider
    # getadcreading(adc_address1, 0x93)
    for i in range(60):
        shunt_v = getadcreading(adc_address1, 0x93) * LSB / 8
        shunt_i = shunt_v / shunt_r
        # print ("Channel 1: %0.2fuA, %0.2fuW, %0.2fV, %0.2fmV" % (shunt_i * 10**6, shunt_i*v* 10**6, v, shunt_v * 10**3))
        my_i = (shunt_i * 10 ** 6)
        print(("%7.2fuA: " % (my_i)) + ("-" * int(my_i / 14)))
