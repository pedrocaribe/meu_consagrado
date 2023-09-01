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

    @commands.command(name="ban", help="Comando habilitado apenas para Admins!\n\n"
                                       "Uso: !ban @usuario motivo")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: str):
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


async def setup(bot):
    await bot.add_cog(Mod(bot))