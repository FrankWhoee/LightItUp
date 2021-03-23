import json
import math
import os
import time
from rpi_ws281x import *
import random
import discord
import numpy as np
from sunx import get_sunset_delay
import argparse
from threading import Timer

# TODO: Implement sunset reminders
# https://sunrise-sunset.org/api
# https://docs.python.org/3/library/threading.html#timer-objects

# Extract secrets from local file.
if os.path.exists("secrets.json"):
  with open("secrets.json") as f:
    secrets = json.load(f)
else:
  secrets = {}
  secrets["token"] = os.environ.get("token")

# Instantiate discord.py Client
TOKEN = secrets["token"]
client = discord.Client()

prefix = "`"

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

def fade(strip, color1, color2, interval):
  max_diff = max(tuple(np.absolute(np.subtract(color2, color1))))
  diff = tuple(np.subtract(color2, color1))
  r = color1[0]
  g = color1[1]
  b = color1[2]
  for i in range(max_diff):
    fill(strip, Color(int(math.floor(r)),int(math.floor(g)),int(math.floor(b))))
    r += diff[0]/max_diff
    g += diff[1] / max_diff
    b += diff[2] / max_diff
    time.sleep(interval)
  fill(strip, Color(color2[0], color2[1], color2[2]))

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

def sunset(strip):
  fade(strip, (255,69,0), (0,0,0),0.01)
  flash(strip,Color(255,69,0), 3,0.5)
  fill(strip, Color(255,255,255))
  t = Timer(get_sunset_delay() / 10000, sunset, args=strip)
  t.start()

@client.event
async def on_message(message):
  if message.author == client.user or not message.content.startswith(prefix):
    return
  if prefix in message.content and len(message.content.split(" ")) < 2:
    command = message.content
  elif prefix in message.content:
    command = message.content.split(" ")[0]
    param = message.content.split(" ")[1:]
  command = command[1:]
  if command == "superping":
    flash(strip, Color(255, 0, 0), 3, 0.5)
  elif command == "off":
    clear(strip)
  elif command == "light":
    fill(strip, Color(255,255,255))
  elif command == "fill":
    fill(strip, Color(int(param[0]),int(param[1]),int(param[2])))
  elif command == "flash":
    flash(strip, Color(int(param[0]), int(param[1]), int(param[2])), int(param[3]), float(param[4]))
  elif command == "train":
    train(strip, int(param[3]), Color(int(param[0]), int(param[1]), int(param[2])))
  elif command == "fade":
    fade(strip, (int(param[0]),int(param[1]),int(param[2])), (int(param[3]),int(param[4]),int(param[5])), 0.05)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  t = Timer(get_sunset_delay(), sunset, args=[strip])
  t.start()
  client.run(TOKEN)

  # flash(strip, Color(255, 00, 0), 3, 0.5)
  # timer(strip, Color(255, 255, 0), 30)

  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,255,0))
  #   strip.show()
  #   time.sleep(0.1)
  #
  # for i in range(strip.numPixels()):
  #   strip.setPixelColor(i,Color(0,0,0))
  #   strip.show()
  #   time.sleep(0.1)



