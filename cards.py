import re
from discord import Embed
from discord import Color
import wikia

from card_data import cards

# regex searches for anything in between square brackets []
card_regex = re.compile('\[(.+?)\]')

# regex searches for anything with .hyper in it
hyper_regex = re.compile('(.+?)\.hyper$')

# Checks if anything in between square brackets
def trigger(content):
    query = re.search(card_regex, content.lower().strip())
    if query and query.groups()[0].strip():
        return True
    return False

# Action of this module - gets a card name from in between brackets, searches
# for the matching card, and sends an
# embed with information about the fetched card
async def action(message, client):
    # Get all words in between square brackets
    results_list = re.findall(card_regex, message.content.lower().strip())

    for result in results_list:
        c = result.strip()

        # check if the string between the [] has .hyper at the end
        if is_hyper(result):
            char_match = re.search(hyper_regex, result.strip())
            if char_match:
                character = char_match.groups()[0].strip()
                hyper_ret = find_hyper(character)
                err_msg = wikia_parse(hyper_ret, client)
                if err_msg:
                    await client.send_message(message.channel, err_msg)
                else:
                    c = hyper_ret[0].lower()
            else: # This case is likely not going to happen due to regex, but just in case
                msg = 'It seems like you didn\'t put anything before \".hyper\", try again'
                await client.send_message(message.channel, msg)
                continue

        if c not in cards.keys():   # no exact match, so search Wikia instead
            card_ret = wikia_search(c, False)
            err_msg = wikia_parse(card_ret, client)
            if err_msg:
                await client.send_message(message.channel, err_msg)
                return
            else:
                c = card_ret[0].lower()

        embed_msg = create_embed(c)
        await client.send_message(message.channel, embed = embed_msg)
        if cards[c]['linked']:
            embed_msg = create_embed(cards[c]['linked'])
            await client.send_message(message.channel, embed = embed_msg)

# creates an embed using the provided card name
def create_embed(card):
    embed_message = Embed(  title = cards[card]['title'],
                            type = 'rich',
                            url = cards[card]['source'])

    if 'availability' in cards[card].keys():
        embed_message.description = 'Availability: ' + cards[card]['availability']

    if 'flavor' in cards[card].keys():
        embed_message.set_footer(text = cards[card]['flavor'])
    embed_message.set_image(url = cards[card]['image'])
    embed_message.color = set_color(cards[card]['type'])
    return embed_message

# Checks if the string has .hyper in it.
def is_hyper(string):
    character = re.search(hyper_regex, string.strip())
    if character:
        return True
    return False

# Finds the name of a character's hyper card.
def find_hyper(char):
    ret = []
    if char in cards.keys():
        if cards[char]['type'] == 'Character':
            ret.append(cards[char]['hyper'])
            return ret
    # search 100% OJ Wikia for names of characters if there is no exact match
    wikia_results =  wikia_search(char, True)
    # uses the result list to look for hypers
    if len(wikia_results) > 0:
        for result in wikia_results:
            entry = result.lower().strip()
            if entry in cards.keys():
                if cards[entry]['type'] == 'Character':
                    ret.append(cards[entry]['hyper'])
    return ret

# Searches the 100% OJ Wikia for titles on its page - charsOnly is boolean to search for characters only, or for all cards
def wikia_search(string, charsOnly):
    result_list = []
    try:
        search_results = wikia.search('onehundredpercentorangejuice', string, 3)
        for result in search_results:
            if result.lower().strip() in cards.keys():
                if charsOnly == True:
                    if cards[result.lower().strip()]['type'] == 'Character':
                        result_list.append(result.strip())
                else:
                    result_list.append(result.strip())
    except ValueError: # strangely, the wikia.search() method throws a ValueError if it doesn't get any search results
        return result_list
    return result_list

# parses a wikia search result to see if it has 1 result only
# returns empty msg if only 1 result
# returns a corresponding message if 0 or 2+ results
def wikia_parse(wikia_results, client):
    msg = ''
    numResults = len(wikia_results)
    if numResults != 1:
        if numResults < 1:
            msg = 'Could not find what you searched for, try again.'
        if numResults > 1:
            msg = 'Multiple results found: \"{0}\"'.format("\", \"".join(x for x in wikia_results))
    return msg

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
    elif type.startswith('Hyper'):
        return Color.orange()
    elif type == 'Character':
        return Color.lighter_grey()
    elif type == 'Enemy':
        return Color.red()
    else:
        return Color.default()
