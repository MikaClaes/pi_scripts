import time
import wiringpi
import sys

def blink(_pin):
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(0.5)
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(0.5)
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(1.5)
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(0.5)
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(0.5)
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(0.5)
    time.sleep(1)
    

# SETUP
print("Start")
pin = 2
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin, 1)

# MAIN
while True:
    blink(pin)