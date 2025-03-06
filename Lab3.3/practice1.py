import time
import wiringpi
import sys

PIN = 14

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN, 0)

while True:
    if wiringpi.digitalRead(PIN) == wiringpi.LOW:
        print("Dark")
    else:
        print("Light")
    time.sleep(0.5)