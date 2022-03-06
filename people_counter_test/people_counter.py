from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonarleft = GroveUltrasonicRanger(16)
sonarright = GroveUltrasonicRanger(5)

def current_millis():
    return round(time.time() * 1000)

def sleep_millis(ms):
    time.sleep(ms/1000)

while True:
    start = current_millis()

    left = sonarleft.get_distance()

    end = current_millis()
    diff = end - start

    if diff < 10:
        sleep_millis(10 - diff)
    # 0.002 doesn't work # make this an absolute value (e.g. since start of last measurement, not end)


    start = current_millis()

    right = sonarright.get_distance()
    current_milis = current_millis()
    print(";".join([str(current_milis), str(left), str(right)]))

    end = current_millis()
    diff = end - start

    if diff < 10:
        sleep_millis(10 - diff)

