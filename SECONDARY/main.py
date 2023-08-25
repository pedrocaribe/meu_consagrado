# Import base modules
import platform
import time
import discord
import asyncio
import os
import random
import sqlite3

# Import error logging modules
import logging

# Import secondary modules
from discord.ext import commands, tasks
from colorama import Back, Fore, Style
from datetime import datetime

# Import local utilities and variables
from settings import *
from global_variables import *
from utils import *

# Declarations
intent = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intent)
    
# Set up logging for DEBUG
# discord.utils.setup_logging(level=logging.DEBUG, root=False)
'''
FAZER FEEDBACK MODAL
'''
# Set up DBs

guild_db = db_connect(GUILD_DB)
msg_db = db_connect(MSG_DB)

    
# Definition of main function, load all cogs and start bot
async def main():
    async with bot:
        await load_cogs(bot)
        await bot.start(DISCORD_TOKEN)


# Print load message once ready
@bot.event
async def on_ready():

    # Create Date/Time prefix for console
    prefix = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    fy = Fore.YELLOW
    fw = Fore.WHITE
    fg = Fore.GREEN
    fr = Fore.RED
    bg = Back.GREEN
    br = Back.RED
    sr = Style.RESET_ALL

    # Print useful information to console
    print(f'{prefix} Discord Version -> {fy}{discord.__version__}')
    print(f'{prefix} Python Version -> {fy}{str(platform.python_version())}')
    print(f'{prefix} All cogs loaded successfully')
    print(f'{prefix} We have successfully logged in as -> {fy}{bot.user} {fw}in a total of {fg}{len(bot.guilds)} guilds')
    print(f'{prefix} Bot ID -> {fy}{bot.user.id}')

    error_code = 0

    # DB connections
    if guild_db:
        print(f'{prefix} {fg}Successfully {fw}Connected to DB {fy}{GUILD_DB}')
    else:
        print(f'{prefix} {fr}ERROR {fw}Connecting to DB {fy}{GUILD_DB}')
        error_code = 1
    if msg_db:
        print(f'{prefix} {fg}Successfully {fw}Connected to DB {fy}{MSG_DB}')
    else:
        print(f'{prefix} {fr}ERROR {fw}Connecting to DB {fy}{MSG_DB}')
        error_code = 2

    # Sync slash command tree
    synced = await bot.tree.sync()

    # Print sync success message
    print(f'{prefix} Slash CMDs Synced {fy}{str(len(synced))} Commands{sr}')
    print(f'{prefix} {fw}{bg}Code {error_code}{Style.RESET_ALL}') if error_code == 0 else print(f'{prefix} {fw}{br}Code {error_code}{sr}')

    await change_status.start()


# If error, open bug report or handle
@bot.event
async def on_command_error(ctx, er):

    # Create Date/Time prefix for console
    prefix = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC ", time.gmtime()) + Back.RED + Fore.WHITE + Style.BRIGHT)
    
    # Create timestamp when error was encountered and print to Bot console for logging purposes
    timestamp = ctx.message.created_at.now()
    print(f'{prefix}ERROR RAISED -> {er} {Back.RESET}')

    # Check if error fits in pre-defined list of errors to monitor and open Bug report
    for i in MONITOR_ERRORS:
        if i in str(er):

            # Open bug report, inform owner and user.
            owner_user = await bot.fetch_user(bot.owner_id)
            thumbnail = 'https://static.thenounproject.com/png/587438-200.png'

            owner_embed = discord.Embed(
                title='***__BUG REPORT__***',
                description=f'**Timestamp:** ```{timestamp}```\n**Server Name:** ```{ctx.guild.name}```\n**Channel ID:** ```{ctx.channel.id}```\n**Channel Name:** ```{ctx.channel.name}```\n**Message ID: **```{ctx.message.id}```\n**ERROR:** ```{er}```\n**User:** ```{ctx.author.name}```',
                colour=discord.Colour.red()
            )

            owner_embed.set_thumbnail(url=ctx.guild.icon)

            await owner_user.send(embed=owner_embed)

            user_embed = discord.Embed(
                title='BUG Encontrado', 
                description=f'Foi enviado um bug report para o Admin do bot. Correção em breve.', 
                colour=discord.Colour.yellow()
            )

            user_embed.set_footer(text=f'ID: {ctx.message.id}')
            user_embed.set_thumbnail(url=thumbnail)

            return await ctx.reply(embed=user_embed)

    # If issue is due to command being sent to private message, return to user.
    # If issue is not related to private message return to user informing that syntax is incorrect.
    return await ctx.reply(f'Este comando não pode ser utilizado em conversa privada **{random.choice(FRASE_MEIO)}**' if 'private messages' in str(er) else f'Tem um erro na sua sintaxe **{random.choice(FRASE_MEIO)}**, da uma conferida por favor.\nManda um `/help commandoAqui` pra ter mais informações de como usar o comando.')


