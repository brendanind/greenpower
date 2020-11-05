## Brendan's Greenpower code for the raspberry pi.

## Follow this: https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/blob/master/ADCPi/README.md
## To get the ADCPi library set up, you will have to git clone a repository and install it via pip3.

print("Init Code!")

ADDRESS1 = 0x68

## this is meant to be set to 0x69 but the raspberry pi doesnt
## seem to find any device on this address, maybe the second chip on the ADC is broken?
ADDRESS2 = 0x68

## This can be 12, 14, 16, or 18.
SAMPLRATE = 18

from ADCPi import ADCPi

## Create the adc object:
adc = ADCPi(ADDRESS1, ADDRESS1, SAMPLERATE)

def read(pin, adc = adc):
    return adc.read_voltage(pin)

def raw(pin, adc = adc):
    return adc.read_raw(pin)