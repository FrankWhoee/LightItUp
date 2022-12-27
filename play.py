import threading

from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO

"""
File is for playing with the LED strip.
"""

# LED strip configuration:
LED_COUNT = 150        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

GPIO.setmode(GPIO.BCM)

# Room Light Sensor
GPIO.setup(17, GPIO.IN)

# Window Light Sensor
GPIO.setup(27, GPIO.IN)

isNight = False

def setColour(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def setBrightness(strip, brightness):
    """Wipe color across display a pixel at a time."""
    c = Color(int(255 * brightness), int(255 * brightness), int(200 * brightness))
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, c)
    strip.show()

def pixelCounter(strip):
    i = 0
    cancel = False
    while not cancel:
        strip.setPixelColor(i, Color(125, 0, 0))
        strip.show()
        i += 1
        if(input() == "c"):
            cancel = True
    print("We have {} pixels".format(i))

def brightnessTester(strip):
    b = 0
    cancel = False
    while not cancel:
        setBrightness(strip, b)
        strip.show()
        b += 0.01
        print(b)
        if(input() == "c"):
            cancel = True
    print("We have {} brightness".format(b))

def checkRoom():
    return GPIO.input(17) == 1

def checkWindow():
    return GPIO.input(27) == 1

def lightUpOnTooDark(strip):
    while True:
        if checkWindow():
            setBrightness(strip, 0.8)
        else:
            setBrightness(strip, 0)
# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

if __name__ == "__main__":
    # brightnessTester(strip)
    setBrightness(strip, 0)