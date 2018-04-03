import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

import cards
plugins = [cards]

from config import token

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # We don't want to respond to ourselves or other bots
    if message.author == client.user or message.author.bot == True:
        return

    for plugin in plugins:
        if plugin.trigger(message.content) == True:
            await plugin.action(message, client)
            return


client.run(token)
