import paho.mqtt.publish as publish

# The ThingSpeak Channel ID.
channel_ID = "1665323"

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_id = "AA0aHiQwMQALKwAmNSUDDSw"
mqtt_username = "AA0aHiQwMQALKwAmNSUDDSw"
mqtt_password = "iN3I1ElEOoAot/p1+0n6RPTd"

t_transport = "websockets"
t_port = 80

topic = "channels/" + channel_ID + "/publish"

while True:
    co2 = 1332
    temperature = 21.1
    humidity = 49

    # build the payload string.
    payload = "field1=" + str(co2) + "&field2=" + str(temperature) + "&field3=" + str(humidity)

    # attempt to publish this data to the topic.
    try:
        print("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
              mqtt_username, " PWD ", mqtt_password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_id,
                       auth={'username': mqtt_username, 'password': mqtt_password})
    except KeyboardInterrupt:
        print("\nExiting.")
        break
    except Exception as e:
        print(e)
