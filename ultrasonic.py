from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonar = GroveUltrasonicRanger(16)

print('Detecting distance...')
while True:
    print('{} cm'.format(sonar.get_distance()))
    time.sleep(0.00001)
