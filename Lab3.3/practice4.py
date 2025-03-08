import time
import wiringpi
import sys

PIN = 14

wiringpi.wiringPiSetup()

while True:
    wiringpi.pinMode(PIN, 1)
    wiringpi.digitalWrite(PIN, wiringpi.LOW)
    time.sleep(0.1)

    wiringpi.pinMode(PIN, 0)
    starttime = time.time()
    while wiringpi.digitalRead(PIN) == wiringpi.LOW:
        pass
    stoptime = time.time()

    interval = stoptime - starttime
    print(interval)