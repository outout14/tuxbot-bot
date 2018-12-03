#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Romain", "Maël / Outout"]
__licence__ = "WTFPL Licence 2.0"

from discord.ext import commands
import discord
from cogs.utils import checks

import datetime
import json
import copy
import traceback
import sys
import os
import aiohttp

import config
import cogs.utils.cli_colors as colors

l_extensions = [

	'cogs.admin',
	# 'cogs.afk',
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
	'cogs.utility'
]

help_attrs = dict(hidden=True, in_help=True, name="DONOTUSE")


class TuxBot(commands.Bot):
	def __init__ (self):
		self.config = config
		super().__init__(command_prefix=self.config.prefix[0], 
						  description=self.config.description,
						  pm_help=None,
						  help_attrs=help_attrs)

		self.client_id = self.config.client_id
		self.session = aiohttp.ClientSession(loop=self.loop)
		self._events = []


		self.add_command(self.do)

		for extension in l_extensions:
			try:
				self.load_extension(extension)
				print(f"{colors.text_colors.GREEN}\"{extension}\" chargé !{colors.ENDC}")
			except Exception as e:
				print(f"{colors.text_colors.RED}Impossible de charger l'extension {extension}\n{type(e).__name__}: {e}{colors.ENDC}", file=sys.stderr)

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.NoPrivateMessage):
			await ctx.author.send('Cette commande ne peut pas être utilisee en message privee.')
		elif isinstance(error, commands.DisabledCommand):
			await ctx.author.send('Desoler mais cette commande est desactive, elle ne peut donc pas être utilisée.')
		elif isinstance(error, commands.CommandInvokeError):
			print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
			traceback.print_tb(error.original.__traceback__)
			print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

	async def on_ready(self):
		if not hasattr(self, 'uptime'):
			self.uptime = datetime.datetime.utcnow()

		log_channel_id = self.get_channel(int(self.config.log_channel_id))

		print('\n\n---------------------')
		print('CONNECTÉ :')
		print(f'Nom d\'utilisateur: {self.user} {colors.text_style.DIM}(ID: {self.user.id}){colors.ENDC}')
		print(f'Channel de log: {log_channel_id} {colors.text_style.DIM}(ID: {log_channel_id.id}){colors.ENDC}')
		print(f'Prefix: {self.config.prefix[0]}')
		print('Merci d\'utiliser TuxBot')
		print('---------------------\n\n')

		await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name=self.config.game))

	async def on_resumed():
		print('resumed...')

	async def on_message(self, message):
		if message.author.bot:
			return

		try:
			await self.process_commands(message)
		except Exception as e:
			print(f'{colors.text_colors.RED}Erreur rencontré : \n {type(e).__name__}: {e}{colors.ENDC} \n \n')

	def run(self):
		super().run(self.config.token, reconnect=True)

	@checks.has_permissions(administrator=True)
	@commands.command(pass_context=True, hidden=True)
	async def do(ctx, times: int, *, command):
		"""Repeats a command a specified number of times."""
		msg = copy.copy(ctx.message)
		msg.content = command
		for i in range(times):
			await bot.process_commands(msg)

## LOAD ##
if __name__ == '__main__':
	if os.path.exists('config.py') is not True:
		print(f"{colors.text_colors.RED}Veuillez créer le fichier config.py{colors.ENDC}"); exit()
	
	tuxbot = TuxBot()
	tuxbot.run()
