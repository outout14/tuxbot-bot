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
    #'cogs.test',
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
        await bot.send_message(ctx.message.author, 'Cette commande ne peut pas être utilisée en message privée.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Désoler mais cette commande est désactivé, elle ne peut donc pas être utilisée.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.event
async def on_ready():
    print('---------------------')
    print('Logged in as :')
    print('Username: ' + bot.user.name)
    print('ID: ' + str(bot.user.id))
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

    try:
        await bot.process_commands(message)
    except Exception as e:
        print('Hé merde, : \n {}: {} \n \n'.format(type(e).__name__, e))

@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)

@bot.command(pass_context=True)
async def github(ctx):
    """Pour voir mon code"""
    text = "How tu veux voir mon repos Github pour me disséquer ? Pas de soucis ! Je suis un Bot, je ne ressens pas la douleur !\n https://github.com/outout14/tuxbot-bot"
    em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
    em.set_author(name='Outout', icon_url="https://avatars0.githubusercontent.com/u/14958554?v=3&s=400")
    await ctx.send(embed=em)

async def on_command_error(self, ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('Cette commande ne peut pas être utilisée en message privée.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('Désoler mais cette commande est désactivé, elle ne peut donc pas être utilisée.')
    elif isinstance(error, commands.CommandInvokeError):
        print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

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
