import asyncio
import json
import math
import os
import time
from datetime import date, datetime
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
import relay

instances_of_victor = 0

timers = {"late_evening": (23,00,5,5,5), "midnight":(23,30,0,0,0)}

previous_state = []
current_status = discord.Status.online
saved_status = discord.Status.online

def save_state():
    global previous_state
    global saved_status
    previous_state = []
    saved_status = current_status
    for i in range(strip.numPixels()):
        previous_state.append(strip.getPixelColorRGB(i))

def restore_state():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,previous_state[i])
    strip.show()

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
    return render_template("index.html")

@app.route('/ambience')
def ambience():
    ambtype = request.args["v"]
    if ambtype == "light":
        fill()
    elif ambtype == "off":
        if mt != None:
            mt.terminate()
            mt_terminate = True
        clear()
    return "",200

def wait_for_finish(child_process, mt):
    global mt_terminate
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
    return child_process

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

prefix = "!"

IN1 = 14
IN2 = 15
mt = None
mt_terminate = False
ADMIN = [194857448673247235, 385297155503685632]


def flash(count, interval):
    global mt
    global mt_terminate
    child_process = False
    child_process = wait_for_finish(child_process,mt)

    def helper():
        for d in range(count):
            fill()
            time.sleep(interval)
            clear()
            time.sleep(interval)

    if child_process:
        helper()
    else:
        mt = Process(target=helper, name="flash")
        mt.start()


def clear():
    relay.off(14)


def fill():
    relay.on(14)


def sunset():
    t = Timer(get_sunset_delay(), sunset)
    t.start()
    fill()

def get_time_delta(hour,minute,second):
    today = datetime.today()
    target = datetime(today.year, today.month, today.day, hour,minute,second)
    if today > target:
        target = datetime(today.year, today.month, today.day + 1, hour, minute, second)
    return abs(target - today).seconds

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
        flash(3,0.1)
    elif command == "off":
        if mt != None:
            mt.terminate()
            mt_terminate = True
        clear()
    elif command == "status":
        guild = await client.fetch_guild(420468091559084033)
        print(guild.name)
        member = await guild.fetch_member(194857448673247235)
        print(member.name)
        print(member.raw_status)
        print(member.activity.name)
    elif command == "light":
        fill()


@client.event
async def on_member_update(before, after):
    global strip
    global current_status
    global saved_status
    if before.id == 194857448673247235 and after.id == 194857448673247235:
        current_status = after.status
        if saved_status == "online" and (str(after.status) == "offline" or str(after.status) == "idle"):
            print("Turning off amogus to save energy: Discord status is idle or offline.")
            clear()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    flash(3, 0.1)



if __name__ == '__main__':
    try:
        sunset_timer = Timer(get_sunset_delay(), sunset)
        sunset_timer.start()
    except:
        flash(3,0.1)

    try:
        discord_thread = async_discord_thread()

        app.run(host="0.0.0.0")
    except KeyboardInterrupt:
        relay.cleanup()
    finally:
        relay.cleanup(force=True)