import time
import wiringpi
import sys

def blink(_pin1, _pin2, _pin3, _pin4):
    # L --> R
    wiringpi.digitalWrite(_pin1, 1)  # Write HIGH to pin
    wiringpi.digitalWrite(_pin3, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin1, 0)  # Write LOW to pin
    wiringpi.digitalWrite(_pin3, 0)
    time.sleep(0.5)
    
    wiringpi.digitalWrite(_pin2, 1)
    wiringpi.digitalWrite(_pin4, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin2, 0)
    wiringpi.digitalWrite(_pin4, 0)
    time.sleep(0.5)

# SETUP
print("Start")
pin1 = 2  # Define the GPIO pin
pin2 = 5
pin3 = 7
pin4 = 8
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin1, 1)  # Set pin as OUTPUT
wiringpi.pinMode(pin2, 1)
wiringpi.pinMode(pin3, 1)
wiringpi.pinMode(pin4, 1)

# MAIN
while True:
    blink(pin1, pin2, pin3, pin4)