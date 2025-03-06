import time
import wiringpi
import sys

PIN1 = 8
PIN2 = 11
PIN3 = 12
PIN4 = 14
BUTTON_PIN = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN1, 1)
wiringpi.pinMode(PIN2, 1)
wiringpi.pinMode(PIN3, 1)
wiringpi.pinMode(PIN4, 1)
wiringpi.pinMode(BUTTON_PIN, 0)
wiringpi.pullUpDnControl(BUTTON_PIN, 2)

steps_forward = [
    (1, 0, 0, 0),  # Step 1
    (0, 1, 0, 0),  # Step 2
    (0, 0, 1, 0),  # Step 3
    (0, 0, 0, 1)   # Step 4
]

steps_backward = list(reversed(steps_forward))

def step_sequence(steps):
    for step in steps:
        wiringpi.digitalWrite(PIN1, step[0])
        wiringpi.digitalWrite(PIN2, step[1])
        wiringpi.digitalWrite(PIN3, step[2])
        wiringpi.digitalWrite(PIN4, step[3])
        time.sleep(0.01)

try:
    while True:
        if wiringpi.digitalRead(BUTTON_PIN) == 1:
            step_sequence(steps_backward)
        else:
            step_sequence(steps_forward)
except KeyboardInterrupt:
    wiringpi.digitalWrite(PIN1, 0)
    wiringpi.digitalWrite(PIN2, 0)
    wiringpi.digitalWrite(PIN3, 0)
    wiringpi.digitalWrite(PIN4, 0)
    print("\nStepper motor stopped.")
    sys.exit(0)
