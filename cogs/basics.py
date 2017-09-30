from discord.ext import commands
from random import choice, shuffle
import aiohttp
import asyncio
import time
import discord
import platform, socket
import os

import wikipedia, bs4

class General:
    """Commandes générales."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()

        result = round((t2-t1)*1000)

        if int(result) >=200:
            em = discord.Embed(title="Ping : " + str(result) + "ms", description="... c'est quoi ce ping !", colour=0xFF1111)
            await ctx.send(embed=em)
        elif int(result) > 100 and int(result) < 200:
            em = discord.Embed(title="Ping : " + str(result) + "ms", description="Ca va, ça peut aller, mais j'ai l'impression d'avoir 40 ans !", colour=0xFFA500)
            await ctx.send(embed=em)
        elif int(result) <= 100:
            em = discord.Embed(title="Ping : " + str(result) + "ms", description="Wow c'te vitesse de réaction, je m'épate moi-même !",colour=0x11FF11)
            await ctx.send(embed=em)

    ##INFO##
    @commands.command()
    async def info(self, ctx):
        """Affiches des informations sur le bot"""
        text = open('texts/info.md').read()
        os_info = str(platform.system()) + " / " + str(platform.release())
        em = discord.Embed(title='Informations sur TuxBot', description=text.format(os_info, platform.python_version(), socket.gethostname(), discord.__version__), colour=0x89C4F9)
        em.set_footer(text=os.getcwd() + "/bot.py")
        await ctx.send(embed=em)


    ## HELP PLZ ##
    @commands.command()
    async def help(self, ctx):
        """Affiches l'aide du bot"""
        text = open('texts/help.md').read()
        em = discord.Embed(title='Commandes de TuxBot', description=text, colour=0x89C4F9)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(General(bot))
