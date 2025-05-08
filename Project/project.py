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

# Light sensor and control thread
def light_thread():
    global MQTT_DATA_lux, PWM_LED  # Properly declare PWM_LED as global
    
    while not exit_event.is_set():
        try:
            # Measure BH1750 data
            lux = get_lux_value(bus, bh1750_address)
            
            # Store for MQTT
            MQTT_DATA_lux = lux
            
            # Print measurement
            print(f"Light: {lux:.1f} lux")
            
            # Adjust LED brightness based on measured lux
            if lux < goal_lux and PWM_LED < 100:
                PWM_LED = min(100, PWM_LED + 5)  # Increase brightness
                print(f"Too dim: increasing brightness to {PWM_LED}%, Current Lux: {lux:.1f}")
            elif lux > goal_lux and PWM_LED > 0:
                PWM_LED = max(0, PWM_LED - 5)  # Decrease brightness
                print(f"Too bright: decreasing brightness to {PWM_LED}%, Current Lux: {lux:.1f}")
            else:
                print(f"LED at stable brightness: {PWM_LED}%, Current Lux: {lux:.1f}")

            wiringpi.softPwmWrite(LED_PIN, PWM_LED)  # Apply PWM setting
            
            # Wait for next check
            time.sleep(interval)
            
        except Exception as e:
            print(f"Light thread error: {e}")
            time.sleep(5)  # Wait before retrying

# Temperature sensor and control thread
def temperature_thread():
    global MQTT_DATA_temp
    
    while not exit_event.is_set():
        try:
            # Measure BMP280 data
            temperature = bmp280.get_temperature()
            
            # Store for MQTT
            MQTT_DATA_temp = temperature
            
            # Print measurement
            print(f"Temperature: {temperature:.1f}°C")
            
            # Adjust fan based on temperature
            if temperature > goal_temp:
                wiringpi.digitalWrite(FAN_PIN, 1)  # Turn on fan
                print(f"Too hot: fan ON, Current Temp: {temperature:.1f}°C")
            else:
                wiringpi.digitalWrite(FAN_PIN, 0)  # Turn off fan
                print(f"Temperature OK: fan OFF, Current Temp: {temperature:.1f}°C")
                
            # Wait for next check
            time.sleep(interval)
            
        except Exception as e:
            print(f"Temperature thread error: {e}")
            time.sleep(5)  # Wait before retrying

# MQTT publishing thread
def mqtt_thread():
    while not exit_event.is_set():
        try:
            # Create the JSON data structure using global variables
            MQTT_DATA = f"field1={MQTT_DATA_lux}&field2={MQTT_DATA_temp}&field3={goal_lux}&field4={goal_temp}&status=MQTTPUBLISH"
            
            # Publish data to ThingSpeak
            client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False, properties=None)
            
            # Wait before next publish
            time.sleep(interval)
            
        except OSError as e:
            print(f"MQTT Error: {e}")
            client.reconnect()
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected MQTT error: {e}")
            time.sleep(5)

# Button input thread
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
            goal_temp = max(0, goal_temp - 1)
            print(f"Goal Temp decreased: {goal_temp}")
        if wiringpi.digitalRead(TEMP_MORE_PIN) == 1:
            goal_temp += 1
            print(f"Goal Temp increased: {goal_temp}")
        
        time.sleep(0.2)  # Prevent bouncing issues

# Variables
LIGHT_LESS_PIN = 7
LIGHT_MORE_PIN = 8
TEMP_LESS_PIN = 11
TEMP_MORE_PIN = 12
LED_PIN = 14
FAN_PIN = 3
goal_temp = 26
goal_lux = 10
PWM_LED = 0
exit_event = threading.Event()

# Variables for MQTT data
MQTT_DATA_lux = 0
MQTT_DATA_temp = 0

# PIN setup
wiringpi.wiringPiSetup()
wiringpi.pinMode(LIGHT_LESS_PIN, 0)
wiringpi.pinMode(LIGHT_MORE_PIN, 0)
wiringpi.pinMode(TEMP_LESS_PIN, 0)
wiringpi.pinMode(TEMP_MORE_PIN, 0)
wiringpi.pinMode(LED_PIN, 1)
wiringpi.pinMode(FAN_PIN, 1)

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
interval = 5  # Sample period in seconds

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

# Multithread setup with separate threads for each function
light_control = threading.Thread(target=light_thread)
temp_control = threading.Thread(target=temperature_thread)
button_input = threading.Thread(target=button_thread)
mqtt_publish = threading.Thread(target=mqtt_thread)

# Start all threads
light_control.start()
temp_control.start()
button_input.start()
mqtt_publish.start()

try:
    while True:
        time.sleep(interval)
except KeyboardInterrupt:
    print("Stopping threads...")
    exit_event.set()  # Signal threads to stop
    light_control.join()
    temp_control.join()
    button_input.join()
    mqtt_publish.join()
    print("Threads stopped. Exiting.")
    wiringpi.digitalWrite(FAN_PIN, 0) #Switch off fan
    wiringpi.softPwmWrite(LED_PIN, 0) #Switch off LED