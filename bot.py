# bot.py
import os

import discord
from dotenv import load_dotenv
from random import randint
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content[0] == "!":
    # This is a bot-command, so we handle it
    cmd = message.content.split(" ")[0][1:]             # Command type, e.g. "roll", "spell", etc
    cmd_cnt = " ".join(message.content.split(" ")[1:])  # Command content e.g. 5d30, acid rain 
    if cmd in ("roll", "r"):
      rolls = cmd_cnt.split(" ")
      total_roll = 0
      for roll in rolls:
        total_roll += roll_to_num(roll)
      await message.channel.send(str(total_roll))
    elif cmd in ("spell", "s"):
      spell_query = cmd_cnt
      spell = get_spell(spell_query)
      msg = spell_to_msg(spell)
      await message.channel.send(msg)

def spell_to_msg(spell):
  msg = "```\n%s" % (spell["name"])
  for desc in spell["desc"]:
    msg += "\n%s" % desc
  if "higher_level" in spell:
    msg += "\n"
    for hl in spell["higher_level"]:
      msg += "\n%s" % hl
  msg += "```"
  return msg

def roll_to_num(roll):
  if "+" in roll:
    dice_roll = roll.split("+")[0]
    add = int(roll.split("+")[1])
    return dice_to_num(dice_roll) + add
  else:
    return dice_to_num(roll)

def dice_to_num(dice):
  """5d30 ==> 5 rolls of a d30."""
  if dice[0] == "d":
    return randint(1, int(dice[1:]))
  else:
    d_pos = dice.find("d")
    num_rolls = int(dice[0:d_pos])
    dice_size = int(dice[d_pos+1:])
    total_roll = 0
    for _ in range(num_rolls):
      total_roll += randint(1, dice_size)
    return total_roll

def get_spell(spell_name_attempt):
  from spellget import get_spell_from_string
  response = get_spell_from_string(spell_name_attempt)
  return response

client.run(TOKEN)