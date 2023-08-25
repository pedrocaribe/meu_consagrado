# Import main modules
import discord, random, re, os, sys

# Import secondary modules
from secrets import choice
from discord.ext import commands

# Import variables and standard functions from local file
from var_Reuse import *


# Define class
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin = admin

    '''Commands defined in this cog are for mod/Admin usage only.

    cog_modCommands v5.02'''

    # Add specified role to mentioned user
    @commands.command(name = 'addrole', help = 'Comando habilitado para MODs e Admins!\n\nUso: %addrole @usuario role.\n\nComando habilitado para MODs e Admins!')
    @commands.has_any_role('Admins' or 'Mods')
    async def addrole(self, ctx, member: discord.Member, *args):

        e = discord.Embed(description = ':no_entry_sign: ***__Você deve especificar todos os parâmetros pra usar o comando.__*** :no_entry_sign:\nO nome da role tem que ser exato.', colour = discord.Color.red())
        e.set_footer(text = '(%addrole @usuario role). ')

        # If not enough parameters specified by user, return standard response
        if not args:
            return await ctx.reply(embed = e)
        else:
            req_role = args[0]
            guild = self.bot.get_guild(ctx.guild.id)
            role = discord.utils.get(guild.roles, name = f'{req_role}')

            # If role does not exist, return standard response to user
            if role == None:
                return await ctx.reply(embed = e)

            await discord.Member.add_roles(member, role)
            c = discord.Embed(description = f':white_check_mark: A role **__{role}__** foi assinalada ao usuário **__{member}__** com sucesso!', colour = discord.Color.green())
            return await ctx.reply(embed = c)


    # Delete specified role from mentioned user
    @commands.command(name = 'delrole', help = 'Comando habilitado para MODs e Admins!\n\nUso: %delrole @usuario role.\n\nComando habilitado para MODs e Admins!')
    @commands.has_any_role('Admins' or 'Mods')
    async def delrole(self, ctx, member: discord.Member, *args):

        e = discord.Embed(description = ':no_entry_sign: ***__Você deve especificar todos os parâmetros pra usar o comando.__*** :no_entry_sign:\nO nome da role tem que ser exato.', colour = discord.Color.red())
        e.set_footer(text = '(%delrole @usuario role). ')

        # If not enought parameters specified by user, return standard response
        if not args:
            return await ctx.reply(embed = e)
        else:
            req_role = args[0]
            guild = self.bot.get_guild(ctx.guild.id)
            role = discord.utils.get(guild.roles, name = f'{req_role}')

            # If role does not exist, return standard response to user
            if role == None:
                return await ctx.reply(embed = e)

            await discord.Member.remove_roles(member, role)
            c = discord.Embed(description = f':white_check_mark: A role ***__{role}__*** foi removida do usuário **__{member}__** com sucesso!', colour = discord.Color.green())
            return await ctx.reply(embed = c)

    # Delete specified number of messages from current channel
    @commands.command(name='clear', help='Comando habilitado apenas para Admins!\n\nUso: %clear numDeMsgs (entre 1 e 100)\n\nO comando deve ser executado dentro do canal que deseja limpar\n\nComando habilitado apenas para Admins!')
    @commands.has_any_role('Admins')
    async def clear(self, ctx, amt: int):

        await ctx.channel.purge(limit=amt)


    # Ban mentioned user
    @commands.command(name = 'ban', help = 'Comando habilitado apenas para Admins!\n\nUso: %ban @usuario confirm\n\nComando habilitado apenas para Admins!')
    @commands.has_any_role('Admins')
    async def ban(self, ctx, member: discord.Member, *args):

        # If 'confirm' argument was not provided, return standard response to user
        if not args or args[0] != 'confirm':
            return await ctx.send('Você deve confirmar essa ação. **(Uso: %ban @usuario confirm)**')


        embed = discord.Embed(description = f':no_entry_sign: ***{member} foi banido.*** :white_check_mark: ', colour = discord.Color.red())
        await member.ban()
        return await ctx.send(embed = embed)

    # Unban mentioned user
    @commands.command(name = 'unban', help = 'Comando habilitado apenas para Admins!\n\nUso: %unban @usuario (Nome do Usuario#1234)\n\nComando habilitando apenas para Admins')
    @commands.has_any_role('Admins')
    async def unban(self, ctx, *, member):

        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        async for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                embed = discord.Embed(description = f':white_check_mark: ***{user.name}#{user.discriminator} foi desbanido.*** :white_check_mark: ', colour = discord.Color.green())
                return await ctx.send(embed = embed)


    # Kick mentioned user for specified reason
    @commands.command(name = 'kick', help = 'Comando habilitado para MODs e Admins!\n\nUso: %kick @usuario Seu Motivo Aqui.\n\nComando habilitado para MODs e Admins!')
    @commands.has_any_role('Mods', 'Admins')
    async def kick(self, ctx, member : discord.Member, *, reason = None):

        # If no reason, open DM with Mod/Admin, give details and delete wrong message
        if reason == None:
            await ctx.message.author.create_dm()
            await ctx.message.author.dm_channel.send(f':no_entry: Você precisa dar um motivo para o kick. Lembrando que tudo estará guardado no histórico de ações (audit logs). ***(Uso: %kick @usuario Seu Motivo Aqui.)***')
            await ctx.message.delete()
            return

        embed = discord.Embed(description = f':warning: ***{member} foi kickado.*** :white_check_mark: ', colour = discord.Color.green())
        await member.kick(reason = reason)
        await ctx.send(embed = embed)


    # Provide list of users banned from channel
    @commands.command(name = 'banlist', help = f'Comando habilitado para MODs e Admins!\n\nUso: %banlist\n\nComando habilitado para MODs e Admins!')
    async def banlist(self, ctx) -> None:

        # Limit list to 10 entries
        bans = [entry async for entry in ctx.guild.bans(limit=10)]
        _list = []

        for BanEntry in bans:
            _list.append({'name':BanEntry.user.name, 'reason':BanEntry.reason})
        e = discord.Embed(title = 'Usuários Banidos', description = "**Usuário /// Motivo**\n\n", colour = discord.Color.red())
        for i in _list:
            e.description += f"- {i['name']} /// {i['reason']}\n"

        if len(_list) < 1: e.description += 'Sem usuários banidos no momento.'

        await ctx.reply(embed = e)

# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(Admin(bot))