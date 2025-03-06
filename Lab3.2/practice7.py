import time
import wiringpi
import sys

PIN1 = 8
PIN2 = 11
PIN3 = 12
PIN4 = 14

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN1, 1)
wiringpi.pinMode(PIN2, 1)
wiringpi.pinMode(PIN3, 1)
wiringpi.pinMode(PIN4, 1)

while True:
    wiringpi.digitalWrite(PIN1, 1)
    time.sleep(0.01)
    wiringpi.digitalWrite(PIN1, 0)

    wiringpi.digitalWrite(PIN2, 1)
    time.sleep(0.01)
    wiringpi.digitalWrite(PIN2, 0)

    wiringpi.digitalWrite(PIN3, 1)
    time.sleep(0.01)
    wiringpi.digitalWrite(PIN3, 0)

    wiringpi.digitalWrite(PIN4, 1)
    time.sleep(0.01)
    wiringpi.digitalWrite(PIN4, 0)
