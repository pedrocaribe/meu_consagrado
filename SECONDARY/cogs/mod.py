# Import main modules
import discord

# Import secondary modules
from discord import app_commands
from discord.ext import commands

# Import variables and standard functions from local file
from utils import icon


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", help='Comando habilitado apenas para Admins!\n\n'
                                         'Uso: !clear numDeMsgs (entre 1 e 100)\n\n'
                                         'O comando deve ser executado dentro do canal que deseja limpar\n\n'
                                         'Comando habilitado apenas para Admins!')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amt: int):
        """A command to delete a specified number of messages from the current channel.

        This command allows administrators and moderators with power to manage messages to delete a
        specified number of messages from the current channel. The number of messages to delete must
        be between 1 and 100.

        Args:
            ctx: commands.Context
                The context object representing the command invocation.
            amt: int
                The number of messages to delete.

        Returns:
            This function does Not return anything.
        """

        if not 1 <= amt <= 100:
            e = discord.Embed(
                title="",
                description="A quantidade deve ser entre **1 e 100**",
                colour=discord.Color.red()
            )
            return await ctx.send(embed=e, ephemeral=True)

        await ctx.channel.purge(limit=amt + 1)  # + 1 due to the message sent requesting the purge

        # Add reaction
        await ctx.message.add_reaction("✅")

        embed = discord.Embed(
            title=f'Mensagens apagadas',
            description=f'**{amt}** Mensagens apagadas com **SUCESSO**'
            )
        embed.add_field(name='Solicitado por ', value=ctx.author.name)
        embed.set_footer(text='essa mensagem se auto-apagará em 5 segundos')

        msg = await ctx.send(embed=embed)

        await msg.delete(delay=5)

    @commands.command(name="ban", help="Comando habilitado apenas para Admins! Uso: !ban @usuario motivo")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        """A command to ban a user from the server.

        This command allows administrators to ban a user from the server. It sends a message to
        the banned user with the reason for the ban and then performs the ban.

        Args:
            ctx: commands.Context
                The context object representing the command invocation.
            user: discord.Member
                The user to ban.
            reason: str
                The reason for the ban.

        Returns:
            This function does Not return anything.
        """

        e_user = discord.Embed(
            title="Você foi banido!",
            description=f"Você foi banido do servidor **{ctx.guild.name}**",
            colour=discord.Colour.red())
        e_user.add_field(name="Motivo", value=f"{reason}")

        thumbnail, e_user = await icon(name="ban", embed=e_user)

        await user.send(file=thumbnail, embed=e_user)

        await user.ban(reason=reason)

        e_ret = discord.Embed(
            title="Usuário banido!",
            description=f"O usuário **{user.name}** foi banido do servidor",
            colour=discord.Colour.yellow()
        )
        thumbnail, e_ret = await icon(name="ban", embed=e_ret)
        await ctx.reply(file=thumbnail, embed=e_ret)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(name="unban", help="Comando habilitado apenas para Admins! Uso: !unban usuario#id")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, *, member: str):
        """A command to unban a previously banned user from the server.

        This command allows administrators to unban a user from the server. It takes the username
        and discriminator or just the username to fit new Discord username pattern and looks for
        the banned user to unban.

        Args:
            ctx: commands.Context
                The context object representing the command invocation.
            member: str
                The username and discriminator (in the format "username#discriminator") of the
                    banned user.

        Returns:
            This function does Not return anything.
        """

        banned_users = ctx.guild.bans()
        member_name = member_discriminator = str()

        if "#" in member:
            member_name, member_discriminator = member.split("#")
        else:
            member_name = member

        async for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                e = discord.Embed(
                    description=f":white_check_mark: ***{user.name}#{user.discriminator} "
                                f"foi desbanido.*** :white_check_mark:",
                    colour=discord.Color.green()
                )
                await ctx.send(embed=e)

                # Add reaction
                return await ctx.message.add_reaction("✅")

        e_ret = discord.Embed(
            description="**Usuário não encontrado!**",
            colour=discord.Color.orange()
        )
        return await ctx.send(embed=e_ret)

    @commands.command(name="banlist", help="Comando habilitado apenas para Admins! Uso: !banlist usuario#id (opcional)")
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx: commands.Context, *, member: str = None):
        """A command to list banned users on the server or retrieve information about a specific banned user.

            This command allows moderators and administrators to list banned users on the server.
            If a specific member is mentioned, it provides information about the ban for that member.

            Args:
                ctx: commands.Context
                    The context object representing the command invocation.
                member: str [OPTIONAL]
                    The username and discriminator (in the format "username#discriminator") of the banned
                        user to retrieve information about.

            Returns:
                This function does Not return anything.
            """

        bans = [entry async for entry in ctx.guild.bans(limit=15)]

        if not bans:
            return await ctx.reply("Sem usuários banidos no momento.")

        entries = [{
            "name": ban_entry.user.name,
            "reason": ban_entry.reason,
            "discriminator": ban_entry.user.discriminator} for ban_entry in bans]

        e = discord.Embed(
            title="Usuários Banidos",
            description="**Usuário /// Motivo**",
            colour=discord.Color.red())

        if member:
            for entry in entries:
                if member == f"{entry['name']}#{entry['discriminator']}":
                    e.add_field(name="", value=f"{member} /// {entry['reason']}")
                    return await ctx.reply(embed=e)

        else:
            for entry in entries:
                e.add_field(name="", value=f"{entry['name']}#{entry['discriminator']} /// {entry['reason']}")
                await ctx.reply(embed=e)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(name="kick", help="Comando habilitado para MODs e Admins! Uso: !kick @membro")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, members: commands.Greedy[discord.Member]):
        """A command to kick one or more members from the server.

            This command allows moderators and administrators to kick one or more members from the server.
            It accepts one or more mentions of the members to be kicked.

            Args:
                ctx: commands.Context
                    The context object representing the command invocation.
                members: List[discord.Member]
                    A list of member objects to be kicked from the server.

            Returns:
                This function does Not return anything.
            """

        e = discord.Embed(
            title="Usuários Kickados!",
            description="Os seguintes usuários foram kickados:",
            colour=discord.Color.teal()
        )
        for member in members:
            e.add_field(name="", value=member.name, inline=False)
            await member.kick()

        await ctx.reply(embed=e)

        # Add reaction
        return await ctx.message.add_reaction("✅")


async def setup(bot):
    await bot.add_cog(Mod(bot))
