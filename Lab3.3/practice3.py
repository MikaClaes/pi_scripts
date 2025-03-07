import time
import wiringpi
import sys

def lightOn():
    wiringpi.digitalWrite(PIN_OUT, 1)
    print("Light On")

PIN_OUT = 16
SWITCH_PIN = 14
LDR_PIN = 12

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_OUT, 1)
wiringpi.pinMode(SWITCH_PIN, 0)
wiringpi.pinMode(LDR_PIN, 0)

while True:
    if wiringpi.digitalRead(LDR_PIN) == wiringpi.LOW:
        lightOn()
    elif(wiringpi.digitalRead(SWITCH_PIN) == 1):
        lightOn()
    else:
        wiringpi.digitalWrite(PIN_OUT, 0)
        print("Light Off")
    time.sleep(0.5)