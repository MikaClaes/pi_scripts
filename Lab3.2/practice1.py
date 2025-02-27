import time
import wiringpi as wp

def blink(pin):
    wp.digitalWrite(pin, 1)
    time.sleep(0.5)
    wp.digitalWrite(pin, 0)
    time.sleep(0.5)

# set pin numbers
LED_PIN = 3
SWITCH_PIN = 2

# initialize WiringPi
wp.wiringPiSetup()

# set up LED pin as output
wp.pinMode(LED_PIN, 1)

# set up switch pin as input
wp.pinMode(SWITCH_PIN, 0)


# Main
while True:
    if(wp.digitalRead(SWITCH_PIN) == 0):
        blink(LED_PIN)
        print("LED Blinks")
    else:
        print("LED not flashing")