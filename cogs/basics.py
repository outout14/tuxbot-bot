import platform
import socket
import subprocess

import discord
from discord.ext import commands
from discord.http import Route


class Basics(commands.Cog):
    """Commandes générales."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping_res = str(subprocess.Popen(["/bin/ping", "-c1", "discordapp.com"],
                                        stdout=subprocess.PIPE).stdout.read())
        formated_res = [item for item in ping_res.split() if 'time=' in item]
        result = str(formated_res[0])[5:]

        if float(result) >= 200:
            em = discord.Embed(title="Ping : " + str(result) + "ms",
                               description="... c'est quoi ce ping !",
                               colour=0xFF1111)
            await ctx.send(embed=em)
        elif float(result) > 100 < 200:
            em = discord.Embed(title="Ping : " + str(result) + "ms",
                               description="Ca va, ça peut aller, mais j'ai "
                                           "l'impression d'avoir 40 ans !",
                               colour=0xFFA500)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Ping : " + str(result) + "ms",
                               description="Wow c'te vitesse de réaction, "
                                           "je m'épate moi-même !",
                               colour=0x11FF11)
            await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @commands.command()
    async def info(self, ctx):
        """Affiches des informations sur le bot"""
        text = open('texts/info.md').read()
        os_info = str(platform.system()) + " / " + str(platform.release())
        em = discord.Embed(title='Informations sur TuxBot',
                           description=text.format(os_info,
                                                   platform.python_version(),
                                                   socket.gethostname(),
                                                   discord.__version__,
                                                   Route.BASE),
                           colour=0x89C4F9)
        em.set_footer(text="/home/****/bot.py")
        await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @commands.command()
    async def help(self, ctx):
        """Affiches l'aide du bot"""
        text = open('texts/help.md').read()
        text = text.split("[split]")
        for text_result in text:
            em = discord.Embed(title='Commandes de TuxBot', description=text_result,colour=0x89C4F9)
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Basics(bot))
