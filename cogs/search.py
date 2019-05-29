from discord.ext import commands
import discord
import asyncio
import urllib.request
import wikipedia

wikipedia.set_lang("fr")


class Search(commands.Cog):
    """Commandes de WWW."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="search", no_pm=True, pass_context=True)
    async def _search(self, ctx):
        """Rechercher sur le world wide web"""
        if ctx.invoked_subcommand is None:
            text = open('texts/search.md').read()
            em = discord.Embed(title='Commandes de search TuxBot',
                               description=text,
                               colour=0x89C4F9)
            await ctx.send(embed=em)

    @_search.command(pass_context=True, name="docubuntu")
    async def search_docubuntu(self, ctx, args):
        attends = await ctx.send("_Je te cherche ça {} !_".format(
            ctx.message.author.mention))
        html = urllib.request.urlopen("https://doc.ubuntu-fr.org/" +
                                      args).read()
        if "avez suivi un lien" in str(html):
            await attends.edit(content=":sob: Nooooon ! Cette page n'existe "
                                       "pas, mais tu peux toujours la créer : "
                                       "https://doc.ubuntu-fr.org/" + args)
        else:
            await attends.delete()
            embed = discord.Embed(description="Voila j'ai trouvé ! Voici la "
                                              "page ramenant à votre recherche,"
                                              " toujours aussi bien rédigée "
                                              ":wink: : https://doc.ubuntu-fr."
                                              "org/" + args,
                                  url='http://doc.ubuntu-fr.org/')
            embed.set_author(name="DocUbuntu-Fr",
                             url='http://doc.ubuntu-fr.org/',
                             icon_url='https://tuxbot.outout.xyz/data/ubuntu.png')
            embed.set_thumbnail(url='https://tuxbot.outout.xyz/data/ubuntu.png')
            embed.set_footer(text="Merci à ceux qui ont pris le temps d'écrire "
                                  "cette documentation")
            await ctx.send(embed=embed)

    @_search.command(pass_context=True, name="docarch")
    async def search_docarch(self, ctx, args):
        attends = await ctx.send("_Je te cherche ça {} !_".format(
            ctx.message.author.mention))
        html = urllib.request.urlopen("https://wiki.archlinux.org/index.php/" +
                                      args).read()
        if "There is currently no text in this page" in str(html):
            await attends.edit(content=":sob: Nooooon ! Cette page n'existe "
                                       "pas.")
        else:
            await attends.delete()
            embed = discord.Embed(description="Voila j'ai trouvé ! Voici la "
                                              "page ramenant à votre recherche,"
                                              " toujours aussi bien rédigée "
                                              ":wink: : https://wiki.archlinux."
                                              "org/index.php/" + args,
                                  url='https://wiki.archlinux.org/index.php/')
            embed.set_author(name="Doc ArchLinux",
                             url='https://wiki.archlinux.org/index.php/',
                             icon_url='https://tuxbot.outout.xyz/data/arch.png')
            embed.set_thumbnail(url='https://tuxbot.outout.xyz/data/arch.png')
            embed.set_footer(text="Merci à ceux qui ont pris le temps d'écrire "
                                  "cette documentation")
            await ctx.send(embed=embed)

    @_search.command(pass_context=True, name="wikipedia")
    async def search_wikipedia(self, ctx: commands.Context, args):
        """Fait une recherche sur wikipd"""

        wait = await ctx.send("_Je cherche..._")
        results = wikipedia.search(args)
        nbmr = 0
        mmssgg = ""

        for value in results:
            nbmr = nbmr + 1
            mmssgg = mmssgg + "**{}**: {} \n".format(str(nbmr), value)

        em = discord.Embed(title='Résultats de : ' + args,
                           description = mmssgg,
                           colour=0x4ECDC4)
        em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/"
                             "2/26/Paullusmagnus-logo_%28large%29.png")
        await wait.delete()

        sending = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in sending and \
                   reaction.message.id == msg.id

        async def waiter(future: asyncio.Future):
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check)
            future.set_result(reaction.emoji)

        emoji = asyncio.Future()
        self.bot.loop.create_task(waiter(emoji))

        msg = await ctx.send(embed=em)
        for e in sending:
            await msg.add_reaction(e)
            if emoji.done():
                break

        while not emoji.done():
            await asyncio.sleep(0.1)

        page = int(sending.index(emoji.result()))

        args_ = results[page]

        try:
            await msg.delete()
            await ctx.trigger_typing()
            wait = await ctx.send(ctx.message.author.mention +
                                  " ah ok sympa cette recherche, je l'effectue de suite !")
            wp = wikipedia.page(args_)
            wp_contenu = wp.summary[:200] + "..."
            em = discord.Embed(title='Wikipedia : ' + wp.title,
                               description = "{} \n_Lien_ : {} ".format(
                                   wp_contenu, wp.url),
                               colour=0x9B59B6)
            em.set_author(name="Wikipedia",
                          url='http://wikipedia.org',
                          icon_url='https://upload.wikimedia.org/wikipedia/'
                                   'commons/2/26/Paullusmagnus-logo_%28large'
                                   '%29.png')
            em.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/"
                                   "commons/2/26/Paullusmagnus-logo_%28large"
                                   "%29.png")
            em.set_footer(text="Merci à eux de nous fournir une encyclopédie "
                               "libre !")
            await wait.delete()
            await ctx.send(embed=em)

        except wikipedia.exceptions.PageError:
            # TODO : A virer dans l'event on_error
            await ctx.send(":open_mouth: Une **erreur interne** est survenue,"
                           " si cela ce reproduit contactez votre"
                           " administrateur ou faites une Issue sur"
                           " ``gitea`` !")


def setup(bot):
    bot.add_cog(Search(bot))
