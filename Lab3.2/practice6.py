import time
import wiringpi
import sys

L1_PIN = 5
L2_PIN = 7
SWITCH1_PIN = 1
SWITCH2_PIN = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(SWITCH1_PIN, 0)
wiringpi.pinMode(SWITCH2_PIN, 0)
wiringpi.pinMode(L1_PIN, 1)
wiringpi.pinMode(L2_PIN, 1)

#Switch off to start
wiringpi.digitalWrite(L1_PIN, 1)
wiringpi.digitalWrite(L2_PIN, 1)

#main
while True:
    if(wiringpi.digitalRead(SWITCH1_PIN) == 1):
        wiringpi.digitalWrite(L1_PIN, 0)
    elif(wiringpi.digitalRead(SWITCH2_PIN) == 1):
        wiringpi.digitalWrite(L2_PIN, 0)
    else:
        wiringpi.digitalWrite(L1_PIN, 1)
        wiringpi.digitalWrite(L2_PIN, 1)