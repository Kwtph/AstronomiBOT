import requests
import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
from keep_alive import keep_alive
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
data = response.json()
date = data["date"]
explanation = data["explanation"]
title = data["title"]

client = discord.Client()
status = cycle(['HV 2112', 'Yıldız içinde yıldız'])


@client.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")
    client = commands.Bot(command_prefix="!")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


async def sendNewDayPhoto():
    await client.get_channel(1004471681898774568).send("```diff\n  (" + date + ")" + " " + title + "\n```")
    if "hdurl" in data:
        await client.get_channel(1004471681898774568).send(data["hdurl"])
    else:
        await client.get_channel(1004471681898774568).send(data["url"])
    await client.get_channel(1004471681898774568).send("```\n" + explanation + "```")


sched = AsyncIOScheduler()
sched.start()
sched.add_job(sendNewDayPhoto, CronTrigger(hour=17, minute=30,
                                           second=0))  #on 20:00

keep_alive()
client.run(os.getenv('TOKEN'))
