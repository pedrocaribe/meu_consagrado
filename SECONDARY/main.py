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
import logging.handlers

# Import secondary modules
from discord.ext import commands, tasks
from colorama import Back, Fore, Style
from datetime import datetime

# Import local utilities and variables
from settings import *
from utils import *

# GLOBAL Declarations
intent = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intent)

# Styling
fy = Fore.YELLOW
fw = Fore.WHITE
fg = Fore.GREEN
fr = Fore.RED
bg = Back.GREEN
br = Back.RED
bb = Back.BLACK
bres = Back.RESET
sb = Style.BRIGHT
sres = Style.RESET_ALL

# Set up DBs
guild_db = db_connect(GUILD_DB)
msg_db = db_connect(MSG_DB)
ticket_db = db_connect(TICKET_DB)

# Set up Logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
    filename="logs/debugs.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,
    backupCount=15,
)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)-10s] %(name)-22s: %(module)-10s: %(message)s", style="%")
handler.setFormatter(formatter)
logger.addHandler(handler)

# TODO: ADD DOCSTRINGS TO ALL CLASSES


# Definition of main function, load all cogs and start bot
async def main():
    async with bot:
        await load_cogs(bot)
        await bot.start(DISCORD_TOKEN)


# Print load message once ready
@bot.event
async def on_ready():
    """A function triggered when the bot is ready to start receiving events and interact with Discord.

        This function prints information about the bot's readiness and connections, including
        Discord version, Python version, loaded cogs, bot's login details, and database connections.
        If any database connection fails, it indicates an error code.
        It also starts a loop for changing the bot's Rich Presence.

        Note:
            - The variables like 'bb', 'fg', 'bres', 'fw', etc., are global variables declared for
                Styling the printed output on error.

        Args:
            This function takes no arguments.

        Returns:
            This functions does Not return anything.
        """

    # Create Date/Time prefix for console
    prefix = (bb + fg + time.strftime("%H:%M:%S UTC", time.gmtime()) + bres + fw + sb)

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
    if ticket_db:
        print(f'{prefix} {fg}Successfully {fw}Connected to DB {fy}{TICKET_DB}')
    else:
        print(f'{prefix} {fr}ERROR {fw}Connecting to DB {fy}{TICKET_DB}')
        error_code = 3

    print(f'{prefix} {fw}{bg}Code {error_code}{Style.RESET_ALL}') if error_code == 0 else f'{prefix} {fw}{br}Code {error_code}{sres}'

    await change_status.start()


@bot.event
async def on_command_error(ctx: commands.Context, er: commands.CommandError):
    """Listen for errors and handle

    Redefinition of on_command_error method to handle errors differently according to
    user owner necessity.
    In case of reported bugs, create a bug Ticket.

    Parameters:
        ctx: commands.Context
            The context used for command invocation.
        er: commands.CommandError
            The Exception raised.

    Returns:
        This method returns differently per Exception encountered.
    """

    # This prevents any commands with local handlers being handled here.
    if hasattr(ctx.command, "on_error"):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog.has_error_handler():
            return

    # Create Date/Time prefix for console
    prefix = (bb + fg + time.strftime("%H:%M:%S UTC ", time.gmtime()) + br + fw + sb)

    print(f'{prefix}ERROR RAISED -> {er} {bres}')

    er = getattr(er, 'original', er)

    # If exception in ignore list, ignore
    if isinstance(er, IGNORE_ERRORS):
        return

    # If issue is due to command being sent to private message, return to user.
    elif isinstance(er, commands.NoPrivateMessage):
        return await ctx.reply(
            f'Este comando não pode ser utilizado em conversa privada **{random.choice(FRASE_MEIO)}**')

    # If issue is not related to private message return to user informing that syntax is incorrect.
    elif isinstance(er, (commands.BadArgument, commands.CommandNotFound)):
        return await ctx.reply(
            f'Tem um erro na sua sintaxe **{random.choice(FRASE_MEIO)}**, da uma conferida por favor.')
    else:
        # Open bug report, inform owner and user.
        owner_user = await bot.fetch_user(bot.owner_id)
        ticket = Ticket(ctx=ctx, error=er, db=ticket_db)

        owner_embed = discord.Embed(
            title='***__BUG REPORT__***',
            description=f'**Timestamp:** ```{ticket.timestamp}```\n'
                        f'**Server Name:** ```{ticket.guild_name}```\n'
                        f'**Channel ID:** ```{ticket.channel_id}```\n'
                        f'**Channel Name:** ```{ticket.channel_name}```\n'
                        f'**Message ID: **```{ticket.message_id}```\n'
                        f'**ERROR:** ```{str(ticket.error)}```\n'
                        f'**User:** ```{ticket.user}```',
            colour=discord.Colour.red()
        )

        ticket.create_ticket()

        thumbnail, owner_embed = await icon("error", owner_embed)

        await owner_user.send(file=thumbnail, embed=owner_embed)

        user_embed = discord.Embed(
            title='BUG Encontrado',
            description=f'Foi enviado um bug report para o Admin do bot. Correção em breve.',
            colour=discord.Colour.yellow()
        )
        thumbnail, user_embed = await icon("error", user_embed)

        user_embed.set_footer(text=f'ID: {ctx.message.id}')

        return await ctx.reply(file=thumbnail, embed=user_embed)


