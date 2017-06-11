from discord.ext import commands
from random import choice, shuffle
import random
import aiohttp
import asyncio
import time
import discord
import urllib.request, json
import datetime, pytz

class Utility:
    """Commandes utilitaires."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clock(self, args):
        """Display hour in a country"""
        args = args.upper()
        then = datetime.datetime.now(pytz.utc)
        form = '%H heures %M'
        try:
            argument = args[1]
            if args == "MONTREAL":
                utc = then.astimezone(pytz.timezone('America/Montreal'))
                site = "http://ville.montreal.qc.ca/"
                img = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Rentier_fws_1.jpg"
                country = "au Canada, Québec"
                description = "Montréal est la deuxième ville la plus peuplée du Canada. Elle se situe dans la région du Québec"
            elif args == "VANCOUVER":
                utc = then.astimezone(pytz.timezone('America/Vancouver'))
                site = "http://vancouver.ca/"
                img = "https://upload.wikimedia.org/wikipedia/commons/f/fe/Dock_Vancouver.JPG"
                country = "au Canada"
                description = "Vancouver, officiellement City of Vancouver, est une cité portuaire au Canada"
            elif args == "NEW-YORK" or args == "N-Y":
                utc = then.astimezone(pytz.timezone('America/New_York'))
                site = "http://www1.nyc.gov/"
                img = "https://upload.wikimedia.org/wikipedia/commons/e/e3/NewYork_LibertyStatue.jpg"
                country = "aux U.S.A."
                description = "New York, est la plus grande ville des États-Unis en termes d'habitants et l'une des plus importantes du continent américain. "
            elif args == "LOSANGELES" or args == "L-A" or args == "LA" or args == "LACITY":
                utc = then.astimezone(pytz.timezone('America/Los_Angeles'))
                site = "https://www.lacity.org/"
                img = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/800px-LA_Skyline_Mountains2.jpg"
                country = "aux U.S.A."
                description = "Los Angeles est la deuxième ville la plus peuplée des États-Unis après New York. Elle est située dans le sud de l'État de Californie, sur la côte pacifique."
            elif args == "PARIS":
                utc = then.astimezone(pytz.timezone('Europe/Paris'))
                site = "http://www.paris.fr/"
                img = "https://upload.wikimedia.org/wikipedia/commons/a/af/Tour_eiffel_at_sunrise_from_the_trocadero.jpg"
                country = "en France"
                description = "Paris est la capitale de la France. Elle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien."
            elif args == "BERLIN":
                utc = then.astimezone(pytz.timezone('Europe/Berlin'))
                site = "http://www.berlin.de/"
                img = "https://upload.wikimedia.org/wikipedia/commons/9/91/Eduard_Gaertner_Schlossfreiheit.jpg"
                country = "en Allemagne"
                description = "Berlin est la capitale et la plus grande ville d'Allemagne. Située dans le nord-est du pays, elle compte environ 3,5 millions d'habitants. "
            elif args == "BERN" or args == "ZURICH" or args == "BERNE":
                utc = then.astimezone(pytz.timezone('Europe/Zurich'))
                site = "http://www.berne.ch/"
                img = "https://upload.wikimedia.org/wikipedia/commons/d/db/Justitia_Statue_02.jpg"
                country = "en Suisse"
                description = "Berne est la cinquième plus grande ville de Suisse et la capitale du canton homonyme. Depuis 1848, Berne est la « ville fédérale »."
            elif args == "TOKYO":
                utc = then.astimezone(pytz.timezone('Asia/Tokyo'))
                site = "http://www.gotokyo.org/"
                img = "https://upload.wikimedia.org/wikipedia/commons/3/37/TaroTokyo20110213-TokyoTower-01.jpg"
                country = "au Japon"
                description = "Tokyo, anciennement Edo, officiellement la préfecture métropolitaine de Tokyo, est la capitale du Japon."
            elif args == "MOSCOU":
                utc = then.astimezone(pytz.timezone('Europe/Moscow'))
                site = "https://www.mos.ru/"
                img = "https://upload.wikimedia.org/wikipedia/commons/f/f7/Andreyevsky_Zal.jpg"
                country = "en Russie"
                description = "Moscou est la capitale de la Fédération de Russie et la plus grande ville d'Europe. Moscou est situé sur la rivière Moskova. "
            try:
                if args == "LIST":
                    text = open('texts/clocks.md').read()
                    em = discord.Embed(title='Liste des Horloges', description=text, colour=0xEEEEEE)
                    await self.bot.say(embed=em)
                else:
                    tt = utc.strftime(form)
                    em = discord.Embed(title='Heure à ' + args[1].title(), description="A [{}]({}) {}, Il est **{}** ! \n {} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_".format(str(args), site, str(country), str(tt), str(description)), colour=0xEEEEEE)
                    em.set_thumbnail(url = img)
                    await self.bot.say(embed=em)
            except UnboundLocalError:
                await self.bot.say("[**Erreur**] Ville inconnue, faites ``.clock list`` pour obtenir la liste des villes")
        except IndexError:
            await self.bot.say("[**Erreur**] Ville inconnue, faites ``.clock list`` pour obtenir la liste des villes")

    @commands.command()
    async def ytdiscover(self):
        """Random youtube channel"""
        with open('texts/ytb.json') as js:
            ytb = json.load(js)

        clef = str(random.randint(0,12))
        chaine = ytb["{}".format(clef)]

        embed = discord.Embed(title=chaine['name'], url=chaine['url'],
        description="**{}**, {} \n[Je veux voir ça]({})".format(chaine['name'], chaine['desc'], chaine['url']))
        embed.set_thumbnail(url='https://outout.tech/tuxbot/yt.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def afk(self, ctx):
        """Away from keyboard"""
        msgs = ["s'absente de discord quelques instants", "se casse de son pc", "va sortir son chien", "reviens bientôt", "va nourrir son cochon", "va manger des cookies", "va manger de la poutine", "va faire caca", "va faire pipi"]
        msg = random.choice(msgs)

        await self.bot.say("**{}** {}...".format(ctx.message.author.mention, msg))

    @commands.command(pass_context=True)
    async def back(self, ctx):
        """I'm back !"""
        msgs = ["a réssuscité", "est de nouveau parmi nous", "a fini de faire caca", "a fini d'urine", "n'est plus mort", "est de nouveau sur son PC", "a fini de manger sa poutine", "a fini de danser", "s'est réveillé", "est de retour dans ce monde cruel"]
        msg = random.choice(msgs)

        await self.bot.say("**{}** {} !".format(ctx.message.author.mention, msg))


def setup(bot):
    bot.add_cog(Utility(bot))
