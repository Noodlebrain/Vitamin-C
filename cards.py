from discord import Embed
from discord import Color
import wikia
import re

from card_data import cards

# regex searches for anything in between square brackets []
card_regex = re.compile('\[(.+?)\]')

# regex searches for anything with .hyper in it
hyper_regex = re.compile('(.+?)\.hyper$')

# class that contains a boolean whether an operation was successful or not,
# and a list of returned objects
class ReturnResult:
    results = []
    success = True
    def __init__(self, results, success):
        self.results = results;
        self.success = success;

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
        c = result
        # checks if the string between the [] has .hyper at the end
        if isHyper(result):
            char_match = re.search(hyper_regex, result.strip())
            if char_match:
                character = char_match.groups()[0].strip()
                hyper_ret = findHyper(character)
                if hyper_ret.success == False:
                    msg = 'Could not find what you searched for, try again.'
                    await client.send_message(message.channel, msg)

                elif len(hyper_ret.results) > 1:
                    msg = 'Multiple results found: {0}'.format(", ".join(x for x in hyper_ret.results))
                    await client.send_message(message.channel, msg)

                else:
                    c = hyper_ret.results[0].lower()
            else:
                msg = 'It seems like you didn\'t put anything before \".hyper\", try again'
                await client.send_message(message.channel, msg)

        if c in cards.keys():
            embed_msg = createEmbed(c)
            await client.send_message(message.channel, embed = embed_msg)

        else:   # no exact match, so search Wikia instead
            card_ret = wikiaSearch(c, False)
            if card_ret.success == False:
                msg = 'Could not find what you searched for, try again.'
                await client.send_message(message.channel, msg)

            elif len(card_ret.results) > 1:
                msg = 'Multiple results found: {0}'.format(", ".join(x for x in card_ret.results))
                await client.send_message(message.channel, msg)

            else:
                c = card_ret.results[0]
                embed_msg = createEmbed(c)
                await client.send_message(message.channel, embed = embed_msg)

# creates an embed using the provided card name
def createEmbed(card):
    embed_message = Embed(  title = cards[card]['title'],
                            type = 'rich',
                            url = cards[card]['source'])

    if cards[card]['type'] == 'Character':
        embed_message.description = 'Availability: ' + cards[card]['availability']
        if 'flavor' in cards[card].keys():
            embed_message.set_footer(text = cards[card]['flavor'])

    embed_message.set_image(url = cards[card]['image'])
    embed_message.color = set_color(cards[card]['type'])
    return embed_message

# Checks if the string has .hyper in it.
def isHyper(string):
    character = re.search(hyper_regex, string.strip())
    if character:
        return True
    return False

# Finds the name of a character's hyper card.
def findHyper(char):
    ret = ReturnResult([], True)
    if char in cards.keys():
        if cards[char]['type'] == 'Character':
            ret.results.append(cards[char]['hyper'])
            return ret
    # search 100% OJ Wikia for titles if there is no exact match
    return wikiaSearch(char, True)

# Searches the 100% OJ Wikia for titles on its page - charsOnly is boolean to search for characters only, or all cards
def wikiaSearch(string, charsOnly):
    ret = ReturnResult([], True)
    try:
        search_results = wikia.search('onehundredpercentorangejuice', char, 2)
        for result in search_results:
            title = result.lower().strip()
            if title in cards.keys():
                if charsOnly:
                    if cards[title]['type'] == 'Character':
                        ret.results.append(title)
                else:
                    ret.results.append(title)
    except:
        ret.success = False
        return ret
    if len(ret.results) < 1:
        ret.success = False
    return ret


# Sets the color of the Discord embed based on the card type
def set_color(type):
    if type == 'Boost':
        return Color(0x95FF9C)
    elif type == 'Battle':
        return Color(0xFFDC83)
    elif type == 'Event':
        return Color(0x93C0FF)
    elif type == 'Trap':
        return Color(0xE28FFF)
    elif type == 'Gift':
        return Color(0xFC8BC6)
    elif type == 'Hyper':
        return Color.orange()
    elif type == 'Character':
        return Color.lighter_grey()
    elif type == 'Enemy':
        return Color.red()
    else:
        return Color.default()
