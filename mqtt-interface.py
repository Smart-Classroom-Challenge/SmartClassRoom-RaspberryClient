from time import sleep
import json
import paho.mqtt.publish as publish

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt.flespi.io"

# Your MQTT credentials for the device
mqtt_client_id = "mqtt-raspberry-pi-demo"
mqtt_username = "8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ"
mqtt_password = ""

topic = "fhnw/classroom/x/"

while True:
    co2 = 1001
    temperature = 21.1
    humidity = 49
    motion = False
    light = 1034

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
        sleep(5)

    except KeyboardInterrupt:
        print("\nExiting.")
        break
    except Exception as e:
        print(e)
