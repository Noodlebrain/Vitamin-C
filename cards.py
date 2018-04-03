from discord import Embed
from discord import Color
import wikia
import re

from card_data import joke_cards

# regex searches for anything in between square brackets []
card_regex = re.compile('\[(.+?)\]')

# Checks if anything in between square brackets
def trigger(content):
    query = re.search(card_regex, content.lower().strip())
    if query and query.groups()[0].strip():
        return True
    return False

async def action(message, client):
    # Get all words in between square brackets
    results_list = re.findall(card_regex, message.content.lower().strip())

    for result in results_list:
        if result in joke_cards.keys():
            embed_message = Embed(  title = joke_cards[result]['title'],
                                type = 'rich',
                                url = joke_cards[result]['source'])
            embed_message.set_image(url = joke_cards[result]['image'])
            embed_message.color = set_color(joke_cards[result]['type'])
            await client.send_message(message.channel, embed = embed_message)


# Sets the color of the Discord embed based on the card type
def set_color(type):
    if type == 'Boost':
        return Color.green()

    else:
        return Color.default()
