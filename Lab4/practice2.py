import time
from smbus2 import SMBus, i2c_msg
import wiringpi as wp

#Create an I2C bus object
bus = SMBus(0)
address = 0x23 # i2c address

wp.wiringPiSetup()
LED1_PIN = 14
LED2_PIN = 12
wp.pinMode(LED1_PIN, 1)
wp.pinMode(LED2_PIN, 1)

#Setup BH1750
bus.write_byte(address, 0x10)
bytes_read = bytearray(2)

def get_value(bus, address):
    write = i2c_msg.write(address, [0x10]) # 1lx resolution 120ms see datasheet
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0]&3)<<8) + bytes_read[1])/1.2 # conversion see datasheet

while True:
    lux = get_value(bus, address)
    print("{:.2f} Lux".format(lux))
    if (lux < 300):
        wp.digitalWrite(LED1_PIN,1)
        wp.digitalWrite(LED2_PIN,0)
    else:
        wp.digitalWrite(LED1_PIN,0)
        wp.digitalWrite(LED2_PIN,1)
    time.sleep(1)
