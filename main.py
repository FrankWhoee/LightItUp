import asyncio
import json
import math
import os
import time
from datetime import date, datetime

from rpi_ws281x import *
import random
import discord
import numpy as np
from sunx import get_sunset_delay
import argparse
from threading import Timer
from threading import Thread
from flask import Flask, render_template, Response, send_from_directory, session, request
from multiprocessing import Process
from discord.ext import tasks

instances_of_victor = 0

timers = {"late_evening": (23,30,5,5,5), "midnight":(23,59,0,0,0)}

class processNode():
    def __init__(self, process, complete: bool, prev, next, name):
        self.process = process
        self.complete = complete
        self.prev = prev
        self.next = next
        self.name = name

    def helper(self):
        global mt

        while self.prev is not None:
            if self.prev.complete:
                break
            time.sleep(0.1)
        self.process()
        self.complete = True
        if self.next is not None:
            mt = Process(target=self.next.helper, name=self.next.name)
            mt.start()


class async_discord_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.start()

    async def starter(self):
        await client.start(TOKEN)

    def run(self):
        global instances_of_victor
        if instances_of_victor > 0:
            return
        self.name = 'Discord.py'
        self.loop.create_task(self.starter())
        self.loop.run_forever()
        instances_of_victor += 1

pnode = processNode(0, True, None, None, "init")

app = Flask(__name__)
app.secret_key = 'Zli6WMDUEboJnp34fzwK'.encode('utf8')


@app.route('/assets/<path>')
def send_assets(path):
    return send_from_directory('assets', path)


@app.route('/assets/icons/<path>')
def send_icons(path):
    return send_from_directory('assets/icons', path)


@app.route('/css/<path>')
def send_style(path):
    return send_from_directory('css', path)


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/')
def index():
    if "momMode" in session and session["momMode"] == True:
        return render_template("mom.html")
    else:
        session["momMode"] = False
        return render_template("index.html")


@app.route('/switchmode')
def switch_mode():
    if "momMode" in session and session["momMode"] == True:
        session["momMode"] = False
        return render_template("index.html"), 200
    else:
        session["momMode"] = True
        return render_template("mom.html"), 200


@app.route('/momalert')
def momalert():
    flash(strip, Color(255, 0, 0), 3, 0.5)
    return "", 200


@app.route('/ambience')
def ambience():
    global mt
    global mt_terminate
    ambtype = request.args["v"]
    if ambtype == "light":
        fill(strip, Color(125, 125, 125))
    elif ambtype == "off":
        if mt != None:
            mt.terminate()
            mt_terminate = True
        clear(strip)
    elif ambtype == "dim":
        fill(strip, Color(5, 5, 5))
    elif ambtype == "superdim":
        clear(strip)
        for i in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i, Color(1, 1, 1))
        strip.show()
    elif ambtype == "reddim":
        clear(strip)
        for i in range(0, strip.numPixels(), 2):
            strip.setPixelColor(i, Color(1, 0, 0))
        strip.show()
    elif ambtype == "party":
        clear(strip)
        rainbow()
    return "", 200

def rainbow():
    rainbow_array = []
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(255, int(i * 255 / (strip.numPixels() / 6)), 0))
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(255 - int(i * 255 / (strip.numPixels() / 6)), 255 , 0))
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(0,255, int(i * 255 / (strip.numPixels() / 6))))
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(0, 255 - int(i * 255 / (strip.numPixels() / 6)), 255))
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(int(i * 255 / (strip.numPixels() / 6)), 0, 255))
    for i in range(0, int(strip.numPixels() / 6)):
        rainbow_array.append(Color(255,0,255-int(i * 255 / (strip.numPixels() / 6))))
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        while True:
            for i in range(len(rainbow_array)):
                mod_array = rainbow_array[i:len(rainbow_array)]
                mod_array.extend(rainbow_array[0:i])
                show_array(strip, mod_array)

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="rainbow")
        mt.start()

def show_array(strip,array):
    for i in range(len(array)):
        # print(i)
        # print(array[i])
        strip.setPixelColor(i,array[i])
    strip.show()

@app.route('/signal')
def signal():
    sigtype = request.args["v"]
    print(sigtype)
    if sigtype == "emergency":
        fill(strip,Color(255,0,0))
    elif sigtype == "kitchen":
        flash(strip,Color(255,125,0),3,0.5)
    elif sigtype == "dad":
        flash(strip,Color(0,170,212),3,0.5)
    elif sigtype == "theater":
        flash(strip,Color(68,0,170),3,0.5)
    return "", 200

# Extract secrets from local file.
if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        secrets = json.load(f)
else:
    print("WARNING: No secrets.json found. Assuming no Discord Token.")
    secrets = {}
    secrets["token"] = os.environ.get("token")

# Instantiate discord.py Client
TOKEN = secrets["token"]
intents = discord.Intents.all()

client = discord.Client(intents=intents)

previous_discord_status = None

prefix = "`"

