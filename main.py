import math
import time
from rpi_ws281x import *
import random
import argparse

LED_COUNT = 150
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

def flash(strip, color, count, interval):
  for d in range(count):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, color)
    strip.show()
    time.sleep(interval)
    clear(strip)
    strip.show()
    time.sleep(interval)

def clear(strip):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))
  strip.show();

def fill(strip, color):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
  strip.show();

def timer(strip, color, total_time):
  fill(strip, color)
  pixels = strip.numPixels()
  if total_time > pixels:
    time.sleep(math.ceil(float(total_time) / pixels))
    for i in range(0, pixels - math.ceil(pixels/float(total_time)), math.ceil(pixels/float(total_time))):
      for k in range(i,i + math.ceil(pixels/float(total_time))):
        strip.setPixelColor(k,Color(0,0,0))
      strip.show()
      time.sleep(math.ceil(float(total_time) / pixels))
  else:
    for i in range(0, pixels):
      strip.setPixelColor(i, Color(0, 0, 0))
      strip.show()
      time.sleep(float(total_time)/pixels)

  flash(strip, Color(255, 0, 0), 3, 0.5)


if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  # flash(strip, Color(255, 00, 0), 3, 0.5)
  timer(strip, Color(255, 255, 0), 30)

  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,255,0))
  #   strip.show()
  #   time.sleep(0.1)
  #
  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,0,0))
  #   strip.show()
  #   time.sleep(0.1)

