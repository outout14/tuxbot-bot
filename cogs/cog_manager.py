from discord.ext import commands
import discord
from .utils import checks
from .utils.paginator import HelpPaginator


class CogManager(commands.Cog):
    """Gestionnaire des cogs"""

    def __init__(self, bot):
        self.bot = bot
        self.help = discord.Embed(title='Tuxbot - Commandes cogs', description="Tuxbot - Commandes cogs\n"
                                                                               "-> .cogs <load/unload/reload/info> *{cog}* : <load/unload/reload/info> *{cog}*\n"
                                                                               "-> .cogs <list> : donne la liste de tous les cogs\n"
                                                                               "-> .cogs <null/!(load/unload/reload)>: affiche cette aide", colour=0x89C4F9)

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.group(name="cogs", no_pm=True, pass_context=True,
                    case_insensitive=True)
    async def _cogs(self, ctx):
        """show help about 'cogs' command"""

        if ctx.invoked_subcommand is None:
            await ctx.send(embed=self.help)

    """---------------------------------------------------------------------"""

    @_cogs.command(name="load", pass_context=True)
    async def cogs_load(self, ctx, cog: str = ""):
        """load a cog"""
        if cog != "":
            try:
                self.bot.load_extension(cog)

                await ctx.send('\N{OK HAND SIGN}')
                print("cog : " + str(cog) + " chargé")
            except Exception as e:
                await ctx.send('\N{PISTOL}')
                await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(embed=self.help)

    """---------------------------------------------------------------------"""

    @_cogs.command(name="unload", pass_context=True)
    async def cogs_unload(self, ctx, cog: str = ""):
        """unload a cog"""
        if cog != "":
            try:
                self.bot.unload_extension(cog)

                await ctx.send('\N{OK HAND SIGN}')
                print("cog : " + str(cog) + " déchargé")
            except Exception as e:
                await ctx.send('\N{PISTOL}')
                await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(embed=self.help)

    """---------------------------------------------------------------------"""

    @_cogs.command(name="reload", pass_context=True)
    async def cogs_reload(self, ctx, cog: str = ""):
        """reload a cog"""
        if cog != "":
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

                await ctx.send('\N{OK HAND SIGN}')
                print("cog : " + str(cog) + " rechargé")
            except Exception as e:
                await ctx.send('\N{PISTOL}')
                await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(embed=self.help)

    """---------------------------------------------------------------------"""

    @_cogs.command(name="info", pass_context=True)
    async def cogs_info(self, ctx, cog: str = ""):
        """show info about a cog"""
        if cog != "":
            try:
                entity = self.bot.get_cog(cog)

                if entity is None:
                    clean = cog.replace('@', '@\u200b')
                    await ctx.send(f'Command or category "{clean}" not found.')
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)
                    await p.paginate()

            except Exception as e:
                await ctx.send('\N{PISTOL}')
                await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(embed=self.help)

    """---------------------------------------------------------------------"""

    @_cogs.command(name="list", pass_context=True)
    async def cogs_list(self, ctx):
        """list all cogs"""

        cogs = ""
        for cog in self.bot.cogs:
            cogs += f"{cog} *`({self.bot.cogs[cog].__module__})`*:" \
                f" {len(self.bot.get_cog_commands(cog))} commandes\n"
        await ctx.send(cogs)


def setup(bot):
    bot.add_cog(CogManager(bot))
