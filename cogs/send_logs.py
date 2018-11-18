from discord.ext import commands
import discord

import datetime, socket

class SendLogs:
	"""Send logs to a specific channel"""

	def __init__(self, bot):

		self.bot = bot
		self.log_channel = None
		self.main_server_id = int(self.bot.config.main_server_id)

	async def on_resumed(self):
		em = discord.Embed(title="Et hop je me reconnecte à l'api 😃", colour=0x5cb85c)
		em.timestamp = datetime.datetime.utcnow()
		await self.log_channel.send(embed=em)

	async def on_ready(self):
		self.log_channel = self.bot.get_channel(int(self.bot.config.log_channel_id))
		em = discord.Embed(title="Je suis opérationnel 😃", description=f"*Instance lancée sur {socket.gethostname()}*", colour=0x5cb85c)
		em.timestamp = datetime.datetime.utcnow()
		await self.log_channel.send(embed=em)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	async def on_guild_join(self, guild: discord.Guild):
		em = discord.Embed(title=f"On m'a ajouté à  : {str(guild.name)} 😃", colour=0x51A351)
		em.timestamp = datetime.datetime.utcnow()
		await self.log_channel.send(embed=em)

	async def on_guild_remove(self, guild: discord.Guild):
		em = discord.Embed(title=f"On m'a viré de  : {str(guild.name)} 😦", colour=0xBD362F)
		em.timestamp = datetime.datetime.utcnow()
		await self.log_channel.send(embed=em)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	async def on_member_join(self, member):
		if member.guild.id == self.main_server_id:
			em = discord.Embed(title=f"{str(member)} *`({str(member.id)})`* nous a rejoint 😃", colour=0x51A351)
			em.set_footer(text="Compte crée le " + str(member.created_at), )
			em.timestamp = datetime.datetime.utcnow()
			await self.log_channel.send(embed=em)

	async def on_member_remove(self, member):
		if member.guild.id == self.main_server_id:
			em = discord.Embed(title=f"{str(member)} *`({str(member.id)})`* nous a quitter 😦", colour=0xBD362F)
			em.timestamp = datetime.datetime.utcnow()
			await self.log_channel.send(embed=em)

	"""--------------------------------------------------------------------------------------------------------------------------"""

	async def on_message_delete(self, message):
		if message.guild.id == self.main_server_id and not message.author.bot:
			async def is_a_command(message):
				prefix_lenght = len(await self.bot.get_prefix(message))
				command = (message.content.split()[0])[prefix_lenght:]
				if command == '':
					command = "not_a_command"

				return self.bot.get_command(str(command))
				
			if await is_a_command(message) is None:
				em = discord.Embed(title=f"Message supprimé dans : {str(message.channel.name)}", colour=0xBD362F)
				em.add_field(name=f"{str(message.author)} *`({str(message.author.id)})`* a supprimé :", value=str(message.content))
				em.timestamp = datetime.datetime.utcnow()
				await self.log_channel.send(embed=em)

	async def on_message_edit(self, before, after):
		if before.guild.id == self.main_server_id and not before.author.bot:
			em = discord.Embed(title="Message edité dans : " + str(before.channel.name), colour=0x0088CC)
			em.add_field(name=f"{str(before.author)} *`({str(before.author.id)})`* a edité :", value=str(before.content))
			em.add_field(name="Pour remplacer par :", value=str(after.content))
			em.timestamp = datetime.datetime.utcnow()
			await self.log_channel.send(embed=em)

def setup(bot):
	bot.add_cog(SendLogs(bot))
