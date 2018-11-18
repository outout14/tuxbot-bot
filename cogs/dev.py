from discord.ext import commands
import discord


class Dev:
	"""Gestionnaire des cogs"""

	def __init__(self, bot):
		self.bot = bot

	"""--------------------------------------------------------------------------------------------------------------------------"""

	@commands.command(name="test", no_pm=True, pass_context=True, case_insensitive=True)
	async def _test(self, ctx):
		"""show help about 'cogs' command"""

		if ctx.invoked_subcommand is None:
			text = "<:python:334346615366221825>"
			em = discord.Embed(title='Some test', description=text, colour=0x89C4F9)
			await ctx.send(embed=em)


def setup(bot):
	bot.add_cog(Dev(bot))
