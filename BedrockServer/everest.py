#!/usr/bin/python3

import discord
import server
import server_log
import os

everest = 'Njc4NzY4Mjk2MDQ4NDU5Nzc2.XknmuQ.3oVAu4eMXb9YiHFLCZ-yaNEw83Q'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$worlds'):
        worlds = "\n".join([c.name for c in server.containers()])
        await message.channel.send('Running worlds:\n'+worlds)

    if message.content.startswith('$online'):

        msg = ""
        for world in server.containers():
            log = os.path.normpath(os.path.join('./worlds',world.name,'server.log'))
            server_log.parse(log)
            msg += "World "+world.name+": "
            online = server_log.online()

            if not online:
               msg += "No users online"

            msg += "\n"

            for p in online:
               msg += p['name']+" is online\n"
        await message.channel.send(msg)

def start():
   client.run(everest)

if __name__== "__main__":
   start()
