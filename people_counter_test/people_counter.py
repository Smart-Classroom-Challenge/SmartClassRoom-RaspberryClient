from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonarleft = GroveUltrasonicRanger(16)
sonarright = GroveUltrasonicRanger(5)


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
    # same but person comes from the right
    if S == 3:
        if left: S = 4
        elif right: pass # keep state S = 3
        else: S = 0
    if S == 4 and not right:
        S = 0
        persons -= 1


    print(persons)
