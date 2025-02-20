import time
import wiringpi
import sys

def blink(_pin):
    wiringpi.digitalWrite(_pin, 1)  # Write HIGH to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 0)  # Write LOW to pin
    time.sleep(0.5)

# SETUP
print("Start")
pin = 2  # Define the GPIO pin
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin, 1)  # Set pin as OUTPUT

# MAIN
while True:
    blink(pin)

# CLEANUP
print("Done")