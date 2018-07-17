from characters import chars
import random

def trigger(message, client):
    stripped = message.content.strip().lower()
    return stripped.startswith('c!saltybet')

async def action(message, client):
    rand_l_char = random.choice(chars)
    rand_r_char = random.choice(chars)
    l_char = Character(rand_l_char['name'], rand_l_char['hp'], rand_l_char['atk'], rand_l_char['defense'], rand_l_char['evd'])
    r_char = Character(rand_r_char['name'], rand_r_char['hp'], rand_r_char['atk'], rand_r_char['defense'], rand_r_char['evd'])
    msg = 'Battle between {} (HP: {}/{}, ATK: {}, DEF: {}, EVD: {}) and {} (HP: {}/{}, ATK: {}, DEF: {}, EVD: {})'.format(
            l_char.name, l_char.hp, l_char.max_hp, l_char.atk, l_char.defense, l_char.evd,
            r_char.name, r_char.hp, r_char.max_hp, r_char.atk, r_char.defense, r_char.evd)
    await client.send_message(message.channel, msg)
    battle_num = 1
    while l_char.hp > 0 and r_char.hp > 0:
        msg = 'Battle {}:'.format(battle_num)
        await client.send_message(message.channel, msg)
        # left side attacks, right side defends/evades
        attacker = l_char
        defender = r_char
        no_turns = 2
        n = 0
        while (n < no_turns):
            atk = attack(attacker, '')
            atk_msg = '{} rolled a {} and attacks for {}'.format(attacker.name, atk[0], atk[1])
            await client.send_message(message.channel, atk_msg)
            # right side chooses whether to evade or defend
            dmg = atk[1]
            if dmg == 1 or defender.hp == 1 or dmg <= defender.evd:
                response = evade(dmg, defender)
                evd_msg = '{} rolled a {} and evades for {}'.format(defender.name, response[0], response[1])
                await client.send_message(message.channel, evd_msg)
            else:
                response = defend(dmg, defender)
                def_msg = '{} rolled a {} and defends for {}'.format(defender.name, response[0], response[1])
                await client.send_message(message.channel, def_msg)
            if response[2] == 0:
                dmg_msg = defender.name + ' dodged ' + attacker.name + '\'s attack!\n'
            else:
                dmg_msg = defender.name + ' took ' + str(response[2]) + ' damage from ' + attacker.name + '\'s attack.'
            defender.take_dmg(response[2])
            dmg_msg += '\n{} has {} HP left.'.format(defender.name, defender.hp)
            await client.send_message(message.channel, dmg_msg)
            if defender.hp <= 0:    # if attacker KOs defender
                msg = attacker.name + ' wins!'
                await client.send_message(message.channel, msg)
                break
            else:
                # swap attacker and defender positions
                temp = attacker
                attacker = defender
                defender = temp
            n += 1
        battle_num += 1

class Character:
    def __init__(self, name, hp, atk, defense, evd):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.evd = evd
    def take_dmg(self, dmg):
        self.hp = max(self.hp - dmg, 0)
    def heal(self, dmg):
        self.hp = min(self.hp + dmg, self.max_hp)
    def set_hp(self, hp):
        self.hp = min(hp, self.max_hp)

def attack(char, modifier):
    roll = random.randint(1, 6)
    if modifier == 'aot':       # "Awakening of Talent" always rolls 5s
        roll = 5
    if modifier == 'accel':     # "Accel Hyper" - double dice for attack
        roll += random.randint(1, 6)
    damage = max(roll + char.atk, 1)
    return (roll, damage)

def defend(enemy_atk, char):
    roll = random.randint(1, 6)
    block = max(roll + char.defense, 1)
    damage = max(enemy_atk - block, 1)
    return (roll, block, damage)

def evade(enemy_atk, char):
    roll = random.randint(1, 6)
    evasion = max(roll + char.evd, 1)
    if evasion > enemy_atk:
        damage = 0
    else:
        damage = enemy_atk
    return (roll, evasion, damage)
