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


# Define Modal class
class EnableModal(discord.ui.Modal, title=" Formulário📝"):
    
    admin_role = ui.TextInput(
        label='Nome da Role para Administradores', 
        placeholder='Admins', 
        style=discord.TextStyle.short
    )

    mod_role = ui.TextInput(
        label='Nome da Role para Moderadores',
        placeholder='Mods',
        style=discord.TextStyle.short
    )

    nsfw_role = ui.TextInput(
        label='Nome da Role para acesso a conteudo NSFW',
        placeholder='+18', 
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = sqlite3.connect(GUILD_DB)
        with db:
            cursor = db.cursor()
            cursor.execute()


# Define class
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to retrieve user information
    @app_commands.guild_only()
    @app_commands.command(name='user_info',
                          description="Verificar informações detalhadas de usuários. Uso: @NomeDoUsuario (opcional)")
    async def status(self, interaction: discord.Interaction, member: discord.Member = None):

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
        embed.add_field(name="Canais", value=f'{len(interaction.guild.text_channels)} Texto | {len(interaction.guild.voice_channels)} Voz')
        embed.add_field(name="Criador", value=f'{interaction.guild.owner.mention}')
        embed.add_field(name="Criado em", value=f'{interaction.guild.created_at.strftime("%a, %B %#d, %Y, %I:%M %p ")}')

        return await interaction.response.send_message(embed=embed)
    


async def setup(bot):
    await bot.add_cog(Admin(bot))
