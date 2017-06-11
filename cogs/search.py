from discord.ext import commands
import aiohttp
import asyncio
import discord
import urllib.request, json
import wikipedia, bs4

wikipedia.set_lang("fr")

class Search:
    """Commandes de WWW."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="search", no_pm=True, pass_context=True)
    async def _search(self, ctx):
        """Rechercher sur le world wide web"""
        if ctx.invoked_subcommand is None:
            text = open('texts/search.md').read()
            em = discord.Embed(title='Commandes de search TuxBot', description=text, colour=0x89C4F9)
            await self.bot.say(embed=em)




    @_search.command(pass_context=True, name="docubuntu")
    async def search_docubuntu(self, ctx, args):
        await self.bot.send_typing(ctx.message.channel)
        attends = await self.bot.say("_Je te cherche ça {} !_".format(ctx.message.author.mention))
        html = urllib.request.urlopen("https://doc.ubuntu-fr.org/" + args).read()
        if "avez suivi un lien" in str(html):
           await self.bot.edit_message(attends, ":sob: Nooooon ! Cette page n'existe pas, mais tu peux toujours la créer : https://doc.ubuntu-fr.org/"+ args)
        else:
           await self.bot.delete_message(attends)
           embed = discord.Embed(description="Voila j'ai trouvé ! Voici la page ramenant à votre recherche, toujours aussi bien rédigée :wink: : https://doc.ubuntu-fr.org/" + args, url='http://doc.ubuntu-fr.org/')
           embed.set_author(name="DocUbuntu-Fr", url='http://doc.ubuntu-fr.org/', icon_url='http://outout.tech/tuxbot/ubuntu.png')
           embed.set_thumbnail(url='http://outout.tech/tuxbot/ubuntu.png')
           embed.set_footer(text="Merci à ceux qui ont pris le temps d'écrire cette documentation")
           await self.bot.say(embed=embed)

    @_search.command(pass_context=True, name="aur")
    async def search_aur(self, ctx, args):
        await self.bot.send_typing(ctx.message.channel)
        attends = await self.bot.say("_Je te cherche ça {} !_".format(ctx.message.author.mention))
        erreur = 0
        try:
            html = urllib.request.urlopen("https://aur.archlinux.org/packages/" + args).read()
        except:
            erreur = 1

        if erreur == 1:
            await self.bot.delete_message(attends)
            embed = discord.Embed(description=":sob: Je n'ai pas trouvé le packet mais j'ai lancé une petite recherche, tu y trouveras peut être ton bonheur ? https://aur.archlinux.org/packages/?K=" + args,url='https://aur.archlinux.org/')
            embed.set_author(name="Aur.archlinux", url='https://aur.archlinux.org/', icon_url='http://outout.tech/tuxbot/arch.png')
            embed.set_thumbnail(url='http://outout.tech/tuxbot/arch.png')
            embed.set_footer(text="Pff même pas trouvé !")
            await self.bot.say(embed=embed)

        else:
           await self.bot.delete_message(attends)
           embed = discord.Embed(description="Et voila, j'ai trouvé la page sur le packet : https://aur.archlinux.org/packages/{0} ! \n Ca te dit un petit ``yaourt -S {0}`` ?".format(args), url='https://aur.archlinux.org/')
           embed.set_author(name="Aur.archlinux", url='https://aur.archlinux.org/', icon_url='http://outout.tech/tuxbot/arch.png')
           embed.set_thumbnail(url='http://outout.tech/tuxbot/arch.png')
           embed.set_footer(text="C'est vrai que Aur est mieux qu'APT ^^")
           await self.bot.say(embed=embed)


    @_search.command(pass_context=True, name="wikipedia")
    async def search_wikipedia(self, ctx, args):
        """Fait une recherche sur wikipd"""
        try:
            wait = await self.bot.say("_Je cherche..._")
            results = wikipedia.search(args)
            nbmr = 0
            msg = ""

            for value in results:
                nbmr = nbmr + 1
                msg = msg + "**{}**: {} \n".format(str(nbmr), value)

            em = discord.Embed(title='Résultats de : ' + args, description = msg, colour=0x4ECDC4)
            em.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/2/26/Paullusmagnus-logo_%28large%29.png")
            await self.bot.delete_message(wait)
            final = await self.bot.say(embed=em)

            list_emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

            for emoji in list_emojis:
               await self.bot.add_reaction(final, emoji)

            res = await self.bot.wait_for_reaction(message=final, user=ctx.message.author)

            for emoji in list_emojis:
                num_emoji = list_emojis.index(emoji)
                if res.reaction.emoji == emoji:
                    args_ = results[num_emoji]

            try:
                await self.bot.delete_message(final)
                await self.bot.send_typing(ctx.message.channel)
                wait = await self.bot.say(ctx.message.author.mention + " ah ok sympa cette recherche, je l'effectue de suite !")
                wp = wikipedia.page(args_)
                wp_contenu = wp.summary[:200] + "..."
                em = discord.Embed(title='Wikipedia : ' + wp.title, description = "{} \n_Lien_ : {} ".format(wp_contenu, wp.url), colour=0x9B59B6)
                em.set_author(name="Wikipedia", url='http://wikipedia.org', icon_url='https://upload.wikimedia.org/wikipedia/commons/2/26/Paullusmagnus-logo_%28large%29.png')
                em.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/2/26/Paullusmagnus-logo_%28large%29.png")
                em.set_footer(text="Merci à eux de nous fournir une encyclopédie libre !")
                await self.bot.delete_message(wait)
                await self.bot.say(embed=em)

            except wikipedia.exceptions.PageError:
                await self.bot.say(":open_mouth: Une **erreur interne** est survenue, si cela ce reproduit contactez votre administrateur ou faites une Issue sur ``github`` !")
            except UnboundLocalError:
                await self.bot.say(":interrobang: Veuillez choisir une réaction valide !")
            except DisambiguationError:
                await self.bot.say(":open_mouth: Une **erreur interne** est survenue, si cela ce reproduit contactez votre administrateur ou faites une Issue sur ``github`` !")
        except IndexError:
            await self.bot.say(" :interrobang: Veuillez entrer un terme de recherche !")

def setup(bot):
    bot.add_cog(Search(bot))
