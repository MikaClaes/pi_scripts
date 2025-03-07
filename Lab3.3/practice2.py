import time
import wiringpi
import sys

PIN_IN = 14
PIN_OUT = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_IN, 0)
wiringpi.pinMode(PIN_OUT, 1)

while True:
    if wiringpi.digitalRead(PIN_IN) == wiringpi.LOW:
        wiringpi.digitalWrite(PIN_OUT, 1)
        print("Light On")
    else:
        wiringpi.digitalWrite(PIN_OUT, 0)
        print("Light Off")
    time.sleep(0.5)