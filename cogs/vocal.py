import asyncio
import os
import re
import subprocess
import uuid

import discord
from discord.ext import commands
from gtts import gTTS


class Vocal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.author = None
        self.voice = None

    """---------------------------------------------------------------------"""

    @staticmethod
    def get_duration(file):
        popen = subprocess.Popen(("ffprobe",
                                  "-show_entries",
                                  "format=duration",
                                  "-i", file),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        output, err = popen.communicate()
        match = re.search(r"[-+]?\d*\.\d+|\d+", str(output))
        return float(match.group())

    @commands.command(name="voc", no_pm=True, pass_context=True)
    async def _voc(self, ctx, *, message=""):
        if message == "":
            await ctx.send("Veuillez écrire un message...")
            return
        if message == "stop_playing" \
                and (
                    ctx.author.id == self.author.id
                    or ctx.message.channel.permissions_for(
                            ctx.message.author
                        ).administrator is True
                ) \
                and self.playing is True:

            await ctx.send('stop')
            await self.voice.disconnect()
            self.playing = False
            return

        if self.playing is True:
            await ctx.send("Je suis déja en train de parler,"
                           " merci de réenvoyer ton message"
                           " quand j'aurais fini.")
            return

        user = ctx.author
        self.author = user

        if user.voice:
            self.playing = True
            filename = f"data/tmp/voc/{uuid.uuid1()}.mp3"
            lang = [x for x in message.split(" ") if x.startswith("lang=")]

            loading = await ctx.send("*Chargement du message en cours...*")

            if lang:
                choice_lang = (lang[0])[5:]
                message = f"{user.display_name} à dit: {message.strip(lang[0])}" if len(ctx.author.voice.channel.members) >= 4 else message.strip(lang[0])

                try:
                    tts = gTTS(
                        text=message,
                        lang=str(choice_lang))
                except ValueError:
                    tts = gTTS(
                        text=message,
                        lang="fr")
                    await ctx.send("La langue n'est pas supportée,"
                                   " le francais a donc été choisi")
            else:
                message = f"{user.display_name} à dit: {message}" if len(ctx.author.voice.channel.members) >= 4 else message
                tts = gTTS(text=message,
                           lang="fr")

            tts.save(filename)

            self.voice = await user.voice.channel.connect()
            self.voice.play(discord.FFmpegPCMAudio(filename))
            counter = 0
            duration = self.get_duration(filename)
            while not counter >= duration:
                if self.playing:
                    await loading.edit(
                        content=f"Lecture du message de {self.author.display_name} en cours : {counter}sec/{duration}sec")
                    await asyncio.sleep(1)
                    counter += 1
                else:
                    break
            await self.voice.disconnect()

            await loading.edit(content="Lecture terminée")
            self.voice = None
            os.remove(filename)
            self.playing = False
        else:
            await ctx.send('Veuillez aller dans un channel vocal.')


def setup(bot):
    bot.add_cog(Vocal(bot))