# When joining a guild, confirm if guild is already set up in DB and send thankful note to owner
@bot.event
async def on_guild_join(guild: discord.Guild):
    """A coroutine triggered when the bot joins a new guild (server).

        This function sends a welcome message to the guild's owner via direct message,
        providing information about the bot's features, custom functionalities, and available
        commands. Additionally, it updates or inserts information about the guild into the database.

        Args:
            guild: discord.Guild
                The guild (server) the bot has joined.

        Returns:
            This function does Not return anything.
        """

    owner = await bot.fetch_user(guild.owner.id)

    embed = discord.Embed(
        title="Olá, meu Consagrado!",
        description="Acabei de ser adicionado a este servidor. "
                    "Estou aqui para ajudar e trazer mais funcionalidades para todos.",
        color=discord.Color.blue()
        )

    # 
    embed.add_field(
        name="Dúvidas ou suporte",
        value="Se você tiver alguma dúvida sobre como me usar ou precisar de suporte, "
              "não hesite em entrar em contato comigo. Estou sempre disponível para ajudar.",
        inline=False)
    embed.add_field(
        name="Funcionalidades personalizadas",
        value="Além das funcionalidades padrão, eu também posso oferecer recursos personalizados "
              "de acordo com as necessidades do seu servidor. Entre em contato com o "
              "desenvolvedor pelo comando **/feedback**",
        inline=False)
    embed.add_field(
        name="Comandos disponíveis",
        value="Digite !help para ver uma lista dos comandos disponíveis.",
        inline=False)

    thumbnail, embed = await icon("consagrado", embed)

    await owner.send(file=thumbnail, embed=embed)

    with guild_db:
        guild_id = guild.id
        guild_name = guild.name
        guild_owner_id = guild.owner.id
        joined_date = datetime.today().strftime('%Y-%m-%d')
        cursor = guild_db.cursor()
        result = cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,)).fetchone()

        if result is None:
            cursor.execute("INSERT INTO guilds ("
                           "guild_id,"
                           "guild_name,"
                           "guild_owner_id,"
                           "joined_date,"
                           "active) "
                           "VALUES (?,?,?,?,?)", (guild_id, guild_name, guild_owner_id, joined_date, True))
            guild_db.commit()
        else:
            cursor.execute("UPDATE guilds SET active = (?) WHERE guild_id = (?)", (True, guild_id,))
            guild_db.commit()


