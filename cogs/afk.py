from discord.ext import commands
import random


class AFK:
    """Commandes utilitaires."""

    def __init__(self, bot):
        self.bot = bot

    """---------------------------------------------------------------------"""

    @commands.command(pass_context=True)
    async def afk(self, ctx):
        
        user = ctx.message.author

        try:
            await user.edit(nick="[AFK] "+str(user.name))
            author = ctx.message.author
            channel = await author.create_dm()
            await channel.send("Ton pseudo a prit le prefix `[AFK]` pour "
                               "monter que tu es absent,")
            await channel.send("tu auras juste a mettre un message pour que "
                               "je signale ton retour parmis nous et que je "
                               "retire le prefix `[AFK]` de ton pseudo 😉")

        except KeyError:
            print('')
            author = ctx.message.author
            channel = await author.create_dm()
            await channel.send("Tu auras juste a mettre un message pour que "
                               "je signale ton retour parmis nous 😉")

        msgs = ["s'absente de discord quelques instants",
                "se casse de son pc",
                "va sortir son chien",
                "reviens bientôt",
                "va nourrir son cochon",
                "va manger des cookies",
                "va manger de la poutine",
                "va faire caca",
                "va faire pipi"]
        msg = random.choice(msgs)

        await ctx.send("**{}** {}...".format(ctx.message.author.mention, msg))

    """---------------------------------------------------------------------"""


async def on_message(message):

    ni = str(message.author.nick)

    if ni:
        ni2 = ni.split(" ")
        if "[AFK]" in ni2:
            user = message.author
            await user.edit(nick=None)

            msgs = ["a réssuscité",
                    "est de nouveau parmi nous",
                    "a fini de faire caca",
                    "a fini d'uriner",
                    "n'est plus mort",
                    "est de nouveau sur son PC",
                    "a fini de manger sa poutine",
                    "a fini de danser",
                    "s'est réveillé",
                    "est de retour dans ce monde cruel"]
            msg = random.choice(msgs)

            await message.channel.send("**{}** {} !".format(
                message.author.mention, msg))


def setup(bot):
    bot.add_cog(AFK(bot))
