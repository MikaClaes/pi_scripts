# Imports
import wiringpi
import time
import threading
from bmp280 import BMP280
from smbus2 import SMBus, i2c_msg
import paho.mqtt.client as mqtt

# Functions
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

def adjust_led_brightness(lux):
    """Adjust LED brightness using Soft PWM based on measured lux."""
    global goal_lux
    
    if lux < goal_lux:
        brightness = min(100, (goal_lux - lux) * 2)  # Increase brightness
    else:
        brightness = max(0, 100 - (lux - goal_lux) * 2)  # Decrease brightness

    brightness = max(0, min(100, brightness))  # Keep brightness within 0-100
    wiringpi.softPwmWrite(LED_PIN, brightness)
    print(f"Lux: {lux}, Goal: {goal_lux}, LED Brightness: {brightness}%")

# Sensor function
def sensor_thread():
    while not exit_event.is_set():
        try:
            # Measure BMP280 data
            bmp280_temperature = bmp280.get_temperature()
        
            # Measure BH1750 data
            lux = get_lux_value(bus, bh1750_address)
        
            # Print measurements
            print("Light: %4.1f lux, Temperature: %4.1f°C," % 
            (lux, bmp280_temperature))
        
            # Create the JSON data structure
            MQTT_DATA = f"field1={lux}&field2={bmp280_temperature}&status=MQTTPUBLISH"
            print(MQTT_DATA)
        
            # Publish data to ThingSpeak
            client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False, properties=None)

            # Adjust LED brightness
            adjust_led_brightness(lux)

            # Wait for the next sample interval
            time.sleep(interval)
        
        except OSError as e:
            print(f"Error: {e}")
            client.reconnect()
            time.sleep(5)  # Wait a bit before trying again
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)  # Wait a bit before trying again

def button_thread():
    global goal_lux, goal_temp

    while not exit_event.is_set():
        if wiringpi.digitalRead(LIGHT_LESS_PIN) == 1:
            goal_lux = max(0, goal_lux - 10)
            print(f"Goal Lux decreased: {goal_lux}")
        if wiringpi.digitalRead(LIGHT_MORE_PIN) == 1:
            goal_lux += 10
            print(f"Goal Lux increased: {goal_lux}")
        if wiringpi.digitalRead(TEMP_LESS_PIN) == 1:
            goal_temp = max(0, goal_temp - 2)
            print(f"Goal Temp decreased: {goal_temp}")
        if wiringpi.digitalRead(TEMP_MORE_PIN) == 1:
            goal_temp += 2
            print(f"Goal Temp increased: {goal_temp}")
        
        time.sleep(0.2)  # Prevent bouncing issues

# Variables
LIGHT_LESS_PIN = 7
LIGHT_MORE_PIN = 8
TEMP_LESS_PIN = 11
TEMP_MORE_PIN = 12
LED_PIN = 14
goal_temp = 26
goal_lux = 260
exit_event = threading.Event()

# PIN setup
wiringpi.wiringPiSetup()
wiringpi.pinMode(LIGHT_LESS_PIN, 0)
wiringpi.pinMode(LIGHT_MORE_PIN, 0)
wiringpi.pinMode(TEMP_LESS_PIN, 0)
wiringpi.pinMode(TEMP_MORE_PIN, 0)
wiringpi.pinMode(LED_PIN, 1)

# Enable Soft PWM on LED_PIN
wiringpi.softPwmCreate(LED_PIN, 0, 100)  # PWM range 0-100

# Create an I2C bus object
bus = SMBus(0)
bmp280_address = 0x77  # BMP280 address
bh1750_address = 0x23  # BH1750 address

# Setup BMP280
bmp280 = BMP280(i2c_addr=bmp280_address, i2c_dev=bus)

# Setup BH1750
bus.write_byte(bh1750_address, 0x10)  # 1lx resolution 120ms

# Sample interval
interval = 15  # Sample period in seconds

# MQTT settings
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "channels/2895287/publish"
MQTT_CLIENT_ID = "Mi09LjQRDCAaAAo4EjcwNDQ"
MQTT_USER = "Mi09LjQRDCAaAAo4EjcwNDQ"
MQTT_PWD = "ENwFrAWDjJxLfeYjRYAlJLBi"

# Set up an MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PWD)

# Connect callback handlers to client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f"Attempting to connect to {MQTT_HOST}")
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()  # Start the loop

# Multithread setup
t1 = threading.Thread(target=sensor_thread)  # Read sensors
t2 = threading.Thread(target=button_thread)  # Read button inputs

# Start the threads
t1.start()
t2.start()

try:
    while True:
        print(f"Goal Temp: {goal_temp}, Goal Lux: {goal_lux}")
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping threads...")
    exit_event.set()  # Signal threads to stop
    t1.join()
    t2.join()
    print("Threads stopped. Exiting.")