# When joining a guild, confirm if guild is already set up in DB and sent thankful note to owner
@bot.event
async def on_guild_join(ctx):

    owner = await bot.fetch_user(ctx.owner.id)

    embed = discord.Embed(
    title="Olá! Eu sou o seu bot",
    description="Acabei de ser adicionado a este servidor. Estou aqui para ajudar e trazer mais funcionalidades para o seu servidor.",
    color=discord.Color.blue()
    )

    # 
    embed.add_field(name="Dúvidas ou suporte", value="Se você tiver alguma dúvida sobre como me usar ou precisar de suporte, não hesite em entrar em contato comigo. Estou sempre disponível para ajudar.")
    embed.add_field(name="Funcionalidades personalizadas", value="Além das funcionalidades padrão, eu também posso oferecer recursos personalizados de acordo com as necessidades do seu servidor. Entre em contato com o desenvolvedor pelo comando **/feedback**")
    embed.add_field(name="Comandos disponíveis", value="Digite !help para ver uma lista dos comandos disponíveis.")

    await owner.send(embed=embed)

    with guild_db:
        cursor = guild_db.cursor()
        cursor.execute("SELECT * FROM joined_guilds WHERE guild_id = ?", (ctx.id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO joined_guilds (guild_id) VALUES (?)", (ctx.id,))
            guild_db.commit()

# When removed from guild, send msg to server owner and set slash commands to disabled.    
@bot.event
async def on_guild_remove(ctx):

    owner = await bot.fetch_user(ctx.owner.id)
    thumbnail = 'https://www.iconsdb.com/icons/preview/white/remove-user-xxl.png'

    leaving_embed = discord.Embed(
        title='Que pena que está indo!', 
        description='Sinto muito que o bot não tenha atendido suas expectativas.\n\nCaso tenha alguma sugestão, por favor mande diretamentamente através deste canal com o comando **/feedback** para que possamos melhorar e continuar oferecendo um serviço cada vez melhor.', 
        colour=discord.Colour.green()
    )

    leaving_embed.set_thumbnail(url=thumbnail)

    await owner.send(embed=leaving_embed)

    with guild_db:
        cursor = guild_db.cursor()
        cursor.execute("UPDATE joined_guilds SET commands_enabled = ? WHERE guild_id = ?", (False, ctx.id))
        guild_db.commit()


@bot.event
async def on_member_join(member):
    prefix = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC ", time.gmtime()) + Back.RED + Fore.WHITE + Style.BRIGHT)
    print(f'{prefix} JOIN -> {member} just joined the server.')
    guild = bot.get_guild(member.guild.id)

    if not member.bot:

        e = discord.Embed(
                title="BEM VINDO!",
                description=f"Bem vindo ao servidor {member.guild.name}!",
                color=discord.Color.blue()
                )

        e.add_field(name="Leia as regras", value="Não deixe de ler as regras para que esteja sempre de acordo com o servidor!")
        e.add_field(name="Dúvidas ou suporte", value="Se você tiver alguma dúvida sobre como me usar ou precisar de suporte, não hesite em entrar em contato comigo. Estou sempre disponível para ajudar.")
        e.add_field(name="Funcionalidades personalizadas", value="Além das funcionalidades padrão, eu também posso oferecer recursos personalizados de acordo com as necessidades do seu servidor. Entre em contato com o desenvolvedor pelo comando **/feedback**")
        e.add_field(name="Comandos disponíveis", value="Digite !help para ver uma lista dos comandos disponíveis.")

        await member.create_dm()
        await member.dm_channel.send(embed=e)
        

# Monitor for messages and keep DB with all messages, authors and dates for auditing purposes
@bot.listen()
async def on_message(message):

    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime('%H:%M:%S')
    channel_id = message.channel.id
    message_id = message.id
    author_id = message.author.id
    content = message.content

    with msg_db:
        msg_cursor = msg_db.cursor()
        msg_cursor.execute("INSERT INTO messages (date, time, channel_id, message_id, author_id, content) VALUES (?, ?, ?, ?, ?, ?)", (date, time, channel_id, message_id, author_id, content))
        msg_db.commit()

@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(STATUS)))


asyncio.run(main())
