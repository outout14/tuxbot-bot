import aiohttp
import datetime
import discord
import imghdr
import os
import shutil
from PIL import Image
from PIL import ImageOps
from discord.ext import commands

from .utils import db
from .utils.checks import get_user
from .utils.passport_generator import generate_passport


class Passport(commands.Cog):
	"""Commandes des passeports ."""

	def __init__(self, bot):
		self.bot = bot

		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SHOW TABLES LIKE 'passport'""")
		result = self.cursor.fetchone()

		if not result:
			# Creation table Passport si premiere fois
			sql = "CREATE TABLE passport ( `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, userid TEXT null, os TEXT null, config TEXT null, languages TEXT null, pays TEXT null, passportdate TEXT null, theme CHAR(5) DEFAULT 'dark');"
			self.cursor.execute(sql)

	@commands.group(pass_context=True)
	async def passeport(self, ctx):
		"""Passeport"""

		if ctx.invoked_subcommand is None:
			text = open('texts/passport-info.md').read()
			em = discord.Embed(title='Commandes de carte de passeport de TuxBot', description=text, colour=0x89C4F9)
			await ctx.send(embed=em)

	@passeport.command(pass_context=True)
	async def show(self, ctx, user: str = None):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		if user == None:
			user = get_user(ctx.message, ctx.message.author.name)
		else:
			user = get_user(ctx.message, user)

		wait_message = await ctx.send(f"Je vais chercher le passeport de {user.name} dans les archives, je vous prie de bien vouloir patienter...")

		card = await generate_passport(self, user)
		s = 'data/users/cards/{0}.png'.format(user.id)

		card.save(s, 'png')

		with open('data/users/cards/{0}.png'.format(user.id), 'rb') as g:
			await ctx.message.channel.send(file=discord.File(g))
			await wait_message.delete()

	@passeport.command(name="config", pass_context=True)
	async def passeport_config(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		await ctx.send('Un message privé vous a été envoyé pour configurer votre passeport.')

		questions = ["Système(s) d'exploitation :", "Configuration Système :", "Langages de programmation préférés :", "Pays :"]
		answers = {}

		user_dm = await ctx.author.create_dm()

		try:
			await user_dm.send("Salut ! Je vais vous posez quelques questions afin de configurer votre passeport, si vous ne voulez pas répondre à une question, envoyez `skip` pour passer à la question suivante.")
		except discord.HTTPException:
			await ctx.send(f"{str(ctx.message.author.mention)}> il m'est impossible de vous envoyer les messages nécessaire a la configuration de votre passeport :sob:")
			return

		for x, question in enumerate(questions):
			await user_dm.send(question)

			def check(m):
				return m.channel.id == user_dm.id and m.author.id == user_dm.recipient.id

			answer = await self.bot.wait_for('message', check=check)
			if answer.content.lower() == 'skip':
				answers[x] = 'n/a'
			else:
				answers[x] = answer.content
		try:
			self.cursor.execute("""SELECT id, userid FROM passport WHERE userid = %s""", str(user_dm.recipient.id))
			result = self.cursor.fetchone()

			if result:
				self.cursor.execute("""UPDATE passport SET os = %s, config = %s, languages = %s, pays = %s WHERE userid = %s""", (str(answers[0]),  str(answers[1]), str(answers[2]), str(answers[3]), str(ctx.message.author.id)))
				self.conn.commit()		
			else:
				now = datetime.datetime.now()

				self.cursor.execute("""INSERT INTO passport(userid, os, config, languages, pays, passportdate, theme) VALUES(%s, %s, %s, %s, %s, %s, %s)""", (str(ctx.message.author.id), str(answers[0]),  str(answers[1]), str(answers[2]), str(answers[3]), now, "dark"))
				self.conn.commit()		
			await user_dm.send('Configuration de votre passeport terminée avec succès, vous pouvez désormais la voir en faisant `.passeport show`.')
		except Exception as e:
			await user_dm.send(f':sob: Une erreur est survenue : \n {type(e).__name__}: {e}')

	@passeport.command(name="background", pass_context=True)
	async def passeport_background(self, ctx, *, url=""):
		try:
			background = ctx.message.attachments[0].url
		except:
			if url != "":
				background = url
			else:
				em = discord.Embed(title='Une erreur est survenue', description="Image ou URL introuvable.", colour=0xDC3546)
				await ctx.send(embed=em)
				return

		user = ctx.message.author
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(background) as r:
					image = await r.content.read()
		except:
			em = discord.Embed(title='Une erreur est survenue', description="Image ou URL introuvable.", colour=0xDC3546)
			await ctx.send(embed=em)
			return

		with open(f"data/users/backgrounds/{str(user.id)}.png",'wb') as f:
			f.write(image)

			isImage = imghdr.what(f"data/users/backgrounds/{str(user.id)}.png")

			if isImage == 'png' or isImage == 'jpeg' or isImage == 'jpg' or isImage == 'gif':
				f.close()
				em = discord.Embed(title='Configuration terminée', description="Fond d'écran enregistré et configuré avec succes", colour=0x28a745)
				await ctx.send(embed=em)
			else:
				f.close()
				os.remove(f"data/users/backgrounds/{str(user.id)}.png")
				em = discord.Embed(title='Une erreur est survenue', description="Est-ce bien une image que vous avez envoyé ? :thinking:", colour=0xDC3546)
				await ctx.send(embed=em)

	@passeport.command(name="theme", aliases=["thème"], pass_context=True)
	async def passeport_theme(self, ctx, theme: str = ""):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		possible_theme = ["dark", "light", "preview"]

		if theme.lower() in possible_theme:
			if theme.lower() == "dark":
				self.cursor.execute("""UPDATE passport SET theme = %s WHERE userid = %s""", ("dark", str(ctx.message.author.id)))
				self.conn.commit()

				em = discord.Embed(title='Configuration terminée', description="Thème enregistré avec succes", colour=0x28a745)
				await ctx.send(embed=em)
			elif theme.lower() == "light":
				self.cursor.execute("""UPDATE passport SET theme = %s WHERE userid = %s""", ("light", str(ctx.message.author.id)))
				self.conn.commit()

				em = discord.Embed(title='Configuration terminée', description="Thème enregistré avec succes", colour=0x28a745)
				await ctx.send(embed=em)
			else:
				wait_message = await ctx.send(f"Laissez moi juste le temps de superposer les 2 passeports, je vous prie de bien vouloir patienter...")
				cardbg = Image.new('RGBA', (1600, 500), (0, 0, 0, 255))

				card_dark = await generate_passport(self, ctx.author, "dark")
				card_dark.save(f'data/tmp/{ctx.author.id}_dark.png', 'png')

				card_light = await generate_passport(self, ctx.author, "light")
				card_light.save(f'data/tmp/{ctx.author.id}_light.png', 'png')

				saved_card_dark = Image.open(f'data/tmp/{ctx.author.id}_dark.png')
				saved_card_light = Image.open(f'data/tmp/{ctx.author.id}_light.png')

				saved_card_dark = ImageOps.fit(saved_card_dark, (800, 500))
				saved_card_light = ImageOps.fit(saved_card_light, (800, 500))

				cardbg.paste(saved_card_dark, (0, 0))
				cardbg.paste(saved_card_light, (800, 0))

				cardbg.save(f'data/tmp/{ctx.author.id}.png', 'png')

				with open(f'data/tmp/{ctx.author.id}.png', 'rb') as g:
					await ctx.send(file=discord.File(g))
					await wait_message.delete()
					await ctx.send(f"Et voila {ctx.author.mention} ! à gauche votre passeport avec le thème \"dark\" et à droite avec le thème \"light\" :wink:")

				shutil.rmtree("data/tmp")
				os.mkdir("data/tmp")

		else:
			em = discord.Embed(title='Une erreur est survenue', description="Les choix possible pour cette commande sont : `dark`, `light`, `preview`", colour=0xDC3546)
			await ctx.send(embed=em)

	@passeport.command(name="delete", pass_context=True)
	async def passeport_delete(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SELECT id, userid FROM passport WHERE userid = %s""", str(ctx.author.id))
		result = self.cursor.fetchone()

		if result:
			def check(m):
				return m.author.id == ctx.author.id and \
						m.channel.id == ctx.channel.id

			await ctx.send(f"{str(ctx.message.author.mention)}> envoyez `CONFIRMER` afin de supprimer vos données conformément à l'article 17 du `règlement général sur la protection des données` sur le `Droit à l'effacement`")
			response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
			if response.content == "CONFIRMER":
				os.remove(f"data/users/backgrounds/{str(ctx.author.id)}.png")
				self.cursor.execute("""DELETE FROM passport WHERE userid =%s""", (str(ctx.message.author.id)))
				self.conn.commit()

				em = discord.Embed(title='Suppression confirmée', description="Vos données ont été supprimées avec succès", colour=0x28a745)
				await ctx.send(embed=em)
		else:
			await ctx.send("Déja configure ton passeport avant de la supprimer u_u (après c'est pas logique...)")

def setup(bot):
	bot.add_cog(Passport(bot))
