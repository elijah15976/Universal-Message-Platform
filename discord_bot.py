#Import Discord Python Library
import discord
from discord.ext import commands, tasks

#Import Built In Python Library
from datetime import datetime
from datetime import date

#Import Other Python Libraries
import configparser
import json
import os

import threading
import asyncio
from flask import Flask, request

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

keys = configparser.ConfigParser()
keys.read("keys.ini")

client = discord.Client()
app = Flask(__name__)

intents = discord.Intents.default()
intents.members = True

@client.event
async def on_ready():
  now = datetime.now()
  today = date.today()
  current_time = now.strftime("%H:%M:%S")
  print("We have logged in as {0.user}".format(client))
  print(f"Date of Logon: {today}")
  print(f"Time of Logon: {current_time}\n")

@client.event
async def on_message(ctx):
  if ctx.content == "TEST":
    print("User tested bot")
    await ctx.author.send("This bot is sucessfully connected")
  elif ctx.content == "SUBSCRIBE":
    user = ctx.author

    subscription_tracker = open(os.path.join(THIS_FOLDER, 'discord_subscription.json'), "r")
    tracker_json = json.loads(subscription_tracker.read())

    for item in tracker_json:
      if user.id == item:
        await user.send("You are already subscribed")
        return
      
    tracker_json.append(user.id)

    subscription_tracker_write = open(os.path.join(THIS_FOLDER, 'discord_subscription.json'), "w")
    subscription_tracker_write.write(json.dumps(tracker_json))
    subscription_tracker.close()
    subscription_tracker_write.close()

    print("Subscribing user: " + str(user.id))
    await user.send("You are now subscribed to receive text notifications")
  elif ctx.content == "UNSUBSCRIBE":
    user = ctx.author

    subscription_tracker = open(os.path.join(THIS_FOLDER, 'discord_subscription.json'), "r")
    tracker_json = json.loads(subscription_tracker.read())

    for item in tracker_json:
      if user.id == item:
        tracker_json.remove(user.id)

        subscription_tracker_write = open(os.path.join(THIS_FOLDER, 'discord_subscription.json'), "w")
        subscription_tracker_write.write(json.dumps(tracker_json))
        subscription_tracker.close()
        subscription_tracker_write.close()

        print("Unsubscribing user: " + str(user.id))
        await user.send("You are no longer subscribed to receive text notifications")
        return
      
    tracker_json.append(user.id)

    subscription_tracker.close()

    await user.send("You are already not subscribed")

@app.route("/send", methods=["POST"])
def send():
  message = request.json["message"]
  try:
    fails = asyncio.run_coroutine_threadsafe(send_message(message), client.loop).result()

    if fails > 0:
      return "error"
    else:
      return "Finished"
  except Exception as e:
    print("Error in coroutine: " + str(e))
    return "error"

async def send_message(message):
  subscription_tracker = open(os.path.join(THIS_FOLDER, 'discord_subscription.json'), "r")
  tracker_json = json.loads(subscription_tracker.read())

  fails = 0

  for item in tracker_json:
    user = await client.fetch_user(item)
    try:
      await user.send(message)
    except Exception as e:
      print("Failed to send message to " + str(item) + ": " + str(e))
      fails = fails + 1

  return fails

def run_flask():
  app.run(host='0.0.0.0', port=3001)

if __name__ == "__main__":
  threading.Thread(target=run_flask).start()
  client.run(keys["Discord"]["Token"])