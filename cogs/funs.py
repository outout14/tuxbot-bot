from discord.ext import commands
import asyncio
import discord
import urllib.request
import json
import random
import requests


class Funs:
	"""Commandes funs."""

	def __init__(self, bot):
		self.bot = bot

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def avatar(self, ctx, user: discord.Member = None):
		"""Récuperer l'avatar de ..."""

		if user == None:
			user = ctx.message.author

		embed = discord.Embed(title="Avatar de : " + user.name,
							  url=user.avatar_url_as(format="png"),
							  description=f"[Voir en plus grand]({user.avatar_url_as(format='png')})")
		embed.set_thumbnail(url=user.avatar_url_as(format="png"))
		await ctx.send(embed=embed)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command(pass_context=True)
	async def poke(self, ctx, user: discord.Member):
		"""Poke quelqu'un"""
		await ctx.send(":clap: Hey {0} tu t'es fait poker par {1} !".format(
			user.mention, ctx.message.author.name))
		await ctx.message.delete()

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@commands.command()
	async def btcprice(self, ctx):
		"""Le prix du BTC"""
		loading = await ctx.send("_réfléchis..._")
		try:
			url = urllib.request.urlopen("https://blockchain.info/fr/ticker")
			btc = json.loads(url.read().decode())
		except KeyError:
			btc = 1

		if btc == 1:
			await loading.edit(content="Impossible d'accèder à l'API blockchain.info, "
						   "veuillez réessayer ultérieurment ! :c")
		else:
			frbtc = str(btc["EUR"]["last"]).replace(".", ",")
			usbtc = str(btc["USD"]["last"]).replace(".", ",")
			await loading.edit(content="Un bitcoin est égal à : {0}$US soit {1}€.".format(usbtc, frbtc))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def joke(self, ctx, number:str = 0):
		"""Print a random joke in a json file"""
		with open('texts/jokes.json') as js:
			jk = json.load(js)

		try:
			if int(number) <= 15 and int(number) > 0:
				clef = str(number)
			else:
				clef = str(random.randint(1,15))
		except:
			clef = str(random.randint(1,15))


		joke = jk["{}".format(clef)]

		embed = discord.Embed(title="Blague _{}_ : ".format(clef), description=joke['content'], colour=0x03C9A9)
		embed.set_footer(text="Par " + joke['author'])
		embed.set_thumbnail(url='https://outout.tech/tuxbot/blobjoy.png')
		await ctx.send(embed=embed)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def ethylotest(self, ctx):
		"""Ethylotest simulator 2018"""
		results_poulet = ["Désolé mais mon ethylotest est sous Windows Vista, "
						  "merci de patienter...",
						  "_(ethylotest)_ : Une erreur est survenue. Windows "
						  "cherche une solution à se problème.",
						  "Mais j'l'ai foutu où ce p\\*\\*\\* d'ethylotest de m\\*\\*\\* "
						  "bordel fait ch\\*\\*\\*",
						  "C'est pas possible z'avez cassé l'ethylotest !"]
		results_client = ["D'accord, il n'y a pas de problème à cela je suis "
						  "complètement clean",
						  "Bien sur si c'est votre devoir !", "Suce bi\\*e !",
						  "J'ai l'air d'être bourré ?",
						  "_laissez moi prendre un bonbon à la menthe..._"]

		result_p = random.choice(results_poulet)
		result_c = random.choice(results_client)

		await ctx.send(":oncoming_police_car: Bonjour bonjour, contrôle "
					   "d'alcoolémie !")
		await asyncio.sleep(0.5)
		await ctx.send(":man: " + result_c)
		await asyncio.sleep(1)
		await ctx.send(":police_car: " + result_p)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def coin(self, ctx):
		"""Coin flip simulator 2025"""
		starts_msg = ["Je lance la pièce !", "C'est parti !", "C'est une pièce"
															  " d'un cent faut"
															  " pas la perdre",
					  "C'est une pièce d'un euro faut pas la perdre",
					  "Je lance !"]
		results_coin = ["{0} pile", "{0} face", "{1} Heu c'est quoi pile c'est"
												" quoi face enfaite ?",
						"{1} Oh shit, je crois que je l'ai perdue",
						"{1} Et bim je te vol ta pièce !",
						"{0} Oh une erreur d'impression il n'y a ni pile ni"
						" face !"]

		start = random.choice(starts_msg)
		result = random.choice(results_coin)

		await ctx.send(start)
		await asyncio.sleep(0.6)
		await ctx.send(result.format(":moneybag: Et la pièce retombe sur ...",
									 ":robot:"))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def pokemon(self, ctx):
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
		except KeyError:
			winer = poke1

		await ctx.send(":flag_white: **Le combat commence !**")
		await asyncio.sleep(1)
		await ctx.send(":loudspeaker: Les concurants sont {} contre {} ! Bonne"
					   " chance à eux !".format(poke1["Name"], poke2["Name"]))
		await asyncio.sleep(0.5)
		await ctx.send(":boom: {} commence et utilise {}".format(
			poke1["Name"], poke1["Fast Attack(s)"][0]["Name"]))
		await asyncio.sleep(1)
		await ctx.send(":dash: {} réplique avec {}".format(
			poke2["Name"], poke2["Fast Attack(s)"][0]["Name"]))
		await asyncio.sleep(1.2)
		await ctx.send("_le combat continue de se dérouler..._")
		await asyncio.sleep(1.5)
		await ctx.send(":trophy: Le gagnant est **{}** !".format(
			winer["Name"]))

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command()
	async def randomcat(self, ctx):
		"""Display a random cat"""
		r = requests.get('http://aws.random.cat/meow')
		cat = str(r.json()['file'])
		embed = discord.Embed(title="Meow",
							  description="[Voir le chat plus grand]({})".
							  format(cat), colour=0x03C9A9)
		embed.set_thumbnail(url=cat)
		embed.set_author(name="Random.cat", url='https://random.cat/')
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Funs(bot))
