# Import base modules
import discord, os, time

# Import secondary modules
from discord.ext import commands
from discord import app_commands
from colorama import Fore, Back, Style
from datetime import datetime
# from utils import reload
from typing import Literal, Optional


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name='load_cog', brief='Somente para uso do Owner', help='Carregar cog. Uso: !load_cog COGNAME')
    @commands.is_owner()
    async def load_cog(self, ctx, module: str):

        # Try to load extension
        try:
            await self.bot.load_extension(f'cogs.{module}')

        # If error, return to user
        except Exception as e:

            embed = discord.Embed(
                description=f':no_entry:      *** Erro ao carregar extensão:***  `{module}`', 
                colour=discord.Color.red()
            )

            await ctx.send(embed=embed)

            print(f'{Fore.BLACK + Back.RED}ERROR -> {e}')

        # If no error, return success to user
        else:

            embed = discord.Embed(
                description=f':ok:    ***Extensão `{module}` foi carregada com sucesso!.*** :white_check_mark: ',
                colour=discord.Color.green()
            )

            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(hidden=True, name='unload_cog', brief='Somente para uso do Owner', help='Descarregar cog. Uso: !unload_cog COGNAME')
    @commands.is_owner()
    async def unload_cog(self, ctx, module: str):

        # Try to load extension
        try:
            await self.bot.unload_extension(f'cogs.{module}')

        # If error, return to user
        except Exception as e:

            embed = discord.Embed(
                description=f':no_entry:      *** Erro ao descarregar extensão:***  `{module}`', 
                colour=discord.Color.red()
                )
            
            await ctx.send(embed=embed)
            print(e)
        # If no error, return success to user
        else:

            embed = discord.Embed(
                description=f':ok:    ***Extensão `{module}` foi descarregada com sucesso!.*** :white_check_mark: ',
                colour=discord.Color.green()
                )
            
            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(hidden=True, name='reload_cog', brief='Somente para uso do Owner', help='Recarregar cog. Uso: !reload_cog COGNAME')
    @commands.is_owner()
    async def reload_cog(self, ctx, module: str):

        # Try to load cog
        try:
            await self.bot.reload_extension(f'cogs.{module}')

        # If error, return to user
        except Exception as e:

            embed = discord.Embed(
                description=f':no_entry:      *** Erro ao recarregar extensão:***  `{module}`', 
                colour=discord.Color.red()
                )
            embed.add_field(
                name='DESCRIÇÃO DO ERRO',
                value=e
            )
            
            await ctx.send(embed=embed)
            print(e)
        # If no error, return success to user
        else:

            embed = discord.Embed(
                description=f':ok:    ***Extensão `{module}` foi recarregada com sucesso!.*** :white_check_mark: ',
                colour=discord.Color.green()
                )
            
            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(hidden=True, name='reloadall', brief='Recarrega todos os cogs')
    @commands.is_owner()
    async def reloadall(self, ctx):

        # Try to reload all cogs
        try:
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py") and filename != "__init.py__":
                    await self.bot.reload_extension(f'cogs.{filename[:-3]}')
        
        # If error, trigger exception and let user know
        except Exception as e:
            
            embed = discord.Embed(
                description=f':no_entry:      *** Erro ao recarregar extensões:***', 
                colour=discord.Color.red()
                )

            await ctx.send(embed=embed)

        # If no errors, return success to user
        else:

            embed = discord.Embed(
                description=f':ok:      *** Extensões Recarregadas***', 
                colour=discord.Color.green()
                )
            
            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")

    @commands.command(
        hidden=True,
        name='sync',
        brief='Sync all slash commands',
        help="No args for sending global commands to discord, ~ to sync all commands to current guild, "
             "* to copy all global to current guild and ^ to remove all commands from CommandTree")
    @commands.is_owner()
    async def syncall(self, ctx, guilds: commands.Greedy[discord.Object], spec: Optional[Literal['~', '*', '^']] = None):
        """ !sync
                This takes all global commands within the CommandTree and sends them to Discord.
            !sync ~
                This will sync all guild commands for the current context’s guild.
            !sync *
                This command copies all global commands to the current guild (within the CommandTree) and syncs.
            !sync ^
                This command will remove all guild commands from the CommandTree and syncs, which
                effectively removes all commands from the guild.
            !sync 123 456 789
                This command will sync the 3 guild ids we passed: 123, 456 and 789.
                Only their guilds and guild-bound commands.

        Parameters:
            ctx: Can be replaced by your own context subclass if needed.
            guilds: Guild number to be parsed as discord.Object
            spec: [OPTIONAL] argument to define what the command will do

        Returns:
            This command returns an embed
        """

        if not guilds:
            if spec == '~':
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == '*':
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == '^':
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            embed = discord.Embed(
                description=f" **{len(synced)}** Comandos sincronizados {'global' if spec is None else 'na guilda atual'}",
                colour=discord.Color.green()
            )

            await ctx.send(embed=embed)
        else:
            ret = 0
            for guild in guilds:
                try:
                    await self.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            embed = discord.Embed(
                description=f"Command Tree sincronizada para {ret}/{len(guilds)}.",
                colour=discord.Color.green()
            )

            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")
    

async def setup(bot):
    await bot.add_cog(Owner(bot))
