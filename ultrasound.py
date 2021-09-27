import RPi.GPIO as GPIO
import relay
import time
from threading import Timer

starting = 0
ending = 0

# relay.cleanup(True)

def calculate_distance():
    ending = time.time()
    distance = 17000 * (ending - starting)
    print("distance: " + str(distance) + "cm")
    t = Timer(0.1, get_distance)
    t.start()

def get_distance():
    global starting
    starting = time.time()
    GPIO.setup(relay.U_TRIG, GPIO.OUT)
    relay.on(relay.U_TRIG)
    time.sleep(0.01)
    relay.off(relay.U_TRIG)
    GPIO.add_event_detect(relay.U_ECHO, GPIO.BOTH, callback=calculate_distance, bouncetime=5)

time.sleep(5)
print("US started.")
get_distance()

time.sleep(30)
GPIO.cleanup()