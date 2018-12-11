from discord.ext import commands
import discord
import random
import asyncio
import datetime


class Sondage:
	"""Commandes sondage."""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def sondage(self, ctx, *, msg="help"):
		if msg != "help":
			await ctx.message.delete()
			options = msg.split(" | ")
			time = [x for x in options if x.startswith("time=")]
			if time:
				time = time[0]
				options.remove(time)
				time = int(time.strip("time="))
			else:
				time = 0
			if len(options) <= 1:
				raise commands.errors.MissingRequiredArgument
			if len(options) >= 21:
				return await ctx.send(ctx.author.mention + "> :octagonal_sign: Vous ne pouvez pas mettre plus de 20 réponses !")
			emoji = ['1⃣',
					 '2⃣',
					 '3⃣',
					 '4⃣',
					 '5⃣',
					 '6⃣',
					 '7⃣',
					 '8⃣',
					 '9⃣',
					 '🔟',
					 '0⃣',
					 '🇦',
					 '🇧',
					 '🇨',
					 '🇩',
					 '🇪',
					 '🇫',
					 '🇬',
					 '🇭',
					 '🇮'
					 ]
			to_react = []
			confirmation_msg = "**{}?**:\n\n".format(options[0].rstrip("?"))
			for idx, option in enumerate(options[1:]):
				confirmation_msg += "{} - {}\n".format(emoji[idx], option)
				to_react.append(emoji[idx])
			confirmation_msg += "*Sondage proposé par* " + \
								str(ctx.author.mention)
			if time == 0:
				confirmation_msg += ""
			else:
				confirmation_msg += "\n\nVous avez {} secondes pour voter!".\
					format(time)
			poll_msg = await ctx.send(confirmation_msg)
			for emote in to_react:
				await poll_msg.add_reaction(emote)

			if time != 0:
				await asyncio.sleep(time)

			if time != 0:
				async for message in ctx.message.channel.history():
					if message.id == poll_msg.id:
						poll_msg = message
				results = {}
				for reaction in poll_msg.reactions:
					if reaction.emoji in to_react:
						results[reaction.emoji] = reaction.count - 1
				end_msg = "Le sondage est términé. Les résultats sont:\n\n"
				for result in results:
					end_msg += "{} {} - {} votes\n".\
						format(result,
							   options[emoji.index(result)+1],
							   results[result])
				top_result = max(results, key=lambda key: results[key])
				if len([x for x in results
						if results[x] == results[top_result]]) > 1:
					top_results = []
					for key, value in results.items():
						if value == results[top_result]:
							top_results.append(options[emoji.index(key)+1])
					end_msg += "\nLes gagnants sont : {}".\
						format(", ".join(top_results))
				else:
					top_result = options[emoji.index(top_result)+1]
					end_msg += "\n\"{}\" est le gagnant!".format(top_result)
				await ctx.send(end_msg)
		else:
			await ctx.message.delete()

			text = open('texts/rpoll.md').read()
			em = discord.Embed(title='Aide sur le sondage',
							   description=text,
							   colour=0xEEEEEE)
			await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Sondage(bot))
