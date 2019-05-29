from discord.ext import commands
import re


class FilterMessages(commands.Cog):
    """Flitre des messages"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        no_pub_guild = [280805240977227776, 303633056944881686,
                        274247231534792704]
        lien_channel = [280805783795662848, 508794201509593088,
                        516017286948061204]
        sondage_channel = [394146769107419146, 477147964393914388]

        if message.author.bot \
                or str(message.author.id) in self.bot.config.authorized_id \
                or message.channel.permissions_for(message.author).administrator is True:
            return

        discord_invite_regex = re.compile(r"(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/[0-9A-Za-z]*", re.IGNORECASE)
        invalid_link_regex = re.compile(r"^(\[[^\]]+\]|<\:[a-z0-9]+\:[0-9]+>) .+ https?:\/\/\S*$", re.IGNORECASE)

        try:
            if message.guild.id in no_pub_guild:
                if isinstance(discord_invite_regex.search(message.content), re.Match):
                    author = self.bot.get_user(message.author.id)
                    await message.delete()
                    await author.send("La pub pour les serveurs discord n'est pas autorisée ici")

            if message.channel.id in lien_channel \
                    and not isinstance(invalid_link_regex.search(message.content), re.Match):
                author = self.bot.get_user(message.author.id)
                await message.delete()
                await author.send(f"Votre message `{message.content}` a été "
                                  f"supprimé du channel `liens` ou `projets` "
                                  f"car il ne respecte pas la structure "
                                  f"définie. Pour partager un lien veuillez "
                                  f"suivre la structure suivante :"
                                  f" ` [Sujet] Descirption http(s)://....`")
                await author.send("Si vous voulez commenter ou discuter à "
                                  "propos d'un lien ou d'un projet, veuillez "
                                  "le faire dans le channel"
                                  " `#discussion-des-liens` ou"
                                  " `#discussion-projets`.")

            if message.channel.id in sondage_channel:
                prefix_lenght = len(await self.bot.get_prefix(message))
                command = (message.content.split()[0])[prefix_lenght:]
                if command != "sondage":
                    await message.delete()
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(FilterMessages(bot))
