from discord.ext import commands
from random import choice, shuffle
import aiohttp
import asyncio
import time
import discord
import platform
from .utils import checks

class Admin:
    """Commandes secrètes d'administration."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def unload(self, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @checks.is_owner()
    @commands.command(name='reload_cog', hidden=True)
    async def _reload(self, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            await self.bot.say("Nice !")
        except Exception as e:
            await self.bot.say(':( Erreur :')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @checks.is_owner()
    @commands.command(name='clear', pass_context=True, hidden=True)
    async def _clear(self, ctx, number: int):
        try:
            number = number + 1
            await self.bot.purge_from(ctx.message.channel, limit=number)
            await self.bot.say("Hello World !")
        except Exception as e:
            await self.bot.say(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

    @checks.is_owner()
    @commands.command(name='say', pass_context=True, hidden=True)
    async def _say(self, ctx, dire):
        try:
            arg = ctx.message.content.split("say ")
            await self.bot.say(arg[1])
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            await self.bot.say(':sob: Une erreur est survenue : \n {}: {}'.format(type(e).__name__, e))

    @checks.is_owner()
    @commands.command(pass_context=True, hidden=True)
    async def _clearterm(self):
        clear = "\n" * 100
        print(clear)
        await self.bot.say(":ok_hand: It's good")

def setup(bot):
    bot.add_cog(Admin(bot))
