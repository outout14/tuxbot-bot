import asyncio

import discord
from discord.ext import commands


class Sondage(commands.Cog):
    """Commandes sondage."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sondage(self, ctx, *, msg="help"):
        if msg != "help":
            await ctx.message.delete()
            options = msg.split(" | ")

            times = [x for x in options if x.startswith("time=")]

            if times:
                time = int(times[0].strip("time="))
                options.remove(times[0])
            else:
                time = 0

            if len(options) <= 1:
                raise commands.errors.MissingRequiredArgument
            if len(options) >= 22:
                return await ctx.send(f"{ctx.message.author.mention}> "
                                      f":octagonal_sign: Vous ne pouvez pas "
                                      f"mettre plus de 20 réponses !")

            emoji = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟', '0⃣',
                     '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
            to_react = []
            confirmation_msg = f"**{options[0].rstrip('?')}?**:\n\n"

            for idx, option in enumerate(options[1:]):
                confirmation_msg += f"{emoji[idx]} - {option}\n"
                to_react.append(emoji[idx])

            confirmation_msg += "*Sondage proposé par* " + \
                                str(ctx.message.author.mention)
            if time == 0:
                confirmation_msg += ""
            else:
                confirmation_msg += f"\n\nVous avez {time} secondes pour voter!"

            poll_msg = await ctx.send(confirmation_msg)
            for emote in to_react:
                await poll_msg.add_reaction(emote)

            if time != 0:
                await asyncio.sleep(time)
                async for message in ctx.message.channel.history():
                    if message.id == poll_msg.id:
                        poll_msg = message

                results = {}

                for reaction in poll_msg.reactions:
                    if reaction.emoji in to_react:
                        results[reaction.emoji] = reaction.count - 1
                end_msg = "Le sondage est términé. Les résultats sont:\n\n"

                for result in results:
                    end_msg += "{} {} - {} votes\n". \
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
                    end_msg += "\nLes gagnants sont : {}". \
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
