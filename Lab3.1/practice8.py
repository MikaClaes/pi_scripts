import wiringpi
import time

def fade(_pin1, _pin2, _pin3, _pin4):
    stage1 = 100
    stage2 = 75
    stage3 = 50
    stage4 = 25
    

    

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

#MAIN
fade()