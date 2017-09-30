from discord.ext import commands
import aiohttp
import asyncio
import time
import discord
from .utils import checks

import requests

class Admin:
    """Commandes secrètes d'administration."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(name='unload_cog', hidden=True)
    async def _unload(self, ctx, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension("cogs."+module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')
            print("cog : " + str(module) + " activé")

    """--------------------------------------------------------------------------------------------------------------------------"""

    @checks.is_owner()
    @commands.command(name='load_cog', hidden=True)
    async def _load(self, ctx, module: str):
        """Unloads a module."""
        try:
            self.bot.load_extension("cogs."+module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')
            print("cog : " + str(module) + " desactivé")

    """--------------------------------------------------------------------------------------------------------------------------"""

    @checks.is_owner()
    @commands.command(name='reload_cog', hidden=True)
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension("cogs."+module)
            self.bot.load_extension("cogs."+module)
            await ctx.send("Je te reload ca")
        except Exception as e: #TODO : A virer dans l'event on_error
            await ctx.send(':( Erreur :')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')
            print("cog : " + str(module) + " relancé")

    """--------------------------------------------------------------------------------------------------------------------------"""

    @checks.is_owner()
    @commands.command(name='clear', pass_context=True, hidden=True)
    async def _clear(self, ctx, number: int):

        await ctx.message.delete()
        if number < 1000:
            async for message in ctx.message.channel.history(limit=number):
                try:
                    await message.delete()
                except Exception as e: #TODO : A virer dans l'event on_error
                    await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))
            await ctx.send("Hop voila j'ai viré des messages! Hello World")
            print(str(number)+" messages ont été supprimés")
        else:
            await ctx.send('Trop de messages, entre un nombre < 1000')

    """--------------------------------------------------------------------------------------------------------------------------"""

    @checks.is_owner()
    @commands.command(name='say', pass_context=True, hidden=True)
    async def _say(self, ctx, *direuh:str):
        try:
            dire = ctx.message.content.split("say ")
            await ctx.message.delete()
            await ctx.send(dire[1])
        except Exception as e: #TODO : A virer dans l'event on_error
            await ctx.send(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

    """--------------------------------------------------------------------------------------------------------------------------"""

    @checks.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def _clearterm(self, ctx):
        clear = "\n" * 100
        print(clear)
        await ctx.send(":ok_hand: It's good")

    """--------------------------------------------------------------------------------------------------------------------------"""



def setup(bot):
    bot.add_cog(Admin(bot))