# When removed from guild, send msg to server owner and set slash commands to 'Disabled'.
@bot.event
async def on_guild_remove(guild: discord.Guild):
    """A coroutine triggered when the bot leaves a guild (server).

            This function sends a goodbye message to the guild's owner via direct message,
            requesting feedback as to why the bot was removed.
            Additionally, it updates information about the guild in the database.

            Args:
                guild: discord.Guild
                    The guild (server) the bot was removed from.

            Returns:
                This function does Not return anything.
            """

    owner = await bot.fetch_user(guild.owner.id)
    guild_id = guild.id

    leaving_embed = discord.Embed(
        title='Que pena que está indo!', 
        description='Sinto muito que o bot não tenha atendido suas expectativas.\n\n'
                    'Caso tenha alguma sugestão, por favor mande diretamentamente através deste canal com o comando '
                    '**/feedback** para que possamos melhorar e continuar oferecendo um serviço cada vez melhor.',
        colour=discord.Colour.green()
    )
    thumbnail, leaving_embed = await icon("guild_remove", leaving_embed)

    await owner.send(file=thumbnail, embed=leaving_embed)

    with guild_db:
        cursor = guild_db.cursor()
        cursor.execute("UPDATE guilds SET active = (?) WHERE guild_id = (?)", (False, guild_id,))
        guild_db.commit()


@bot.event
async def on_member_join(member: discord.Member):
    """Monitor for new members

    Monitors for new members and sends welcome message.

    Parameters:
        member: The member to send the welcoming message to.

    Returns:
        This function does Not return anything.
    """

    prefix = (bb + fg + time.strftime("%H:%M:%S UTC ", time.gmtime()) + br + fw + sb + bres)
    print(f'{prefix} JOIN -> {member} just joined the {member.guild.name} server.')
    guild = bot.get_guild(member.guild.id)

    if not member.bot:

        e = discord.Embed(
                title="BEM VINDO!",
                description=f"Bem vindo ao servidor **{member.guild.name}**!",
                color=discord.Color.blue()
                )

        await embed_empty_field(e)

        e.add_field(
            name="Leia as regras",
            value="Não deixe de ler as regras para que esteja sempre de acordo com o servidor!",
            inline=False)

        await embed_empty_field(e)

        e.add_field(
            name="Dúvidas ou suporte",
            value="Se você tiver alguma dúvida sobre como me usar ou precisar de suporte, "
                  "não hesite em entrar em contato comigo. Estou sempre disponível para ajudar.",
            inline=False)

        await embed_empty_field(e)

        e.add_field(
            name="Funcionalidades personalizadas",
            value="Além das funcionalidades padrões, "
                  "eu também posso oferecer recursos personalizados de acordo com as necessidades do servidor. "
                  "Entre em contato com o desenvolvedor pelo comando **/feedback** para qualquer solicitação.",
            inline=False)

        await embed_empty_field(e)

        e.add_field(
            name="Comandos disponíveis",
            value="Digite !help para ver uma lista dos comandos disponíveis.",
            inline=False)

        thumbnail, e = await icon("consagrado", e)

        await member.create_dm()
        await member.dm_channel.send(file=thumbnail, embed=e)


@bot.listen()
async def on_message(message: discord.Message):
    """Monitor for messages

    Monitor for messages and keep DB updated with all messages, authors and dates,
    for auditing purposes.

    Parameters:
        message: Message from which to retrieve all information.
    Returns:
         This function does Not return anything.
    """

    m_date = datetime.today().strftime('%Y-%m-%d')
    m_time = datetime.today().strftime('%H:%M:%S')
    guild_id = message.guild.id if message.guild else None
    channel_id = message.channel.id
    message_id = message.id
    author_id = message.author.id
    content = message.content

    with msg_db:
        if not message.author.bot:
            msg_cursor = msg_db.cursor()
            msg_cursor.execute("INSERT INTO messages("
                               "guild_id, channel_id, message_id, author_id, date, time, content) "
                               "VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (guild_id, channel_id, message_id, author_id, m_date, m_time, content))
            msg_db.commit()


@tasks.loop(seconds=20)
async def change_status():
    """Initiate status rotation

    Initiates task to change status every 20 seconds.

    Parameters:
        This function does Not take any parameters.
    Returns:
        This function does Not return anything.
    """

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(STATUS)))


asyncio.run(main())
