#Imports
import time
from bmp280 import BMP280
from smbus2 import SMBus, i2c_msg
import paho.mqtt.client as mqtt

#Functions
def get_lux_value(bus, address):
    write = i2c_msg.write(address, [0x10])  # 1lx resolution 120ms see datasheet
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2  # conversion see datasheet

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected OK with result code " + str(rc))
    else:
        print("Bad connection with result code " + str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic + "; message: " + msg.payload)


# Create an I2C bus object
bus = SMBus(0)
bmp280_address = 0x77  # BMP280 address
bh1750_address = 0x23  # BH1750 address

# Setup BMP280
bmp280 = BMP280(i2c_addr=bmp280_address, i2c_dev=bus)

# Setup BH1750
bus.write_byte(bh1750_address, 0x10)  # 1lx resolution 120ms

# Sample interval
interval = 3  # Sample period in seconds

# MQTT settings
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "channels/2895287/publish"
MQTT_CLIENT_ID = "Mi09LjQRDCAaAAo4EjcwNDQ"
MQTT_USER = "Mi09LjQRDCAaAAo4EjcwNDQ"
MQTT_PWD = "ENwFrAWDjJxLfeYjRYAlJLBi"

# Set up a MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

# Connect callback handlers to client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Attempting to connect to %s" % MQTT_HOST)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()  # start the loop

while True:
    try:
        # Measure BMP280 data
        bmp280_temperature = bmp280.get_temperature()
        
        # Measure BH1750 data
        lux = get_lux_value(bus, bh1750_address)
        
        # Print measurements
        print("Light: %4.1f lux, Temperature: %4.1f°C," % 
              (lux, bmp280_temperature))
        
        # Create the JSON data structure with three fields
        MQTT_DATA = "field1=" + str(lux) + "&field2=" + str(bmp280_temperature) + "&status=MQTTPUBLISH"
        print(MQTT_DATA)
        
        # Publish data to ThingSpeak
        client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False, properties=None)
        
        # Wait for the next sample interval
        time.sleep(interval)
        
    except OSError as e:
        print(f"Error: {e}")
        client.reconnect()
        time.sleep(3)  # Wait a bit before trying again
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(3)  # Wait a bit before trying again