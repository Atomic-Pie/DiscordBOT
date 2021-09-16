import discord
import random
import asyncio
import os
from keep_alive import keep_alive
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
run = True
message1 = message2 = message3 = ""
VOIDCHARACTERS = [" ", ",", ".", "-", "?", "*", "_", "'", '"']
types = ["is", "in"]


def checkuser(user1, user2):
    return user1 == user2


def searchIn(word, sentance):
    word = word.upper()
    sentance = sentance.upper()
    sentancelen = len(sentance)
    wordlen = len(word)
    x = sentance.find(word)
    if sentance[x - 1] not in VOIDCHARACTERS:
        if (x + wordlen + 1) < sentancelen and [x + wordlen + 1
                                                ] in VOIDCHARACTERS:
            return True
    return False


def getTriggers():
    c.execute("SELECT * FROM triggers")
    return c.fetchall()


def addTrigger():
    pass


test = c.fetchall()
if len(test) < 0:
    c.execute("""CREATE TABLE triggers (
                trigger text,
                answer text,
                type text,
                author text
                )""")

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    triggers = getTriggers()

    if message.author == client.user:
        return

    try:
        if msg.upper() == "!ADD TRIGGER":
            await message.channel.send("Enter Trigger")
            trigger = (await client.wait_for(
                'message',
                check=lambda m: m.author == message.author,
                timeout=60)).content
            await message.channel.send("Enter Result")
            result = (await client.wait_for(
                'message',
                check=lambda m: m.author == message.author,
                timeout=60)).content
            await message.channel.send("Enter Type(in/is)")
            type_ = (await client.wait_for(
                'message',
                check=lambda m: m.author == message.author,
                timeout=60)).content
            if type_.lower() not in types:
                await message.channel.send(
                    "jesus christ learn to follow basic instructions")
                return
            else:

                statement = "INSERT INTO triggers VALUES('" + trigger + "', '" + result + "', '" + type_ + "', '" + message.author.name + "')"
                c.execute(statement)
                conn.commit()
                return

    except asyncio.TimeoutError:
        await message.channel.send("too slow bitch")
        return

    for trigger in triggers:
        if trigger[0].upper() in msg.upper():
            if trigger[2] == "is" and not searchIn(trigger[0], msg):
                await message.channel.send(trigger[1])
            elif trigger[2] == "in":
                await message.channel.send(trigger[1])


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
