import time
from rpi_ws281x import *
import argparse

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  
  for i in range(strip.numPixels()):
    strip.setPixelColor(i,Color(0,255,0))
    strip.show()
    time.sleep(0.5)
    
  for i in range(strip.numPixels()):
    strip.setPixelColor(i,Color(0,0,0))
    strip.show()
    time.sleep(0.5)
