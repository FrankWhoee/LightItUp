import sys

import RPi.GPIO as GPIO
import relay
import time
from threading import Thread

starting = 0
ending = 0
current_distance = 0
down = False

# relay.cleanup(True)

def calculate_distance(pin):
    global ending
    global current_distance
    global down
    ending = time.time()
    current_distance = 17150 * (ending - starting) - 10
    if current_distance < 50:
        down = True
    if down and current_distance > 60:
        relay.toggle(relay.IN1)
        down = False



GPIO.add_event_detect(relay.U_ECHO, GPIO.FALLING, callback=calculate_distance, bouncetime=300)


def get_distance():
    global current_distance
    global starting
    GPIO.setup(relay.U_TRIG, GPIO.OUT)
    relay.on(relay.U_TRIG)
    starting = time.time()
    time.sleep(0.000001)
    relay.off(relay.U_TRIG)

def collect_distance():
    global current_distance
    try:
        while True:
            get_distance()
            time.sleep(0.01)
    except:
        GPIO.cleanup()

Thread(target=collect_distance).start()