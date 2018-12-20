from discord.ext import commands
import discord

from .utils import checks
from .utils import db
from .utils.checks import get_user, check_date

import datetime
import random

import pymysql
import requests


class Identity:
	"""Commandes des cartes d'identité ."""

	def __init__(self, bot):
		self.bot = bot

		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SHOW TABLES LIKE 'users'""")
		result = self.cursor.fetchone()

		if not result:
			# Creation table Utilisateur si premiere fois
			sql = "CREATE TABLE users ( `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, userid TEXT null, username TEXT null, os TEXT null, config TEXT null, useravatar TEXT null, userbirth TEXT null, pays TEXT null, cidate TEXT null, cibureau TEXT null);"
			self.cursor.execute(sql)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.group(name="ci", no_pm=True, pass_context=True)
	async def _ci(self, ctx):
		"""Cartes d'identité"""
		
		if ctx.invoked_subcommand is None:
			text = open('texts/ci-info.md').read()
			em = discord.Embed(title='Commandes de carte d\'identité de TuxBot', description=text, colour=0x89C4F9)
			await ctx.send(embed=em)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@_ci.command(pass_context=True, name="show")
	async def ci_show(self, ctx, args: str = None):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		if args == None:
			user = get_user(ctx.message, ctx.author.name)
		else:
			user = get_user(ctx.message, args)

		if user:
			self.cursor.execute("""SELECT userid, username, useravatar, userbirth, cidate, cibureau, os, config, pays, id FROM users WHERE userid=%s""",(str(user.id)))
			result = self.cursor.fetchone()

			def isexist(var):
				if not var:
					return "Non renseigné."
				else:
					return var

			if not result:
				await ctx.send(f"{ctx.author.mention}> :x: Désolé mais {user.mention} est sans papier !")
			else:
				try:
					user_birth = datetime.datetime.fromisoformat(result[3])
					user_birth_day = check_date(str(user_birth.day))
					user_birth_month = check_date(str(user_birth.month))

					formated_user_birth = str(user_birth_day) + "/" + str(user_birth_month) + "/" + str(user_birth.year)

					try: ## a virer une fois le patch appliqué pour tout le monde
						cidate = datetime.datetime.fromisoformat(result[4])
						cidate_day = check_date(str(cidate.day)) ## a garder
						cidate_month = check_date(str(cidate.month)) ## a garder

						formated_cidate = str(cidate_day) + "/" + str(cidate_month) + "/" + str(cidate.year) ## a garder
					except ValueError: ## a virer une fois le patch appliqué pour tout le monde
						formated_cidate = str(result[4]).replace('-', '/') ## a virer une fois le patch appliqué pour tout le monde
						await ctx.send(f"{user.mention} vous êtes prié(e) de faire la commande `.ci update` afin de regler un probleme de date coté bdd") ## a virer une fois le patch appliqué pour tout le monde

					embed=discord.Embed(title="Carte d'identité | Communisme Linuxien")
					embed.set_author(name=result[1], icon_url=result[2])
					embed.set_thumbnail(url = result[2])
					embed.add_field(name="Nom :", value=result[1], inline=True)
					embed.add_field(name="Système d'exploitation :", value=isexist(result[6]), inline=True)
					embed.add_field(name="Configuration Système : ", value=isexist(result[7]), inline=True)
					embed.add_field(name="Date de naissance sur discord : ", value=formated_user_birth, inline=True)
					embed.add_field(name="Pays : ", value=isexist(result[8]), inline=True)
					embed.add_field(name="Profil sur le web : ", value=f"https://tuxbot.gnous.eu/users/{result[9]}", inline=True)
					embed.set_footer(text=f"Enregistré dans le bureau {result[5]} le {formated_cidate}.")
					await ctx.send(embed=embed)
				except Exception as e:
					await ctx.send(f"{ctx.author.mention}> :x: Désolé mais la carte d'identité de {user.mention} est trop longue de ce fait je ne peux te l'envoyer, essaye de l'aléger, {user.mention} :wink: !")
					await ctx.send(f':sob: Une erreur est survenue : \n {type(e).__name__}: {e}')
		else:
			return await ctx.send('Impossible de trouver l\'user.')

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="register")
	async def ci_register(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
		result = self.cursor.fetchone()

		if result:
			await ctx.send("Mais tu as déja une carte d'identité ! u_u")
		else:
			now = datetime.datetime.now()

			self.cursor.execute("""INSERT INTO users(userid, username, useravatar, userbirth, cidate, cibureau) VALUES(%s, %s, %s, %s, %s, %s)""", (str(ctx.author.id), str(ctx.author),  str(ctx.author.avatar_url_as(format="jpg", size=512)), str(ctx.author.created_at), now, str(ctx.message.guild.name)))
			self.conn.commit()
			await ctx.send(f":clap: Bievenue à toi {ctx.author.name} dans le communisme {ctx.message.guild.name} ! Fait ``.ci`` pour plus d'informations !")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="delete")
	async def ci_delete(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
		result = self.cursor.fetchone()

		if result:
			self.cursor.execute("""DELETE FROM users WHERE userid =%s""", (str(ctx.author.id)))
			self.conn.commit()
			await ctx.send("Tu es maintenant sans papiers !")
		else:
			await ctx.send("Déja enregistre ta carte d'identité avant de la supprimer u_u (après c'est pas logique...)")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="update")
	async def ci_update(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		try:
			self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
			result = self.cursor.fetchone()

			if result:
				self.cursor.execute("""SELECT cidate FROM users WHERE userid=%s""",(str(ctx.author.id)))
				old_ci_date = self.cursor.fetchone()

				try:
					new_ci_date = datetime.datetime.fromisoformat(old_ci_date[0])
				except ValueError:
					old_ci_date = datetime.datetime.strptime(old_ci_date[0].replace('/', '-'), '%d-%m-%Y')

					old_ci_date_day = check_date(str(old_ci_date.day))
					old_ci_date_month = check_date(str(old_ci_date.month))

					new_ci_date = f"{str(old_ci_date.year)}-{str(old_ci_date_month)}-{str(old_ci_date_day)} 00:00:00.000000"

					await ctx.send("succes update")

					self.cursor.execute("""UPDATE users SET cidate = %s WHERE userid = %s""", (str(new_ci_date), str(ctx.author.id)))
					self.conn.commit()

				self.cursor.execute("""UPDATE users SET useravatar = %s, username = %s, cibureau = %s WHERE userid = %s""", (str(ctx.author.avatar_url_as(format="jpg", size=512)), str(ctx.author), str(ctx.message.guild), str(ctx.author.id)))
				self.conn.commit()
				await ctx.send(f"{ctx.author.mention}> Tu viens, en quelques sortes, de renaitre !")
			else:
				await ctx.send(f"{ctx.author.mention}> :x: Veuillez enregistrer votre carte d'identité pour commencer !")

		except Exception as e: #TODO : A virer dans l'event on_error
			await ctx.send(':( Erreur veuillez contacter votre administrateur :')
			await ctx.send(f'{type(e).__name__}: {e}')

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="setconfig")
	async def ci_setconfig(self, ctx, *, conf: str = None):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		if conf:
			self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
			result = self.cursor.fetchone()

			if result:
				self.cursor.execute("""UPDATE users SET config = %s WHERE userid = %s""", (str(conf), str(ctx.author.id)))
				self.conn.commit()
				await ctx.send(f"{ctx.author.mention}> :ok_hand: Carte d'identité mise à jour !")
			else:
				await ctx.send(f"{ctx.author.mention}> :x: Veuillez enregistrer votre carte d'identité pour commencer !")
		else:
			await ctx.send(f"{ctx.author.mention}> :x: Il manque un paramètre !")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="setos")
	async def ci_setos(self, ctx, *, conf: str = None):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		if conf:
			self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
			result = self.cursor.fetchone()

			if result:
				self.cursor.execute("""UPDATE users SET os = %s WHERE userid = %s""", (str(conf), str(ctx.author.id)))
				self.conn.commit()
				await ctx.send(f"{ctx.author.mention}> :ok_hand: Carte d'identité mise à jour !")
			else:
				await ctx.send(f"{ctx.author.mention}> :x: Veuillez enregistrer votre carte d'identité pour commencer !")
		else:
			await ctx.send(f"{ctx.author.mention}> :x: Il manque un paramètre !")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="setcountry")
	async def ci_setcountry(self, ctx, *, country: str = None):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		if country:
			self.cursor.execute("""SELECT id, userid FROM users WHERE userid=%s""", (str(ctx.author.id)))
			result = self.cursor.fetchone()

			if result:
				self.cursor.execute("""UPDATE users SET pays = %s WHERE userid = %s""", (str(country), str(ctx.author.id)))
				self.conn.commit()
				await ctx.send(f"{ctx.author.mention}> :ok_hand: Carte d'identité mise à jour !")
			else:
				await ctx.send(f"{ctx.author.mention}> :x: Veuillez enregistrer votre carte d'identité pour commencer !")
		else:
			await ctx.send(f"{ctx.author.mention}> :x: Il manque un paramètre !")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@_ci.command(pass_context=True, name="online_edit")
	async def ci_online_edit(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SELECT id FROM users WHERE userid=%s""",(str(ctx.author.id)))
		result = self.cursor.fetchone()

		if not result:
			return await ctx.send(f"Déja enregistre ta carte d'identité avant de l'éditer u_u (après c'est pas logique...)")

		dm = await ctx.author.create_dm()

		try:
			def is_exist(key, value):
				self.cursor.execute("""SELECT * FROM sessions WHERE {}=%s""".format(str(key)), (str(value)))
				return self.cursor.fetchone()

			user_id = result[0]
			is_admin = '1' if str(ctx.author.id) in self.bot.config.authorized_id else '0'
			token = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'*25, 25))
			created_at = datetime.datetime.utcnow()

			while is_exist('token', token):
				token = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'*25, 25))

			if is_exist('user_id', user_id):
				self.cursor.execute("""UPDATE sessions SET is_admin = %s, token = %s, updated_at = %s WHERE user_id = %s""", (str(is_admin), str(token), str(created_at), str(user_id)))
				self.conn.commit()
			else:
				self.cursor.execute("""INSERT INTO sessions(user_id, is_admin, token, created_at, updated_at) VALUES(%s, %s, %s, %s, %s)""", (str(user_id), str(is_admin),  str(token), str(created_at), str(created_at)))
				self.conn.commit()

			embed=discord.Embed(title="Clé d'édition pour tuxweb", description=f"Voici ta clé d'édition, vas sur [https://tuxbot.gnous.eu/fr/users/{user_id}](https://tuxbot.gnous.eu/fr/users/{user_id}) puis cliques sur `editer` et entre la clé afin de pouvoir modifier ta ci", colour=0x89C4F9)
			embed.set_footer(text=f"Cette clé sera valide durant les 10 prochaines minutes, ne la communiques à personne !")
			await dm.send(embed=embed)
			await dm.send(token)

			await ctx.send(f"{ctx.author.mention} ta clé d'édition t'a été envoyée en message privé")

		except Exception as e:
			await ctx.send(f"{ctx.author.mention}, je ne peux pas t'envoyer de message privé :(. Penses à autoriser les messages privés provenant des membres du serveur pour que je puisse te donner ta clef d'édition")

	"""--------------------------------------------------------------------------------------------------------------------------"""
	
	@checks.has_permissions(administrator=True)
	@_ci.command(pass_context=True, name="list")
	async def ci_list(self, ctx):
		self.conn = db.connect_to_db(self)
		self.cursor = self.conn.cursor()

		self.cursor.execute("""SELECT id, username FROM users""")
		rows = self.cursor.fetchall()
		msg = ""
		try:
			for row in rows:
				row_id = row[0]
				row_name = row[1].encode('utf-8')
				msg += f"{str(row_id)} : {str(row_name)} \n"
			post = requests.post("https://hastebin.com/documents", data=msg)
			await ctx.send(f"{ctx.author.mention} liste posté avec succès sur :\nhttps://hastebin.com/{post.json()['key']}.txt")

			with open('ci_list.txt', 'w', encoding='utf-8') as fp:
				for row in rows:
					row_id = row[0]
					row_name = row[1]

					fp.write(f"{str(row_id)} : {str(row_name)} \n")

		except Exception as e:
			await ctx.send(f':sob: Une erreur est survenue : \n {type(e).__name__}: {e}')

def setup(bot):
	bot.add_cog(Identity(bot))
