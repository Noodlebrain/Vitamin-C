import random
import time
from discord import Embed
from discord import Color

from cards import set_color
from card_data import cards

# module for the C!extension command.
# in the game, "Extension" is a card, when used, plays a random battle card
# (excluding "Extension").

# gets valid battle cards from the dictionary of all cards
def generate_extension_cards():
    extension_cards = []
    for card in cards.values():
        if 'Battle' in card['type'] and 'Extension' not in card['title']:
            extension_cards.append(card)
    return extension_cards

ext_cards = generate_extension_cards()

# checks if typed message is "C!extension" or abbreviation "C!ext"
def trigger(content):
    stripped = content.strip().lower()
    return stripped.startswith('c!extension') or stripped.startswith('c!ext')

async def action(message, client):
    ext_embed = Embed(title = 'Playing...', type = 'rich', color = Color.orange())
    ext_embed.set_image(url = cards['extension']['image'])
    msg = await client.send_message(message.channel, embed = ext_embed)
    random_card = random.choice(ext_cards)
    time.sleep(1)
    msg_text = 'Your card is...'
    embed_msg = create_embed(random_card)
    await client.edit_message(msg, new_content = msg_text, embed = embed_msg)
    return

# generates an embed for the randomly selected card
def create_embed(card):
    embed_message = Embed(  title = card['title'],
                            type = 'rich',
                            url = card['source'])
    embed_message.set_image(url = card['image'])
    embed_message.color = set_color(card['type'])
    return embed_message
