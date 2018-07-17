import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

import cards, extension, potg, saltybet
plugins = [cards, extension, potg, saltybet]

from config import token

client = discord.Client()

@client.event
async def on_ready():
    print('Link for inviting bot to servers:\nhttps://discordapp.com/api/oauth2/authorize?client_id='+ client.user.id + '&permissions=0&scope=bot')
    print('Logged in as')
    print(client.user.name)
    print('Client ID: ' + client.user.id)
    print('------')

@client.event
async def on_message(message):
    # We don't want to respond to ourselves or other bots
    if message.author == client.user or message.author.bot == True:
        return

    for plugin in plugins:
        if plugin.trigger(message, client) == True:
            await plugin.action(message, client)
            return


client.run(token)
