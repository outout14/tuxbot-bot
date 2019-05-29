from discord.ext import commands
import discord
import random


class AFK(commands.Cog):
    """Commandes utilitaires."""

    def __init__(self, bot):
        self.bot = bot
        self.afk_users = []

    """---------------------------------------------------------------------"""

    @commands.command(pass_context=True)
    async def afk(self, ctx, action: str = ""):

        if action.lower() == "list":
            try:
                await ctx.send(*self.afk_users)
            except discord.HTTPException:
                await ctx.send("Il n'y a personne d'afk...")
        else:
            user = ctx.author
            self.afk_users.append(user)
            msgs = ["s'absente de discord quelques instants",
                    "se casse de son pc",
                    "va sortir son chien",
                    "reviens bientôt",
                    "va nourrir son cochon",
                    "va manger des cookies",
                    "va manger de la poutine",
                    "va faire caca",
                    "va faire pipi"]

            await ctx.send(f"**{user.mention}** {random.choice(msgs)}...")

    """---------------------------------------------------------------------"""

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot \
                or message.guild.id != int(self.bot.config.main_server_id):
            return

        user = message.author

        if user in self.afk_users \
                and message.content != self.bot.config.prefix[0] + "afk":
            self.afk_users.remove(user)

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

            await message.channel.send(f"**{user.mention}**"
                                       f" {random.choice(msgs)}...")


def setup(bot):
    bot.add_cog(AFK(bot))
