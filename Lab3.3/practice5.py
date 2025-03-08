import time
import wiringpi
import sys

GPIO1 = 1
GPIO2 = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(GPIO1, 1)
wiringpi.pinMode(GPIO2, 0)

while True:
    wiringpi.digitalWrite(GPIO1, wiringpi.HIGH)
    time.sleep(10e-6)
    wiringpi.digitalWrite(GPIO1, wiringpi.LOW)

    while not wiringpi.digitalRead(GPIO2):
        pass
    signal_high = time.time()
        
        # Wait for echo pin to go LOW
    while wiringpi.digitalRead(GPIO2):
        pass
    signal_low = time.time()
        
        # Calculate time passed and distance
    timepassed = signal_low - signal_high
    distance = timepassed * 17000
    print("Distance:", distance, "cm")
        
    time.sleep(0.5)