LED_COUNT = 150
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
CORNER_LED = 45
mt = None
mt_terminate = False
ADMIN = [194857448673247235, 385297155503685632]



def train(strip, length, color, wait_time_ms=50, trailing=Color(0, 0, 0)):
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        for i in range(length):
            strip.setPixelColor(i, color)
            strip.show()
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, trailing)
            strip.setPixelColor(i + length, color)
            strip.show()
            time.sleep(wait_time_ms / 1000)

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="train")
        mt.start()


def flash(strip, color, count, interval):
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        for d in range(count):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(interval)
            clear(strip)
            strip.show()
            time.sleep(interval)

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="flash")
        mt.start()


def clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def fill(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show();

# def fade(strip,color,interval):
#     global mt
#     global mt_terminate
#     child_process = False
#     while True:
#         if mt_terminate:
#             mt_terminate = False
#             break
#         if mt is None:
#             break
#         try:
#             mt.join(timeout=0)
#         except:
#             child_process = True
#             break
#         if not mt.is_alive():
#             break
#         time.sleep(0.5)
#
#     def helper():
#        for i in range(int(interval/0.05)):
#            for k in range(strip.numPixels()):
#
#            time.sleep(0.05)
#
#     if child_process:
#         helper()
#     else:
#         mt = Process(target=helper, name="fade")
#         mt.start()

def fade_from_to(strip, color1, color2, interval):
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        max_diff = max(tuple(np.absolute(np.subtract(color2, color1))))
        diff = tuple(np.subtract(color2, color1))
        r = color1[0]
        g = color1[1]
        b = color1[2]
        for i in range(max_diff):
            fill(strip, Color(int(math.floor(r)), int(math.floor(g)), int(math.floor(b))))
            r += diff[0] / max_diff
            g += diff[1] / max_diff
            b += diff[2] / max_diff
            time.sleep(interval / max_diff)
        fill(strip, Color(color2[0], color2[1], color2[2]))

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="fade")
        mt.start()


def timer(strip, color, total_time):
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        fill(strip, color)
        pixels = strip.numPixels()
        if total_time > pixels:
            time.sleep(math.ceil(float(total_time) / pixels))
            for i in range(0, pixels - math.ceil(pixels / float(total_time)), math.ceil(pixels / float(total_time))):
                for k in range(i, i + math.ceil(pixels / float(total_time))):
                    strip.setPixelColor(k, Color(0, 0, 0))
                strip.show()
                time.sleep(math.ceil(float(total_time) / pixels))
        else:
            for i in range(0, pixels):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                time.sleep(float(total_time) / pixels)

        flash(strip, Color(255, 0, 0), 3, 0.5)

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="timer")
        mt.start()


def sunset(strip):
    global mt
    global mt_terminate
    child_process = False
    while True:
        if mt_terminate:
            mt_terminate = False
            break
        if mt is None:
            break
        try:
            mt.join(timeout=0)
        except:
            child_process = True
            break
        if not mt.is_alive():
            break
        time.sleep(0.5)

    def helper():
        fade_from_to(strip, (255, 69, 0), (0, 0, 0), 1)
        for i in range(CORNER_LED, strip.numPixels()):
            strip.setPixelColor(i, Color(255, 69, 0))
        strip.show()
        for k in range(3):
            for i in range(CORNER_LED, -1, -1):
                strip.setPixelColor(i, Color(int(255 * (float(i) / CORNER_LED)), int(69 * (float(i) / CORNER_LED)),
                                             int(255 * ((CORNER_LED - float(i)) / CORNER_LED))))
                strip.show()
                time.sleep(0.02)
            for i in range(CORNER_LED, -1, -1):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                time.sleep(0.02)

        flash(strip, Color(255, 69, 0), 3, 0.5)
        fill(strip, Color(125, 125, 125))

    t = Timer(get_sunset_delay(), sunset, args=[strip])
    t.start()
    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="sunset")
        mt.start()

def get_time_delta(hour,minute,second):
    today = datetime.today()
    target = datetime(today.year, today.month, today.day, hour,minute,second)
    if today > target:
        target = datetime(today.year, today.month, today.day + 1, hour, minute, second)
    return abs(target - today).seconds

def daily_timer(strip, data):
    print("Triggered timer: " + str(data))
    fill(strip, Color(data[2], data[3], data[4]))
    Timer(get_time_delta(data[0],data[1],0),daily_timer, args=[strip,data]).start()

def brightness_protection(strip):
    for i in range(0,strip.numPixels()):
        c = strip.getPixelColorRGB(i)
        r = c.r
        g = c.g
        b = c.b
        if (r+g+b) > 375:
            adjustment = 375/(r+g+b)
            r *= adjustment
            b *= adjustment
            g *= adjustment
            r = int(math.floor(r))
            g = int(math.floor(g))
            b = int(math.floor(b))
        strip.setPixelColor(i,Color(r,g,b))
    strip.show()
    t = Timer(300, brightness_protection, args=[strip])
    t.start()

