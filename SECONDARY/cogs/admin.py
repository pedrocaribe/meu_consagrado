# Import main modules
import discord
import datetime
import sqlite3

# Import secondary modules
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction
from discord.ui import Button, View
from utils import *


# Define cog class
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(name='user_info',
                          description="Verificar informações detalhadas de usuários. Uso: @NomeDoUsuario (opcional)")
    async def status(self, interaction: discord.Interaction, member: discord.Member = None):
        """A command to retrieve detailed information about a user.

        This command can be used to retrieve detailed information about a specific user,
        including their ID, username, nickname, status, creation date, and join date in the server.
        If no member is provided, it defaults to the user who invoked the command.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            member: discord.Member [OPTIONAL]
                The member for whom to retrieve the information. Defaults to None.

        Returns:
            This function does Not return anything.
        """

        # Check if member was provided, if not default to user
        if not member:
            member = interaction.user

        # Create Embed
        embed = discord.Embed(
            title="Informações de Usuário", 
            description=f"Aqui estão as informações do usuário {member.name}", 
            color=discord.Colour.green(), 
            timestamp=interaction.created_at
        )

        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Nome", value=f"{member.name}# {member.discriminator}" if member.discriminator != '0' else f'{member.name}')
        embed.add_field(name="Apelido", value=f'{member.display_name}')
        embed.add_field(name="Status", value=f"{member.status}")
        embed.add_field(name="Criado em", value=f'{member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p ")}')
        embed.add_field(name="Entrou em", value=f'{member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p ")}')
        
        return await interaction.response.send_message(embed=embed)

    # Command to retrieve server information
    @app_commands.guild_only()
    @app_commands.command(name='server_info', description='Verificar informações detalhadas do servidor.')
    async def server_info(self, interaction: discord.Interaction):

        # Create Embed
        embed = discord.Embed(
            title="Server Info", 
            description=f"Aqui estão as informações do servidor, **{interaction.guild.name}**", 
            color=discord.Color.green(), 
            timestamp=interaction.created_at
        )
        
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Membros", value=interaction.guild.member_count)
        embed.add_field(name="Canais",
                        value=f'{len(interaction.guild.text_channels)} Texto | '
                              f'{len(interaction.guild.voice_channels)} Voz')
        embed.add_field(name="Criador", value=f'{interaction.guild.owner.mention}')
        embed.add_field(name="Criado em", value=f'{interaction.guild.created_at.strftime("%a, %B %#d, %Y, %I:%M %p ")}')

        return await interaction.response.send_message(embed=embed)
    

async def setup(bot):
    await bot.add_cog(Admin(bot))
