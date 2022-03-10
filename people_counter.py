from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time
import json
import paho.mqtt.publish as publish
import threading
from datetime import datetime, timezone


def current_millis():
    return round(time.time() * 1000)


def sleep_millis(ms):
    time.sleep(ms/1000)


def get_distance(sonar, ms_min_wait = 32):
    start = current_millis()

    distance = sonar.get_distance()

    end = current_millis()
    diff = end - start

    if diff < ms_min_wait:
        sleep_millis(ms_min_wait - diff)

    return distance


def person_infront(sonar):
    diff = abs(get_distance(sonar) -  100)
    return diff > 20


def send(payload):
    publish.single(topic, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                       auth={'username': mqtt_username, 'password': mqtt_password})


# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt.flespi.io"

# Your MQTT credentials for the device
mqtt_client_id = "mqtt-raspberry-pi-demo"
mqtt_username = "8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ"
mqtt_password = ""

topic = "fhnw/classroom/x/"

def on_entrance_event(change):
    payload = json.dumps({
        "time": datetime.now(tz=timezone.utc).isoformat(),
        "change": change
        })

    # attempt to publish this data to the topic.
    try:
        print("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
              mqtt_username, " PWD ", mqtt_password)
 
        t = threading.Thread(target=send, args=(payload,))
        t.daemon = True
        t.start()

    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(e)


sonarleft = GroveUltrasonicRanger(16)
sonarright = GroveUltrasonicRanger(5)


persons = 0

S = 0
# S=0: kein Sensor schlägt aus
# S=1: vor dem linken Sensor ist eine Person, vor dem rechten nicht.
# S=2: vor dem linken Sensor ist/war eine Person, vor dem rechten Sensor ist eine Person.
# S=3: vor dem rechten Sensor ist eine Person, vor dem linken nicht.
# S=4: vor dem rechten Sensor ist/wat eine Person, vor dem linken Sensor ist eine Person.

while True:
    left = person_infront(sonarleft)
    right = person_infront(sonarright)

#    current_milis = current_millis()
#    print(";".join([str(current_milis), str(left), str(right)]))


    if S == 0:
        if left: S = 1
        elif right: S = 3
    # persons comes from the left
    if S == 1:
        if right: S = 2
        elif left: pass # keep state S = 1
        else: S = 0
    if S == 2 and not right:
        S = 0
        persons += 1
        on_entrance_event(1)
    # same but person comes from the right
    if S == 3:
        if left: S = 4
        elif right: pass # keep state S = 3
        else: S = 0
    if S == 4 and not right:
        S = 0
        persons -= 1
        on_entrance_event(-1)


    print(persons)
