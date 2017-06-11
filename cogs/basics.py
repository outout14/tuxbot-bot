from discord.ext import commands
from random import choice, shuffle
import aiohttp
import asyncio
import time
import discord
import platform, socket
import os

class General:
    """Commandes générales."""

    def __init__(self, bot):
        self.bot = bot

    ##PING##
    @commands.command()
    async def ping(self):
        """Ping le bot"""
        await self.bot.say(":ping_pong: Pong !")

    ##INFO##
    @commands.command()
    async def info(self):
        """Affiches des informations sur le bot"""
        text = open('texts/info.md').read()
        os_info = str(platform.system()) + " / " + str(platform.release())
        em = discord.Embed(title='Informations sur TuxBot', description=text.format(os_info, platform.python_version(), socket.gethostname(), discord.__version__), colour=0x89C4F9)
        em.set_footer(text=os.getcwd() + "/bot.py")
        await self.bot.say(embed=em)


    ## HELP PLZ ##
    @commands.command()
    async def help(self):
        """Affiches l'aide du bot"""
        text = open('texts/help.md').read()
        em = discord.Embed(title='Commandes de TuxBot', description=text, colour=0x89C4F9)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(General(bot))
