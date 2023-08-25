# Import base modules
import discord, os, time

# Import secondary modules
from discord.ext import commands
from discord import app_commands
from colorama import Fore, Back, Style
from datetime import datetime
# from utils import reload

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

    @commands.command(hidden=True, name='reload_cog', brief='Somente para uso do Owner',help='Recarregar cog. Uso: !reload_cog COGNAME')
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
    

    @commands.command(hidden=True, name='sync', brief='Sync all slash commands')
    @commands.is_owner()
    async def syncall(self, ctx):

        try:
            synced = await self.bot.tree.sync()
        except Exception as e:

            embed = discord.Embed(
                description=f':no_entry:     *** Erro ao sincronizar Slash Commands.***',
                colour=discord.Color.red()
            )
            embed.add_field(
                name='DESCRIÇÃO DO ERRO:',
                value=f'{e}'
            )

            await ctx.send(embed=embed)

        else:

            prefix = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
            sr = Style.RESET_ALL
            fy = Fore.YELLOW

            print(f'{prefix} Slash CMDs Synced {fy}{str(len(synced))} Commands{sr}')
            embed = discord.Embed(
                description=f':ok:     *** Slash Commands sincronizados ***',
                colour=discord.Color.green()
            )

            await ctx.send(embed=embed)

        # Add reaction
        return await ctx.message.add_reaction("✅")
    

async def setup(bot):
    await bot.add_cog(Owner(bot))
