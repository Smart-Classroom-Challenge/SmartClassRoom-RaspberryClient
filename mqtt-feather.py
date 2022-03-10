import json
import adafruit_ble
from time import sleep
import paho.mqtt.publish as publish
from adafruit_ble.services.nordic import UARTService

# Bluetooth low energy
ble = adafruit_ble.BLERadio()
connection = None

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt.flespi.io"

# Your MQTT credentials for the device
mqtt_client_id = "mqtt-raspberry-pi-demo"
mqtt_username = "8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ"
mqtt_password = ""

topic = "fhnw/classroom/1/"

# Global sensor data
co2 = None
temperature = None
humidity = None
motion = None
light = None

while True:
    print("Scanning for an CIRCUITPY3137...")
    for adv in ble.start_scan(timeout=50, minimum_rssi=-80):
        if adv.complete_name == "CIRCUITPY3137":
            connection = ble.connect(adv)
            print("Connected to:", adv.complete_name)
            break
    ble.stop_scan()

    if connection and connection.connected:
        uart = connection[UARTService]
        while connection.connected:
            message = uart.read()
            if message != None:
                message = message.decode("utf-8").replace("\n", ";")
                if message != "":

                    # process valid data
                    message = message.split(";")
                    for val in message:
                        col = val.split(":")
                        if len(col) == 3:
                            if col[0] == "CO2":
                                co2 = col[1] 
                            if col[0] == "TEM":
                                temperature  = col[1] 
                            if col[0] == "HUM":
                                humidity = col[1] 
                            if col[0] == "MOT":
                                motion = col[1] 
                            if col[0] == "LIG":
                                light = col[1] 

                    # setup data for transmission
                    data = {
                        "co2": co2,
                        "temperature": temperature,
                        "humidity": humidity,
                        "motion": motion,
                        "light": light
                    } 
                    payload = json.dumps(data)

                    # attempt to publish this data to the topic.
                    try:
                        print("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
                            mqtt_username, " PWD ", mqtt_password)

                        publish.single(topic, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                                    auth={'username': mqtt_username, 'password': mqtt_password})
                        sleep(1)
                    except KeyboardInterrupt:
                        print("\nExiting.")
                        break
                    except Exception as e:
                        print(e)
