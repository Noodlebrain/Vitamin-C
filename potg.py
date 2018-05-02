import random
import time
from discord import Embed
from discord import Color

from cards import set_color
from extension import create_embed
from card_data import cards

# module for the C!playofthegods command.
# in the game, "Play of the Gods" is a card, that, when used, plays a random
# event card from the deck or someone's hand.
# this implementation just pulls a random event card that isn't PotG itself.

# gets valid event cards from the dictionary of all cards
def generate_potg_cards():
    potg_cards = []
    for card in cards.values():
        if 'Event' in card['type'] and 'Play of the Gods' not in card['title']:
            potg_cards.append(card)
    return potg_cards

potg_cards = generate_potg_cards()

# checks if typed message is "C!playofthegods" or abbreviation "C!potg"
def trigger(content):
    return content.startswith('C!playofthegods') or content.startswith('C!potg')

async def action(message, client):
    potg_embed = Embed(title = 'Playing...', type = 'rich', color = Color(0x93C0FF))
    potg_embed.set_image(url = cards['play of the gods']['image'])
    msg = await client.send_message(message.channel, embed = potg_embed)
    random_card = random.choice(potg_cards)
    time.sleep(1)
    msg_text = 'Your card is...'
    embed_msg = create_embed(random_card)
    await client.edit_message(msg, new_content = msg_text, embed = embed_msg)
    return
