import pytz
import json
import adafruit_ble
from time import sleep
from datetime import datetime
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
                message = message.decode("utf-8")
                if message != "":

                    # process valid data
                    data = {
                        "time": str(datetime.now(pytz.timezone("Europe/Zurich"))),
                        "co2": None,
                        "temperature": None,
                        "humidity": None,
                        "motion": None,
                        "light": None
                    }

                    message = message.split(";")
                    for val in message:
                        col = val.split(":")
                        if len(col) == 3:
                            if col[0] == "CO2":
                                data["co2"] = col[1] 
                            if col[0] == "TEM":
                                data["temperature"]  = float(col[1]) / 100
                            if col[0] == "HUM":
                                data["humidity"] = float(col[1]) / 100
                            if col[0] == "MOT":
                                data["motion"] = col[1] 
                            if col[0] == "LIG":
                                data["light"] = col[1] 

                    # setup data for transmission
                    payload = json.dumps(data)

                    # attempt to publish this data to the topic.
                    try:
                        if not (data["co2"] == None and data ["temperature"] == None and data["humidity"] == None and data["motion"] == None and data["light"] == None):
                            print("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
                                mqtt_username, " PWD ", mqtt_password)

                            publish.single(topic, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                                        auth={'username': mqtt_username, 'password': mqtt_password})
                    except KeyboardInterrupt:
                        print("\nExiting.")
                        break
                    except Exception as e:
                        print(e)