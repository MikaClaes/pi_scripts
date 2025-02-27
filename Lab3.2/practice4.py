import time
import wiringpi
import sys

def blink(_pin):
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(0.5)
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(0.5)
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(1.5)
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(0.5)
    for i in range(0,3):
        wiringpi.digitalWrite(_pin, 0)
        time.sleep(0.5)
        wiringpi.digitalWrite(_pin, 1)
        time.sleep(0.5)
    time.sleep(1)
    

# SETUP
print("Start")
LED_PIN = 3
SWITCH_PIN = 2
wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, 1)
wiringpi.pinMode(SWITCH_PIN, 0)

# MAIN
while True:
    if(wiringpi.digitalRead(SWITCH_PIN) == 1):
        blink(LED_PIN)