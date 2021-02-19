import time
from rpi_ws281x import *
import random
import argparse

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

def train(strip, length, color, wait_time_ms=50, trailing=Color(0,0,0) ):
  for i in range(length):
    strip.setPixelColor(i, color)
    strip.show()
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, trailing)
    strip.setPixelColor(i + length, color)
    strip.show()
    time.sleep(wait_time_ms/1000)

def high_freq_flashing(strip, color, duration):
  for d in range(duration):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, color)
      strip.show()
    time.sleep(random.random())
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, Color(0,0,0))
      strip.show()
    time.sleep(random.random())

if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  high_freq_flashing(strip, Color(255,255,255), 10)
  train(strip, 10, Color(0,255,0))

  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,255,0))
  #   strip.show()
  #   time.sleep(0.1)
  #
  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,0,0))
  #   strip.show()
  #   time.sleep(0.1)

