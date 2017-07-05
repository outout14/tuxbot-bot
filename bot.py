#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Maël / Outout"
__licence__ = "WTFPL Licence 2.0"

from discord.ext import commands
import discord
from cogs.utils import checks
import datetime, re
import json, asyncio
import copy
import logging
from logging.handlers import RotatingFileHandler
import traceback
import sys
from collections import Counter

description = """
Je suis TuxBot, le bot qui vit de l'OpenSource ! ;)
"""

l_extensions = [

    'cogs.basics',
    'cogs.admin',
    'cogs.funs',
    'cogs.utility',
    'cogs.search',
    'cogs.ci'
]

# DISCORD LOGGER #
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True, in_help=True, name="DONOTUSE")


# CREDENTIALS #
try:
    def load_credentials():
        with open('params.json') as f:
            return json.load(f)
except:
    print("Le fichier de paramètre est introuvable, veuillez le créer et le configurer.")

prefix = ['.']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None, help_attrs=help_attrs)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.event
async def on_ready():
    print('---------------------')
    print('Logged in as :')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('---------------------')
    await bot.change_presence(game=discord.Game(name="Manger des pommes ! .help !"), status=discord.Status("dnd"), afk=False)
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_resumed():
    print('resumed...')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if re.search(r'^(cc |bonjour |salut |hello |bjr |slt |s\'lut)?([^ ]+ ){0,3}(qui s\'y conna(î|i)(t|s)|des gens|quelqu\'un|qqun|des personnes|du monde s\'y connait)[^\?]+\?$',message.content):
        await bot.send_message(message.channel, ":question: N'hésite pas à poser ta question directement {}, il n'est pas utile de demander si quelqu'un connait quelque chose avant ! :wink:".format(message.author.mention))

    if re.match(r'^<@(\w+)>$', message.content):
        await bot.send_message(message.channel, message.author.mention + " > Tu voulais lui dire quoi ? Tu le mentionne sans message !")

    if re.match(r"[A-Z]{5,}", message.content) and not message.author.bot and len(message.content) > 5:
        await bot.send_message(message.channel, message.author.mention + " > Evite les messages en majuscule, ce n'est pas la peine de crier !")

    await bot.process_commands(message)

@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)


## GITHUB CMD ##
@bot.command()
async def github():
    """Pour voir mon code"""
    text = "How tu veux voir mon repos Github pour me disséquer ? Pas de soucis ! Je suis un Bot, je ne ressens pas la douleur !\n https://github.com/outout14/tuxbot-bot"
    em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
    em.set_author(name='Outout', icon_url="https://avatars0.githubusercontent.com/u/14958554?v=3&s=400")
    await bot.say(embed=em)

## LOAD ##
if __name__ == '__main__':
    try:
        credentials = load_credentials()
        token = credentials['token']
        bot.client_id = credentials['client_id']
    except:
        print("Impossible de démarer tuxbot.")


    for extension in l_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Impossible de charger l\'extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    try:
        bot.run(token)
    except:
        print("Une erreur est survenue avec votre Token, merci de le vérifier.")

    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
