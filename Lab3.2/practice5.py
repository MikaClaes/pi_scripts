import time
import wiringpi
import sys

def blinkR(_PIN1, _PIN2, _PIN3, _PIN4):
    wiringpi.digitalWrite(_PIN1, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN1, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN2, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN2, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN3, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN3, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN4, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN4, 0)
    time.sleep(0.5)

def blinkL(_PIN1, _PIN2, _PIN3, _PIN4):
    wiringpi.digitalWrite(_PIN4, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN4, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN3, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN3, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN2, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN2, 0)
    time.sleep(0.5)

    wiringpi.digitalWrite(_PIN1, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(_PIN1, 0)
    time.sleep(0.5)

L1_PIN = 5
L2_PIN = 7
L3_PIN = 8
L4_PIN = 11
SWITCH_PIN = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(SWITCH_PIN, 0)
wiringpi.pinMode(L1_PIN, 1)
wiringpi.pinMode(L2_PIN, 1)
wiringpi.pinMode(L3_PIN, 1)
wiringpi.pinMode(L4_PIN, 1)

while True:
    if(wiringpi.digitalRead(SWITCH_PIN) == 1):
        blinkL(L1_PIN, L2_PIN, L3_PIN, L4_PIN)
    else:
        blinkR(L1_PIN, L2_PIN, L3_PIN, L4_PIN)