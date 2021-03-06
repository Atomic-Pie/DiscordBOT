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


async def deleteTrigger(message):
    saved = False
    savedTriggers = getTriggers()
    await message.channel.send("Enter Trigger")
    trigger = (await client.wait_for(
        'message',
        check=lambda m: m.author == message.author,
        timeout=60)).content
    for savedTrigger in savedTriggers:
        if savedTrigger[0].upper() == trigger.upper():
            saved = True
    if not saved:
        await message.channel.send("Never heard of it")
        return
    await message.channel.send("Are you Sure?")
    sure = (await client.wait_for(
        'message',
        check=lambda m: m.author == message.author,
        timeout=60)).content
    if sure.upper() == "NO":
        await message.channel.send(
            "Stop wasting my time")
        return
    elif sure.upper() == "YES":
        c.execute("Delete from triggers Where trigger='{}'".format(trigger))
        conn.commit()
        await message.channel.send("The damage has been done")
        await message.channel.send("oi <@381520865390624773> they are fucking with me")
        return
    else:
        await message.channel.send(
            "do you have brain damage?")
        return



def checkuser(user1, user2):
    return user1 == user2


def searchIn(word, sentence):
    word = word.upper()
    sentence = sentence.upper()
    sentencelen = len(sentence)
    wordlen = len(word)
    x = sentence.find(word)
    if sentence[x - 1] not in VOIDCHARACTERS:
        if (x + wordlen + 1) < sentencelen and [x + wordlen + 1
                                                ] in VOIDCHARACTERS:
            return True
    return False


def getTriggers():
    c.execute("SELECT * FROM triggers")
    return c.fetchall()


async def addTrigger(message):
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
        await message.channel.send("K")
        return


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    triggers = getTriggers()

    # Don't react to yourself you idiot
    if message.author == client.user:
        return

    try:
        if msg.upper() == "!DELETE TRIGGER" or msg.upper() == "!DEL TRIGGER":
            await deleteTrigger(message)

    except asyncio.TimeoutError:
        await message.channel.send("too slow bitch")
        return

    # Add Trigger
    try:
        if msg.upper() == "!ADD TRIGGER":
            await addTrigger(message)

    except asyncio.TimeoutError:
        await message.channel.send("too slow bitch")
        return

    # Trigger Triggers
    for trigger in triggers:
        if trigger[0].upper() in msg.upper():
            if trigger[2] == "is" and not searchIn(trigger[0], msg):
                await message.channel.send(trigger[1])
            elif trigger[2] == "in":
                await message.channel.send(trigger[1])


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
