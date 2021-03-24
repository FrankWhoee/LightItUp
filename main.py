import asyncio
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
from threading import Thread
from flask import Flask

class async_discord_thread(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.loop = asyncio.get_event_loop()
    self.start()

  async def starter(self):
    await client.start(TOKEN)

  def run(self):
    self.name = 'Discord.py'
    self.loop.create_task(self.starter())
    self.loop.run_forever()


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
    time.sleep(interval/max_diff)
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
  fade(strip, (255,69,0), (0,0,0),1)
  flash(strip,Color(255,69,0), 3,0.5)
  fill(strip, Color(255,255,255))
  t = Timer(get_sunset_delay() / 10000, sunset, args=[strip])
  t.start()

@client.event
async def on_message(message):
  try:
    if message.author == client.user or not message.content.startswith(prefix):
      return
    if prefix in message.content and len(message.content.split(" ")) < 2:
      command = message.content
      param = []
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
      if len(param) < 3:
        await message.channel.send("Not enough parameters! Command requires three RGB values. Ex. `fill 255 0 123`")
      elif len(param) > 3:
        await message.channel.send("Too many parameters! Command requires three RGB values. Ex. `fill 255 0 123`")
      else:
        fill(strip, Color(int(param[0]),int(param[1]),int(param[2])))
    elif command == "flash":
      if len(param) < 5:
        await message.channel.send("Not enough parameters! Command requires three RGB values, a count, and interval between flashes. Ex. `flash 255 0 0 3 0.5`")
      elif len(param) > 5:
        await message.channel.send("Too many parameters! Command requires three RGB values, a count, and interval between flashes. Ex. `flash 255 0 0 3 0.5`")
      else:
        flash(strip, Color(int(param[0]), int(param[1]), int(param[2])), int(param[3]), float(param[4]))
    elif command == "train":
      if len(param) < 4:
        await message.channel.send("Not enough parameters! Command requires three RGB values, and a length. Ex. `train 255 0 0 5`")
      elif len(param) > 4:
        await message.channel.send("Too many parameters! Command requires three RGB values, and a length. Ex. `train 255 0 0 5`")
      else:
        train(strip, int(param[3]), Color(int(param[0]), int(param[1]), int(param[2])))
    elif command == "fade":
      if len(param) < 6:
        await message.channel.send("Not enough parameters! Command requires two sets of three RGB values. Ex. `fade 255 69 0 0 0 0`")
      elif len(param) > 6:
        await message.channel.send("Too many parameters! Command requires two sets of three RGB values. Ex. `fade 255 69 0 0 0 0`")
      else:
        fade(strip, (int(param[0]),int(param[1]),int(param[2])), (int(param[3]),int(param[4]),int(param[5])), 1)
    elif command == "timer":
      if len(param) == 1:
        timer(strip, Color(255,0,0), int(param[0]))
      elif len(param) == 4:
        timer(strip, Color(int(param[0]), int(param[1]), int(param[2])), int(param[3]))
      elif (len(param) > 1 and len(param) < 4) or len(param) > 4:
        await message.channel.send("Parameter mismatch. Command requires either three RGB values and a duration or just a duration in seconds. Ex. `timer 255 0 0 5` or `timer 5`")
  except Exception as e:
    print(e)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    flash(strip, Color(0, 255, 0), 3, 0.5)
    clear(strip)

if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  sunset_timer = Timer(get_sunset_delay(), sunset, args=[strip])
  # sunset_timer.start()
  fade(strip, (255,255,255),(0,0,0), 1)
  discord_thread = async_discord_thread()
  app.run(host="0.0.0.0")