@client.event
async def on_message(message):
    global mt
    global mt_terminate
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
        flash(strip, Color(200, 50, 218), 3, 0.5)
    elif command == "off":
        if mt != None:
            if mt.name == "timer" and message.author.id not in ADMIN:
                await message.channel.send("Non-admin users can not override timer commands.")
                return
            mt.terminate()
            mt_terminate = True
        clear(strip)
    elif command == "status":
        guild = await client.fetch_guild(420468091559084033)
        print(guild.name)
        member = await guild.fetch_member(194857448673247235)
        print(member.name)
        print(member.raw_status)
        print(member.activity.name)
    elif command == "light":
        fill(strip, Color(125, 125, 125))
    elif command == "dim":
        fill(strip, Color(5, 5, 5))
    elif command == "superdim":
        clear(strip)
        for i in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i, Color(1, 1, 1))
        strip.show()
    elif command == "reddim":
        clear(strip)
        for i in range(0, strip.numPixels(), 2):
            strip.setPixelColor(i, Color(1, 0, 0))
        strip.show()
    elif command == "fill":
        if len(param) < 3:
            await message.channel.send("Not enough parameters! Command requires three RGB values. Ex. `fill 255 0 123`")
        elif len(param) > 3:
            await message.channel.send("Too many parameters! Command requires three RGB values. Ex. `fill 255 0 123`")
        else:
            fill(strip, Color(int(param[0]), int(param[1]), int(param[2])))
    elif command == "flash":
        if len(param) < 5:
            await message.channel.send(
                "Not enough parameters! Command requires three RGB values, a count, and interval between flashes. Ex. `flash 255 0 0 3 0.5`")
        elif len(param) > 5:
            await message.channel.send(
                "Too many parameters! Command requires three RGB values, a count, and interval between flashes. Ex. `flash 255 0 0 3 0.5`")
        else:
            flash(strip, Color(int(param[0]), int(param[1]), int(param[2])), int(param[3]), float(param[4]))
    elif command == "train":
        if len(param) < 4:
            await message.channel.send(
                "Not enough parameters! Command requires three RGB values, and a length. Ex. `train 255 0 0 5`")
        elif len(param) > 4:
            await message.channel.send(
                "Too many parameters! Command requires three RGB values, and a length. Ex. `train 255 0 0 5`")
        else:
            train(strip, int(param[3]), Color(int(param[0]), int(param[1]), int(param[2])))
    elif command == "fade":
        if len(param) < 6:
            await message.channel.send(
                "Not enough parameters! Command requires two sets of three RGB values. Ex. `fade 255 69 0 0 0 0`")
        elif len(param) > 6:
            await message.channel.send(
                "Too many parameters! Command requires two sets of three RGB values. Ex. `fade 255 69 0 0 0 0`")
        else:
            fade_from_to(strip, (int(param[0]), int(param[1]), int(param[2])), (int(param[3]), int(param[4]), int(param[5])), 1)
    elif command == "timer":
        if len(param) == 1:
            timer(strip, Color(255, 0, 0), int(param[0]))
        elif len(param) == 4:
            timer(strip, Color(int(param[0]), int(param[1]), int(param[2])), int(param[3]))
        elif (len(param) > 1 and len(param) < 4) or len(param) > 4:
            await message.channel.send(
                "Parameter mismatch. Command requires either three RGB values and a duration or just a duration in seconds. Ex. `timer 255 0 0 5` or `timer 5`")
    elif command == "rainbow":
        rainbow()


@client.event
async def on_member_update(before, after):
    global strip
    if before.id == 194857448673247235 and after.id == 194857448673247235:
        if str(before.status) == "online" and (str(after.status) == "offline" or str(after.status) == "idle"):
            print("Turning off strip to save energy: Discord status is idle or offline.")
            clear(strip)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    fade_from_to(strip, (0, 0, 0),(255, 255, 255), 2)
    fade_from_to(strip, (255, 255, 255), (50, 50, 50),0.1)
    time.sleep(0.1)
    fade_from_to(strip, (50, 50, 50), (255, 255, 255), 0.1)
    time.sleep(0.1)
    fade_from_to(strip, (255, 255, 255), (0, 0, 0), 0.5)
    clear(strip)


if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    clear(strip)
    # rainbow()
    try:
        sunset_timer = Timer(get_sunset_delay(), sunset, args=[strip])
        sunset_timer.start()
    except:
        flash(strip,Color(125,0,0),3,0.1)

    brightness_protection_timer = Timer(300, brightness_protection, args=[strip])
    brightness_protection_timer.start()

    today = datetime.today()
    for t in timers.keys():
        print(get_time_delta(timers[t][0], timers[t][1], 0))
        Timer(get_time_delta(timers[t][0], timers[t][1], 0), daily_timer, args=[strip, timers[t]]).start()


    # flash(strip, Color(255, 69, 0), 2, 0.5)
    discord_thread = async_discord_thread()

    app.run(host="0.0.0.0")
