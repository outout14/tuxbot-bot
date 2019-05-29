#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Maël / Outout | Romain"
__licence__ = "WTFPL Licence 2.0"

import copy
import datetime
import os
import sys
import traceback

import aiohttp
import discord
from discord.ext import commands

import cogs.utils.cli_colors as colors
import config
from cogs.utils import checks

l_extensions = (
    'cogs.admin',
    'cogs.afk',
    'cogs.atc',
    'cogs.basics',
    'cogs.ci',
    'cogs.cog_manager',
    'cogs.filter_messages',
    'cogs.funs',
    'cogs.passport',
    'cogs.role',
    'cogs.search',
    'cogs.send_logs',
    'cogs.sondage',
    'cogs.utility',
    'cogs.vocal',
)

help_attrs = dict(hidden=True, in_help=True, name="DONOTUSE")


class TuxBot(commands.Bot):
    def __init__(self):
        self.uptime = datetime.datetime.utcnow()
        self.config = config
        super().__init__(command_prefix=self.config.prefix[0],
                         description=self.config.description,
                         pm_help=None,
                        help_command = None
        )

        self.client_id = self.config.client_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self._events = []

        self.add_command(self.do)

        for extension in l_extensions:
            try:
                self.load_extension(extension)
                print(f"{colors.text_colors.GREEN}\"{extension}\""
                      f" chargé !{colors.ENDC}")
            except Exception as e:
                print(f"{colors.text_colors.RED}"
                      f"Impossible de charger l'extension {extension}\n"
                      f"{type(e).__name__}: {e}{colors.ENDC}", file=sys.stderr)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('Cette commande ne peut pas être utilisée '
                                  'en message privé.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Desolé mais cette commande est desactivée, '
                                  'elle ne peut donc pas être utilisée.')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f'{error.original.__class__.__name__}: {error.original}',
                  file=sys.stderr)

    async def on_ready(self):
        log_channel_id = self.get_channel(int(self.config.log_channel_id))

        print('\n\n---------------------')
        print('CONNECTÉ :')
        print(f'Nom d\'utilisateur: {self.user} {colors.text_style.DIM}'
              f'(ID: {self.user.id}){colors.ENDC}')
        print(f'Salon de journalisation: {log_channel_id} {colors.text_style.DIM}'
              f'(ID: {log_channel_id.id}){colors.ENDC}')
        print(f'Prefix: {self.config.prefix[0]}')
        print('Merci d\'utiliser TuxBot')
        print('---------------------\n\n')

        await self.change_presence(status=discord.Status.dnd,
                                   activity=discord.Game(
                                       name=self.config.game),
                                   )

    @staticmethod
    async def on_resumed():
        print('resumed...')

    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            await self.process_commands(message)
        except Exception as e:
            print(f'{colors.text_colors.RED}Erreur rencontré : \n'
                  f' {type(e).__name__}: {e}{colors.ENDC} \n \n')

    def run(self):
        super().run(self.config.token, reconnect=True)

    @checks.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def do(self, ctx, times: int, *, command):
        """Repeats a command a specified number of times."""
        msg = copy.copy(ctx.message)
        msg.content = command
        for i in range(times):
            await self.process_commands(msg)


if __name__ == '__main__':
    if os.path.exists('config.py') is not True:
        print(f"{colors.text_colors.RED}"
              f"Veuillez créer le fichier config.py{colors.ENDC}")
        exit()

    tuxbot = TuxBot()
    tuxbot.run()
