#Import Discord Python Library
import discord
from discord.ext import commands, tasks

#Import API Request Librarys
import aiohttp

#Import Built In Python Library
from datetime import datetime
from datetime import date

client = discord.Client()

@client.event
async def on_ready():
  now = datetime.now()
  today = date.today()
  current_time = now.strftime("%H:%M:%S")
  print("We have logged in as {0.user}".format(client))
  print(f"Date of Logon: {today}")
  print(f"Time of Logon: {current_time}\n")