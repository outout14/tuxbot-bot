from discord.ext import commands
import discord


class Role(commands.Cog):
    """Commandes role."""

    def __init__(self, bot):
        self.bot = bot

        self.ARCH_ROLE = 393077257826205706
        self.DEBIAN_ROLE = 393077933209550859
        self.RHEL_ROLE = 393078333245751296
        self.ANDROID_ROLE = 393087862972612627
        self.BSD_ROLE = 401791543708745738

    @commands.group(name="role", no_pm=True, pass_context=True,
                    case_insensitive=True)
    async def _role(self, ctx):
        """Affiche l'aide sur la commande role"""
        if ctx.message.guild.id != 280805240977227776:
            return

        if ctx.invoked_subcommand is None:
            text = open('texts/roles.md').read()
            em = discord.Embed(title='Gestionnaires de rôles',
                               description=text, colour=0x89C4F9)
            await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @_role.command(name="arch", aliases=["archlinux", "arch_linux"],
                   pass_context=True)
    async def role_arch(self, ctx):
        """Ajoute/retire le role 'Arch user'"""
        roles = ctx.message.author.roles
        role_id = []
        for role in roles:
            role_id.append(role.id)

        user = ctx.message.author
        if self.ARCH_ROLE in role_id:
            await user.remove_roles(discord.Object(id=self.ARCH_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Pourquoi tu viens "
                           f"de supprimer Arch Linux, c'était trop compliqué "
                           f"pour toi ? <:sad:343723037331292170>")
        else:
            await user.add_roles(discord.Object(id=self.ARCH_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > How un "
                           f"ArchLinuxien, c'est bon les ``yaourt`` ? "
                           f"<:hap:354275645574086656>")

    """---------------------------------------------------------------------"""

    @_role.command(name="debian", pass_context=True)
    async def role_debian(self, ctx):
        """Ajoute/retire le role 'debian user'"""
        roles = ctx.message.author.roles
        role_id = []
        for role in roles:
            role_id.append(role.id)

        user = ctx.message.author
        if self.DEBIAN_ROLE in role_id:
            await user.remove_roles(discord.Object(id=self.DEBIAN_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Adieu ! Tu verras, "
                           f"APT te manquera ! ")
        else:
            await user.add_roles(discord.Object(id=self.DEBIAN_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Un utilisateur de "
                           f"Debian, encore et encore ! "
                           f"<:stuck_out_tongue:343723077412323339>")

    """---------------------------------------------------------------------"""

    @_role.command(name="rhel", pass_context=True)
    async def role_rhel(self, ctx):
        """Ajoute/retire le role 'rhel user'"""
        roles = ctx.message.author.roles
        role_id = []
        for role in roles:
            role_id.append(role.id)

        user = ctx.message.author
        if self.RHEL_ROLE in role_id:
            await user.remove_roles(discord.Object(id=self.RHEL_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Pourquoi tu t'en "
                           f"vas, il sont déjà assez seul là-bas "
                           f"<:sad:343723037331292170>")
        else:
            await user.add_roles(discord.Object(id=self.RHEL_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Mais, voila "
                           f"quelqu'un qui porte des chapeaux ! "
                           f"<:hap:354275645574086656>")

    """---------------------------------------------------------------------"""

    @_role.command(name="android", pass_context=True)
    async def role_android(self, ctx):
        """Ajoute/retire le role 'android user'"""
        roles = ctx.message.author.roles
        role_id = []
        for role in roles:
            role_id.append(role.id)

        user = ctx.message.author
        if self.ANDROID_ROLE in role_id:
            await user.remove_roles(discord.Object(id=self.ANDROID_ROLE))
            await ctx.send(f"{ctx.message.author.mention} >How, me dit pas "
                           f"que tu as compris que les Android's allaient "
                           f"exterminer le monde ? "
                           f"<:trollface:375327667160875008>")
        else:
            await user.add_roles(discord.Object(id=self.ANDROID_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Hey, un utilisateur"
                           f" d'Android, prêt à continuer l'extermination de "
                           f"WP et iOS ? "
                           f"<:stuck_out_tongue:343723077412323339>")

    """---------------------------------------------------------------------"""

    @_role.command(name="bsd", pass_context=True)
    async def role_bsd(self, ctx):
        """Ajoute/retire le role 'BSD user'"""
        roles = ctx.message.author.roles
        role_id = []
        for role in roles:
            role_id.append(role.id)

        user = ctx.message.author
        if self.BSD_ROLE in role_id:
            await user.remove_roles(discord.Object(id=self.BSD_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Ohhhh fait gaffe "
                           f"ou le démon va te piquer")
        else:
            await user.add_roles(discord.Object(id=self.BSD_ROLE))
            await ctx.send(f"{ctx.message.author.mention} > Quelqu'un sous "
                           f"BSD ! Au moins il a pas besoin de mettre GNU "
                           f"devant son OS à chaque fois :d")

    """---------------------------------------------------------------------"""

    @_role.command(name="staff", pass_context=True, hidden=True)
    async def role_staff(self, ctx):
        """Easter egg"""

        await ctx.send(f"{ctx.message.author.mention} > Vous n'avez pas "
                       f"le rôle staff, tu crois quoi :joy:")


def setup(bot):
    bot.add_cog(Role(bot))
