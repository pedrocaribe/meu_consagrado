# Import main modules
import os, discord

# Import secondary modules
from imp import reload
from discord.ext import commands

# Import variables and standard functions from local file
from var_Reuse import *

# Define class
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''Commands defined in this cog are for owner usage only

    cog_ownerCommands v1.06'''

    # Hidden command to reload cog
    @commands.command(hidden = True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, module: str):

        # Try to reload extension
        try:
            await self.bot.reload_extension(module)

        # If error, return to user
        except Exception as e:
            embed = discord.Embed(description = f':no_entry:      *** Erro ao recarregar extensão:***  `{module}`', colour = discord.Color.red())
            await ctx.send(embed = embed)

        # If no error, return success to user
        else:
            embed = discord.Embed(description = f':ok:    ***Extensão `{module}` foi recarregada com sucesso!.*** :white_check_mark: ', colour = discord.Color.green())
            await ctx.send(embed = embed)


    # Hidden command to broadcast start of maintenance window
    @commands.command(hidden = True)
    @commands.is_owner()
    async def maintenancestart(self, ctx, est: int, *, reason: str):
        guild = self.bot.get_guild(ctx.guild.id)
        allowed_mentions = discord.AllowedMentions(everyone = True)

        channel = discord.utils.get(guild.text_channels, name="anúncios")

        e = discord.Embed(title = ':warning: Anúncio de Manutenção Programada - INÍCIO', description = f'@everyone\nO servidor será desligado por aproximadamente **{est}** minutos para que sejam aplicadas melhorias ao sistema do BOT.\n\n**Motivo**: "__{reason}__"\n\n\nAgradeço a compreensão e paciência de todos.')
        e.set_footer(text = 'Pedro Caribé - Criador')
        e.set_thumbnail(url = 'https://rioantigomoveis.files.wordpress.com/2016/06/maintenance-icon.png')

        await channel.send(embed = e, allowed_mentions = allowed_mentions)


    # Hidden command to broadcast end of maintenance window
    @commands.command(hidden = True)
    @commands.is_owner()
    async def maintenanceend(self, ctx):
        guild = self.bot.get_guild(ctx.guild.id)
        allowed_mentions = discord.AllowedMentions(everyone = True)

        channel = discord.utils.get(guild.text_channels, name="anúncios")

        e = discord.Embed(title = ':white_check_mark: Anúncio de Manutenção Programada - TÉRMINO', description = f'@everyone\nO servidor está novamente no ar.\n\nAgradeço a compreensão e paciência de todos.')
        e.set_footer(text = 'Pedro Caribé - Criador')
        e.set_thumbnail(url = 'https://rioantigomoveis.files.wordpress.com/2016/06/maintenance-icon.png')

        await channel.send(embed = e, allowed_mentions = allowed_mentions)


# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(Owner(bot))