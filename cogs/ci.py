from discord.ext import commands
from random import choice, shuffle
import aiohttp
import asyncio
import discord
import platform, socket
import os
import sqlite3

#### SQL #####
conn = sqlite3.connect('tuxbot.db') #Connexion SQL

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     userid TEXT,
     username TEXT,
     os TEXT,
     config TEXT,
     useravatar TEXT,
     userbirth TEXT,
     pays TEXT,
     cidate TEXT,
     cibureau TEXT
)
""")# Creation table Utilisateur si premiere fois
conn.commit()

class Identity:
    """Commandes des cartes d'identité ."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="ci", no_pm=True, pass_context=True)
    async def _ci(self, ctx):
        """Cartes d'identité"""
        if ctx.invoked_subcommand is None:
            text = open('texts/ci-info.md').read()
            em = discord.Embed(title='Commandes de carte d\'identité de TuxBot', description=text, colour=0x89C4F9)
            await self.bot.say(embed=em)

    @_ci.command(pass_context=True, name="show")
    async def ci_test(self, ctx, args : discord.Member):

        def isexist(var):
            if not var:
                return "Non renseigné."
            else:
                return var

        cursor.execute("""SELECT userid, username, useravatar, userbirth, cidate, cibureau, os, config, pays FROM users WHERE userid=?""",(args.id,))
        result = cursor.fetchone()

        if not result:
            await self.bot.say(ctx.message.author.mention + "> :x: Désolé mais {} est sans papier !".format(args.mention))

        else:
            try:
                userbirth = result[3].split(" ")
                cidate = result[4].split(" ")
                embed=discord.Embed(title="Carte d'identité | Communisme Linuxien")
                embed.set_author(name=result[1], icon_url=result[2])
                embed.set_thumbnail(url = result[2])
                embed.add_field(name="Nom :", value=result[1], inline=True)
                embed.add_field(name="Système d'exploitation :", value=isexist(result[6]), inline=True)
                embed.add_field(name="Configuration Système : ", value=isexist(result[7]), inline=True)
                embed.add_field(name="Date de naissance : ", value=userbirth[0], inline=True)
                embed.add_field(name="Pays : ", value=isexist(result[8]), inline=True)
                embed.set_footer(text="Enregistré dans le bureau {} le {}.".format(result[5], cidate[0]))
                await self.bot.say(embed=embed)
            except:
                await self.bot.say(ctx.message.author.mention + "> :x: Désolé mais la carte d'identité de {0} est trop longue de ce fait je ne peux te l'envoyer, essaye de l'aléger, {0} :wink: !".format(args.mention))

    @_ci.command(pass_context=True, name="register")
    async def ci_register(self, ctx):
        cursor.execute("""SELECT id, userid FROM users WHERE userid=?""", (ctx.message.author.id,))
        existansw = cursor.fetchone()
        if existansw != None:
            await self.bot.say("Mais tu as déja une carte d'identité ! u_u")
        else:
            cursor.execute("""INSERT INTO users(userid, username, useravatar, userbirth, cidate, cibureau) VALUES(?, ?, ?, ?, ?, ?)""", (ctx.message.author.id, ctx.message.author.name,  ctx.message.author.avatar_url, ctx.message.author.created_at, ctx.message.timestamp, ctx.message.server.name))
            conn.commit()
            await self.bot.say(":clap: Bievenue à toi {} dans le communisme {} ! Fait ``.ci`` pour plus d'informations !".format(ctx.message.author.name, ctx.message.server.name))

    @_ci.command(pass_context=True, name="setconfig")
    async def ci_setconfig(self, ctx, args_):
        try:
            args = ctx.message.content.split("setconfig ")
            args = args[1]
            cursor.execute("""SELECT id, userid FROM users WHERE userid=?""", (ctx.message.author.id,))
            existansw = cursor.fetchone()

            if existansw != None:
                cursor.execute("""UPDATE users SET config = ? WHERE userid = ?""", (args, ctx.message.author.id))
                conn.commit()
                await self.bot.say(ctx.message.author.mention + "> :ok_hand: Carte d'identité mise à jour !")
            else:
                await self.bot.say(ctx.message.author.mention + "> :x: Veuillez enregistrer votre carte d'identité pour commencer !")
        except:
            await self.bot.say(ctx.message.author.mention + "> :x: Il manque un paramètre !")

    @_ci.command(pass_context=True, name="setos")
    async def ci_setos(self, ctx, args_):
        try:
            args = ctx.message.content.split("setos ")
            args = args[1]
            cursor.execute("""SELECT id, userid FROM users WHERE userid=?""", (ctx.message.author.id,))
            existansw = cursor.fetchone()

            if existansw != None:
                cursor.execute("""UPDATE users SET os = ? WHERE userid = ?""", (args, ctx.message.author.id))
                conn.commit()
                await self.bot.say(ctx.message.author.mention + "> :ok_hand: Carte d'identité mise à jour !")
            else:
                await self.bot.say(ctx.message.author.mention + "> :x: Veuillez enregistrer votre carte d'identité pour commencer !")
        except:
            await self.bot.say(ctx.message.author.mention + "> :x: Il manque un paramètre !")

    @_ci.command(pass_context=True, name="setcountry")
    async def ci_setcountry(self, ctx, args):
        cursor.execute("""SELECT id, userid FROM users WHERE userid=?""", (ctx.message.author.id,))
        existansw = cursor.fetchone()

        if existansw != None:
            cursor.execute("""UPDATE users SET pays = ? WHERE userid = ?""", (args, ctx.message.author.id))
            conn.commit()
            await self.bot.say(ctx.message.author.mention + "> :ok_hand: Carte d'identité mise à jour !")
        else:
            await self.bot.say(ctx.message.author.mention + "> :x: Veuillez enregistrer votre carte d'identité pour commencer !")

    @_ci.command(pass_context=True, name="list")
    async def ci_list(self, ctx):
        cursor.execute("""SELECT id, username FROM users""")
        rows = cursor.fetchall()
        msg = ""
        try:
            for row in rows:
                msg = msg + '{0} : {1} \n'.format(row[0], row[1])
            await self.bot.say(msg)
        except:
            await self.bot.say(":x: Pas d'entrés")

def setup(bot):
    bot.add_cog(Identity(bot))
