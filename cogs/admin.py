from discord.ext import commands
import discord
import asyncio
from .utils import checks

from .utils.checks import get_user

import traceback
import textwrap
from contextlib import redirect_stdout
import inspect
import io


class Admin(commands.Cog):
    """Commandes secrètes d'administration."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, user, *, reason=""):
        """Ban user"""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                return_msg = f"`{user.mention}` a été banni\n"
                if reason:
                    return_msg += f"raison : `{reason}`"
                return_msg += "."
                await ctx.send(return_msg)
            except discord.Forbidden:
                await ctx.send('Impossible de bannir cet user,'
                               ' probleme de permission.')
        else:
            return await ctx.send('Impossible de trouver l\'user.')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def kick(self, ctx, user, *, reason=""):
        """Kick a user"""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                return_msg = f"`{user.mention}` a été kické\n"
                if reason:
                    return_msg += f"raison : `{reason}`"
                return_msg += "."
                await ctx.send(return_msg)
            except discord.Forbidden:
                await ctx.send('Impossible de kicker cet user,'
                               ' probleme de permission.')
        else:
            return await ctx.send('Impossible de trouver l\'user.')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='clear', pass_context=True)
    async def _clear(self, ctx, number: int, silent: str = True):
        """Clear <number> of message(s)"""
        try:
            await ctx.message.delete()
        except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
        if number < 1000:
            try:
                await ctx.message.channel.purge(limit=number)
            except Exception as e:  # TODO : A virer dans l'event on_error
                if silent is not True:
                    await ctx.send(f':sob: Une erreur est survenue : \n'
                                   f' {type(e).__name__}: {e}')
            if silent is not True:
                await ctx.send("Hop voila j'ai viré des messages! Hello World")
            print(f"{str(number)} messages ont été supprimés")
        else:
            await ctx.send('Trop de messages, entre un nombre < 1000')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='say', pass_context=True)
    async def _say(self, ctx, *, tosay: str):
        """Say a message in the current channel"""
        try:
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            await ctx.send(tosay)
        except Exception as e:  # TODO : A virer dans l'event on_error
            await ctx.send(f':sob: Une erreur est survenue : \n'
                           f' {type(e).__name__}: {e}')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='sayto', pass_context=True)
    async def _sayto(self, ctx, channel_id: int, *, tosay: str):
        """Say a message in the <channel_id> channel"""
        try:
            chan = self.bot.get_channel(channel_id)
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            try:
                await chan.send(tosay)
            except Exception:
                print(f"Impossible d'envoyer le message dans {str(channel_id)}")
        except Exception as e:  # TODO : A virer dans l'event on_error
            await ctx.send(f':sob: Une erreur est survenue : \n'
                           f' {type(e).__name__}: {e}')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='sayto_dm', pass_context=True)
    async def _sayto_dm(self, ctx, user_id: int, *, tosay: str):
        """Say a message to the <user_id> user"""
        try:
            user = self.bot.get_user(user_id)
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            try:
                await user.send(tosay)
            except Exception:
                print(f"Impossible d'envoyer le message dans {str(user_id)}")
        except Exception as e:  # TODO : A virer dans l'event on_error
            await ctx.send(f':sob: Une erreur est survenue : \n'
                           f' {type(e).__name__}: {e}')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='editsay', pass_context=True)
    async def _editsay(self, ctx, id: int, *, new_content: str):
        """Edit a bot's message"""
        try:
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            toedit = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send(f"Impossible de trouver le message avec l'id "
                           f"`{id}` sur ce salon")
            return
        try:
            await toedit.edit(content=str(new_content))
        except discord.errors.Forbidden:
            await ctx.send("J'ai po les perms pour editer mes messages :(")

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='addreaction', pass_context=True)
    async def _addreaction(self, ctx, id: int, reaction: str):
        """Add reactions to a message"""
        try:
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            toadd = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send(f"Impossible de trouver le message avec l'id "
                           f"`{id}` sur ce salon")
            return
        try:
            await toadd.add_reaction(reaction)
        except discord.errors.Forbidden:
            await ctx.send("J'ai po les perms pour ajouter des réactions :(")

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='delete', pass_context=True)
    async def _delete(self, ctx, id: int):
        """Delete message in current channel"""
        try:
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            todelete = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send(f"Impossible de trouver le message avec l'id "
                           f"`{id}` sur ce salon")
            return
        try:
            await todelete.delete()
        except discord.errors.Forbidden:
            await ctx.send("J'ai po les perms pour supprimer des messages :(")

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='deletefrom', pass_context=True)
    async def _deletefrom(self, ctx, chan_id: int, *, message_id: str):
        """Delete message in <chan_id> channel"""
        try:
            chan = self.bot.get_channel(chan_id)
            try:
                await ctx.message.delete()
            except Exception:
                print(f"Impossible de supprimer le message "
                      f"\"{str(ctx.message.content)}\"")
            todelete = await chan.get_message(message_id)
        except discord.errors.NotFound:
            await ctx.send(f"Impossible de trouver le message avec l'id "
                           f"`{id}` sur le salon")
            return
        try:
            await todelete.delete()
        except discord.errors.Forbidden:
            await ctx.send("J'ai po les perms pour supprimer le message :(")

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(name='embed', pass_context=True)
    async def _embed(self, ctx, *, msg: str = "help"):
        """Send an embed"""
        if msg != "help":
            ptext = title \
                = description \
                = image \
                = thumbnail \
                = color \
                = footer \
                = author \
                = None
            timestamp = discord.Embed.Empty
            embed_values = msg.split('|')
            for i in embed_values:
                if i.strip().lower().startswith('ptext='):
                    ptext = i.strip()[6:].strip()
                elif i.strip().lower().startswith('title='):
                    title = i.strip()[6:].strip()
                elif i.strip().lower().startswith('description='):
                    description = i.strip()[12:].strip()
                elif i.strip().lower().startswith('desc='):
                    description = i.strip()[5:].strip()
                elif i.strip().lower().startswith('image='):
                    image = i.strip()[6:].strip()
                elif i.strip().lower().startswith('thumbnail='):
                    thumbnail = i.strip()[10:].strip()
                elif i.strip().lower().startswith('colour='):
                    color = i.strip()[7:].strip()
                elif i.strip().lower().startswith('color='):
                    color = i.strip()[6:].strip()
                elif i.strip().lower().startswith('footer='):
                    footer = i.strip()[7:].strip()
                elif i.strip().lower().startswith('author='):
                    author = i.strip()[7:].strip()
                elif i.strip().lower().startswith('timestamp'):
                    timestamp = ctx.message.created_at
                else:
                    if description is None and not i.strip()\
                            .lower().startswith('field='):
                        description = i.strip()

            if color:
                if color.startswith('#'):
                    color = color[1:]
                if not color.startswith('0x'):
                    color = '0x' + color

            if ptext \
                    is title \
                    is description \
                    is image \
                    is thumbnail \
                    is color \
                    is footer \
                    is author \
                    is None \
                    and 'field=' not in msg:
                try:
                    await ctx.message.delete()
                except Exception:
                    print("Impossible de supprimer le message \"" + str(
                        ctx.message.content) + "\"")
                return await ctx.send(content=None,
                                      embed=discord.Embed(description=msg))

            if color:
                em = discord.Embed(timestamp=timestamp, title=title,
                                   description=description,
                                   color=int(color, 16))
            else:
                em = discord.Embed(timestamp=timestamp, title=title,
                                   description=description)
            for i in embed_values:
                if i.strip().lower().startswith('field='):
                    field_inline = True
                    field = i.strip().lstrip('field=')
                    field_name, field_value = field.split('value=')
                    if 'inline=' in field_value:
                        field_value, field_inline = field_value.split(
                            'inline=')
                        if 'false' in field_inline.lower() \
                                or 'no' in field_inline.lower():
                            field_inline = False
                    field_name = field_name.strip().lstrip('name=')
                    em.add_field(name=field_name, value=field_value.strip(),
                                 inline=field_inline)
            if author:
                if 'icon=' in author:
                    text, icon = author.split('icon=')
                    if 'url=' in icon:
                        em.set_author(name=text.strip()[5:],
                                      icon_url=icon.split('url=')[0].strip(),
                                      url=icon.split('url=')[1].strip())
                    else:
                        em.set_author(name=text.strip()[5:], icon_url=icon)
                else:
                    if 'url=' in author:
                        em.set_author(name=author.split('url=')[0].strip()[5:],
                                      url=author.split('url=')[1].strip())
                    else:
                        em.set_author(name=author)

            if image:
                em.set_image(url=image)
            if thumbnail:
                em.set_thumbnail(url=thumbnail)
            if footer:
                if 'icon=' in footer:
                    text, icon = footer.split('icon=')
                    em.set_footer(text=text.strip()[5:], icon_url=icon)
                else:
                    em.set_footer(text=footer)

            try:
                await ctx.message.delete()
            except Exception:
                print("Impossible de supprimer le message \"" + str(
                    ctx.message.content) + "\"")
            await ctx.send(content=ptext, embed=em)

        else:
            embed = discord.Embed(
                title="Aide sur l'utilisation de la commande .embed:")
            embed.add_field(name="Titre:", value="title=<le titre>",
                            inline=True)
            embed.add_field(name="Description:",
                            value="description=<la description>", inline=True)
            embed.add_field(name="Couleur:", value="color=<couleur en hexa>",
                            inline=True)
            embed.add_field(name="Image:",
                            value="image=<url de l'image (en https)>",
                            inline=True)
            embed.add_field(name="Thumbnail:",
                            value="thumbnail=<url de l'image>", inline=True)
            embed.add_field(name="Auteur:", value="author=<nom de l'auteur>",
                            inline=True)
            embed.add_field(name="Icon", value="icon=<url de l'image>",
                            inline=True)
            embed.add_field(name="Footer", value="footer=<le footer>",
                            inline=True)
            embed.set_footer(text="Exemple: .embed title=Un titre |"
                                  " description=Une description |"
                                  " color=3AB35E |"
                                  " field=name=test value=test")

            await ctx.send(embed=embed)

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        """Launches an interactive REPL session."""
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            '_': None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel.'
                           ' Exit it with `quit`.')
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send(
            'Enter code to execute or evaluate. `exit()` or `quit` to exit.')

        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await self.bot.wait_for('message', check=check,
                                                   timeout=10.0 * 60.0)
            except asyncio.TimeoutError:
                await ctx.send('Exiting REPL session.')
                self.sessions.remove(ctx.channel.id)
                break

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.send('Content too big to be printed.')
                    else:
                        await ctx.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')

    """---------------------------------------------------------------------"""

    @checks.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Admin(bot))
