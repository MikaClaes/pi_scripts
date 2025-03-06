import time
import wiringpi
import sys

def step_sequence():
    steps = [
        (1, 1, 0, 0),  # Step 1
        (0, 1, 1, 0),  # Step 2
        (0, 0, 1, 1),  # Step 3
        (1, 0, 0, 1)   # Step 4
    ]
    
    for step in steps:
        wiringpi.digitalWrite(PIN1, step[0])
        wiringpi.digitalWrite(PIN2, step[1])
        wiringpi.digitalWrite(PIN3, step[2])
        wiringpi.digitalWrite(PIN4, step[3])
        time.sleep(0.01)

PIN1 = 8
PIN2 = 11
PIN3 = 12
PIN4 = 14

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN1, 1)
wiringpi.pinMode(PIN2, 1)
wiringpi.pinMode(PIN3, 1)
wiringpi.pinMode(PIN4, 1)


try:
    while True:
        step_sequence()
except KeyboardInterrupt:
    wiringpi.digitalWrite(PIN1, 0)
    wiringpi.digitalWrite(PIN2, 0)
    wiringpi.digitalWrite(PIN3, 0)
    wiringpi.digitalWrite(PIN4, 0)
    print("\nStepper motor stopped.")
    sys.exit(0)
