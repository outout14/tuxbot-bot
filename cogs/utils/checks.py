# -*- coding: utf-8 -*-
import discord.utils
from discord.ext import commands


def is_owner_check(message):           #    OUTOUT id                RICK id               L4P1N id             GIGA id              FLAYOR id              ROMAIN id
    owner = str(message.author.id) in ['171685542553976832', '163697401935298560', '88644904112128000', '92619860521005056', '273757386127441920', '269156684155453451'] ###ID's modo & admin
    rights = str(message.author.top_role.name).upper() in ['ADMIN', 'ADMINISTRATEURS', 'ADMINISTRATEUR', 'MODO', 'MODÉRATEUR', 'MODÉRATEURS', 'MODERATEUR', 'MODERATEURS']
    if rights == True or owner == True:
        return True  # Owner of the bot
    else: 
        return False

def is_owner(warn=True):
    def check(ctx, warn):
        owner = is_owner_check(ctx.message)
        if not owner and warn:
                print(ctx.message.author.name + " à essayer d'executer " + ctx.message.content)
        return owner

    owner = commands.check(lambda ctx: check(ctx, warn))
    return owner

def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Bot Admin', **perms)

    return commands.check(predicate)


def is_in_servers(*server_ids):
    def predicate(ctx):
        server = ctx.message.server
        if server is None:
            return False
        return server.id in server_ids

    return commands.check(predicate)

def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True

    return check

def is_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})
    return commands.check(pred)