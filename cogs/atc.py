import asyncio

from bs4 import BeautifulSoup
import requests
import re

import discord
from discord.ext import commands


class ATC(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.author = None
        self.voice = None

    @staticmethod
    async def extra(self, ctx, icao):
        if icao == "stop_playing":
            if self.playing and (
                ctx.author.id == self.author.id
                or ctx.message.channel.permissions_for(ctx.message.author).administrator is True
            ):
                await self.voice.disconnect()
                self.playing = False
                await ctx.send("Écoute terminée !")
                return "quit"
            else:
                await ctx.send("Veuillez specifier un icao")
                return "quit"
        if icao == "info":
            em = discord.Embed(title=f"Infos sur les services utilisés par {self.bot.config.prefix[0]}atc")
            em.add_field(name="Service pour les communications:",
                         value="[liveatc.net](https://www.liveatc.net/)",
                         inline=False)
            em.add_field(name="Service pour les plans des aéroports:",
                         value="[universalweather.com](http://www.universalweather.com/)",
                         inline=False)
            await ctx.send(embed=em)
            return "quit"

    """---------------------------------------------------------------------"""

    @commands.command(name="atc", no_pm=True, pass_context=True)
    async def _atc(self, ctx, icao="stop_playing"):
        user = ctx.author
        if not user.voice:
            await ctx.send('Veuillez aller dans un channel vocal.')
            return

        if await self.extra(self, ctx, icao) == "quit":
            return

        if self.playing:
            await ctx.send(f"Une écoute est déja en court, "
                           f"demandez à {self.author.mention} de faire "
                           f"`.atc stop_playing` pour l'arreter")
            return
        self.author = user
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.35 Safari/537.36',
        }
        req = requests.post("https://www.liveatc.net/search/",
                            data={'icao': icao},
                            headers=headers)
        html = BeautifulSoup(req.text, features="lxml")
        regex = r"(javascript: pageTracker\._trackPageview\('\/listen\/)(.*)(\'\)\;)"

        possibilities = {}
        emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟',
                  '0⃣', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']
        to_react = []

        idx = 0
        for a in html.findAll("a", onclick=True):
            val = a.get('onclick')
            for match in re.finditer(regex, val):
                possibilities[idx] = f"{emojis[idx]} - {match.groups()[1]}\n"
                to_react.append(emojis[idx])
                idx += 1

        em = discord.Embed(title='Résultats pour : ' + icao,
                           description=str(''.join(possibilities.values())),
                           colour=0x4ECDC4)
        em.set_image(
            url=f"http://www.universalweather.com/regusers/mod-bin/uvtp_airport_image?icao={icao}")

        poll_msg = await ctx.send(embed=em)
        for emote in to_react:
            await poll_msg.add_reaction(emote)

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in to_react and \
                   reaction.message.id == poll_msg.id

        async def waiter(future: asyncio.Future):
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     check=check)

            future.set_result(emojis.index(reaction.emoji))

        added_emoji = asyncio.Future()
        self.bot.loop.create_task(waiter(added_emoji))

        while not added_emoji.done():
            await asyncio.sleep(0.1)

        freq = possibilities[added_emoji.result()].split('- ')[1]

        if possibilities:
            self.playing = True
            self.voice = await user.voice.channel.connect()
            self.voice.play(
                discord.FFmpegPCMAudio(f"http://yyz.liveatc.net/{freq}"))
            await poll_msg.delete()
            await ctx.send(f"Écoute de {freq}")
        else:
            await ctx.send(f"Aucun résultat trouvé pour {icao} {freq}")


def setup(bot):
    bot.add_cog(ATC(bot))
