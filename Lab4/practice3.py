import time
from smbus2 import SMBus, i2c_msg
import wiringpi as wp
import paho.mqtt.client as mqtt
import ssl

# Create an I2C bus object
bus = SMBus(0)
address = 0x23  # BH1750 i2c address

# Setup LED pins
wp.wiringPiSetup()
LED1_PIN = 14  # LED for low light
LED2_PIN = 12  # LED for high light
wp.pinMode(LED1_PIN, 1)
wp.pinMode(LED2_PIN, 1)

# Setup BH1750
bus.write_byte(address, 0x10)
bytes_read = bytearray(2)

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883  # Non-SSL port
MQTT_TOPIC = "sensors/light"
MQTT_CLIENT_ID = "light_sensor_client"

# Light threshold (in lux)
LIGHT_THRESHOLD = 300

def get_value(bus, address):
    write = i2c_msg.write(address, [0x10])  # 1lx resolution 120ms see datasheet
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2  # conversion see datasheet

# MQTT Callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")
    else:
        print(f"Failed to connect, return code: {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"Disconnected from MQTT broker, return code: {rc}")

def on_publish(client, userdata, mid, properties=None):
    print(f"Message published with ID: {mid}")

# Set up MQTT client
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Connect to MQTT broker
try:
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()  # Start the MQTT network loop in a separate thread
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Main loop
print("Starting light monitoring...")
while True:
    try:
        # Get light value from sensor
        lux = get_value(bus, address)
        print(f"{lux:.2f} Lux")
        
        # Control LEDs based on light level
        if lux < LIGHT_THRESHOLD:
            wp.digitalWrite(LED1_PIN, 1)  # Turn on LED1 (low light)
            wp.digitalWrite(LED2_PIN, 0)  # Turn off LED2
            light_status = "low"
        else:
            wp.digitalWrite(LED1_PIN, 0)  # Turn off LED1
            wp.digitalWrite(LED2_PIN, 1)  # Turn on LED2 (high light)
            light_status = "high"
        
        # Create MQTT message
        message = f'{{"lux": {lux:.2f}, "status": "{light_status}", "threshold": {LIGHT_THRESHOLD}}}'
        
        # Publish message to MQTT broker
        client.publish(MQTT_TOPIC, message, qos=1)
        
        # Wait before next reading
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Program stopped by user")
        client.loop_stop()
        client.disconnect()
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Wait before retrying