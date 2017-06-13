from discord.ext import commands
from random import choice, shuffle
import aiohttp
import asyncio
import discord
import urllib.request, json
import random
import requests

class Funs:
    """Commandes funs."""

    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def avatar(self, user : discord.Member):
        """Récuperer l'avatar de ..."""
        embed = discord.Embed(title="Avatar de : " + user.name, url=user.avatar_url, description="[Voir en plus grand]({})".format(user.avatar_url))
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command()
    async def btcprice(self):
        """Le prix du BTC"""
        loading = await self.bot.say("_réfléchis..._")
        try:
            with urllib.request.urlopen("http://api.coindesk.com/v1/bpi/currentprice/EUR.json") as url:
                data = json.loads(url.read().decode())
                btc = data['bpi']['EUR']['rate']
                btc = btc.split(".")
        except:
            btc = 1

        if btc == 1:
            await self.bot.say("Impossible d'accèder à l'API coindesk.com, veuillez réessayer ultérieurment !")
        else:
            await self.bot.edit_message(loading, "Un bitcoin est égal à : " + btc[0] + " €")

    @commands.command()
    async def joke(self):
        """Print a random joke in a json file"""
        with open('texts/jokes.json') as js:
            jk = json.load(js)

        clef = str(random.randint(1,12))
        joke = jk["{}".format(clef)]

        embed = discord.Embed(title="Blague _{}_ : ".format(clef), description=joke['content'], colour=0x03C9A9)
        embed.set_footer(text="Par " + joke['author'])
        embed.set_thumbnail(url='https://outout.tech/tuxbot/blobjoy.png')
        await self.bot.say(embed=embed)

    @commands.command()
    async def ethylotest(self):
        """Ethylotest simulator 2018"""
        results_poulet = ["Désolé mais mon ethylotest est sous Windows Vista, merci de patienter...", "_(ethylotest)_ ``Une erreur est survenue. Windows cherche une solution à se problème...``", "Mais j'l'ai foutu où ce p*** d'ethylotest de m*** bordel fait ch*** tab***", "C'est pas possible z'avez cassé l'ethylotest !"]
        results_client = ["D'accord, il n'y a pas de problème à cela je suis complètement clean", "Bien sur si c'est votre devoir !", "Suce bi** !", "J'ai l'air d'être bourré ?", "_laissez moi prendre un bonbon à la menthe..._"]

        result_p = random.choice(results_poulet)
        result_c = random.choice(results_client)

        await self.bot.say(":oncoming_police_car: Bonjour bonjour, controle d'alcoolémie !")
        await asyncio.sleep(0.5)
        await self.bot.say(":man: " + result_c)
        await asyncio.sleep(1)
        await self.bot.say(":police_car: " + result_p)

    @commands.command()
    async def coin(self):
        """Coin flip simulator 2025"""
        starts_msg = ["Je lance la pièce !", "C'est parti !", "C'est une pièce d'un cent faut pas la perdre", "C'est une pièce d'un euro faut pas la perdre", "Je lance !"]
        results_coin = ["{0} pile", "{0} face", "{1} Heu c'est quoi pile c'est quoi face enfaite ?", "{1} Oh shit, je crois que je l'ai perdue", "{1} Et bim je te vol ta pièce !", "{0} Oh une erreur d'impression il n'y a ni pile ni face !"]

        start = random.choice(starts_msg)
        result = random.choice(results_coin)

        await self.bot.say(start)
        await asyncio.sleep(0.6)
        await self.bot.say(result.format(":moneybag: Et la pièce retombe sur ...", ":robot:"))

    @commands.command()
    async def pokemon(self):
        """Random pokemon fight"""
        with open('texts/pokemons.json') as js:
            jk = json.load(js)

        poke1 = jk[random.randint(1, 150)]
        poke2 = jk[random.randint(1, 150)]

        try:
            if poke1['MaxHP'] > poke2['MaxHP']:
                winer = poke1
            else:
                winer = poke2
        except:
            winer = poke1

        await self.bot.say(":flag_white: **Le combat commence !**")
        await asyncio.sleep(1)
        await self.bot.say(":loudspeaker: Les concurants sont {} contre {} ! Bonne chance à eux !".format(poke1["Name"], poke2["Name"]))
        await asyncio.sleep(0.5)
        await self.bot.say(":boom: {} commence et utilise {}".format(poke1["Name"], poke1["Fast Attack(s)"][0]["Name"]))
        await asyncio.sleep(1)
        await self.bot.say(":dash: {} réplique avec {}".format(poke2["Name"], poke2["Fast Attack(s)"][0]["Name"]))
        await asyncio.sleep(1.2)
        await self.bot.say("_le combat continue de se dérouler..._")
        await asyncio.sleep(1.5)
        await self.bot.say(":trophy: Le gagnant est **{}** !".format(winer["Name"]))

    @commands.command()
    async def randomcat(self):
        """Display a random cat"""

        r = requests.get('http://random.cat/meow.php')
        cat = str(r.json()['file'])
        embed = discord.Embed(title="Meow", description="[Voir le chat plus grand]({})".format(cat), colour=0x03C9A9)
        embed.set_thumbnail(url=cat)
        embed.set_author(name="Random.cat", url='https://random.cat/', icon_url='http://outout.tech/tuxbot/nyancat2.gif')
        await self.bot.say(embed=embed)



def setup(bot):
    bot.add_cog(Funs(bot))
