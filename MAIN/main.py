# Import base modules
import os, discord, random, importlib, asyncio, sqlite3

# Import error logging modules
import traceback, logging

# Import secondary modules
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv

# Vars and general use functions from local file
from var_Reuse import *

# Start SQL DB
mdb = sqlite3.connect('messages.db')
cursor = mdb.cursor()

# Load hidden token
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
intent = discord.Intents.all()

bot = commands.Bot(command_prefix='%', intents=intent)

# Define main (according to recent changes //https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)
async def main():
    async with bot:
        await loadall()
        await bot.start(TOKEN)

# Define behaviour once logged in
@bot.event
async def on_ready():
    print(f'Code 0 -> We have successfully logged in as {bot.user} .')

    # Start status rotation and load cogs
    change_status.start()
    await loadall()

# Function to load cogs when initiating Bot
async def loadall():
    for cog in bot_cogs:
        await bot.load_extension(f'{cog}')
    print('All cogs loaded successfully.')

# Function to reload all cogs without restarting the Bot
@bot.command(hidden=True, name='reloadall')
@commands.is_owner()
async def reloadall(ctx):
    e = discord.Embed(title=':ok:     ***Extensões Recarregadas***     :white_check_mark:', description='')
    try:
        for cog in bot_cogs:
            await bot.reload_extension(f'{cog}')
            e.description += f'**->** {cog}\n'

        await ctx.reply(embed=e)
    # If error encountered, let user know
    except Exception as a:
        e1 = discord.Embed(description=':no_entry:     ***Erro ao recarregar Extensões***     \n')
        e1.description += f'{a}'
        await ctx.reply(embed=e1)

# Loop through pre-defined status messages
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

# Function to report errors or bugs
@bot.event
async def on_command_error(ctx, error):

    # Create timestamp when error was encountered and print to Bot console
    timestamp = ctx.message.created_at.now()
    print(f'ERROR RAISED -> {error}, {timestamp}')
    
    # Check if error fits in pre-defined list of erros to ignore and just print to Bot console
    for i in ignore_errors:
        if i in str(error):
            return print(f'Error index[{i}] logged.')
    
    # Check if error fits in pre-defined list of errors to monitor and open Bug report
    for i in monitor_errors:
        if i in str(error): 
            owner_user = await bot.fetch_user(ctx.guild.owner.id)
            
            await owner_user.send(f'***__BUG REPORT__***\n\n**Timestamp:** {timestamp}\n\n**Channel ID:** {ctx.channel.id}\n**Channel Name:** {ctx.channel.name}\n**Message ID: **{ctx.message.id}\n\n**ERROR:** {error}.\n\n\n**User:** {ctx.author.name}\n\n\n')
            
            embed = discord.Embed(title='BUG Encontrado', description=f'Foi enviado um bug report para o Admin do bot. Correção em breve.', colour=discord.Colour.yellow())
            embed.set_footer(text=f'ID: {ctx.message.id}')
            embed.set_thumbnail(url='https://static.thenounproject.com/png/587438-200.png')
            return await ctx.reply(embed=embed)
    await ctx.reply(f'Tem um erro na sua sintaxe **{random.choice(fraseMeio)}**, da uma conferida por favor.\nManda um `/help commandoAqui` pra ter mais informações de como usar o comando.')

# Greet user when joining server, send rules and apply standard role. Also print event and username to Bot console
@bot.event
async def on_member_join(member):
    print(f'JOIN -> {member} just joined the server.')
    guild = bot.get_guild(member.guild.id)
    
    if not member.bot:
        role = discord.utils.get(guild.roles, name='Andarilhos')
        await discord.Member.add_roles(member, role)
        await member.create_dm()
        await member.dm_channel.send(f'Bem vindo ao discord da __**METRA**__, {random.choice(fraseMeio)}.\nLeia as regras e reaja na mensagem com um {emoji_id} para ter acesso ao servidor.\n\nSiga as regras, aproveite, e qualquer coisa estamos por aqui!')
    else:
        role = discord.utils.get(guild.roles, name='Bots')
        await discord.Member.add_roles(member, role)

# Monitor for reaction on rules message, when reacted give Member role to user
@bot.event
async def on_raw_reaction_add(payload):
    
    if payload.message_id == role_msg_id and payload.emoji.name == emoji_id:
        member = payload.member
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name='Membros')
        
        await discord.Member.add_roles(member, role)
        
# Monitor for messages with specific words in it, and reply accordingly
@bot.listen()
async def on_message(message):

    if message.author.name == bot.user: return

    if 'boa noite' in message.content.lower():
        await message.channel.send('Dorme bem **'+message.author.name+'**, e bom descanso!')
    elif ('bom dia' in message.content.lower() or 'boa tarde' in message.content.lower()):
        await message.channel.send('Opa, **'+random.choice(fraseMeio)+'**, '+random.choice(fraseFinal))
    elif ('bot burro' in message.content.lower()):
        await message.channel.send(f'**{random.choice(fraseMeio)}** perdeu o medo do perigo...')

# Monitor for messages and keep a DB with all messages, authors and dates for auditing purposes
@bot.listen()
async def on_message(message):

    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime('%H:%M:%S')
    channel_id = message.channel.id
    message_id = message.id
    author_id = message.author.id
    content = message.content

    cursor.execute("INSERT INTO messages (date, time, channel_id, message_id, author_id, content) VALUES (?, ?, ?, ?, ?, ?)", (date, time, channel_id, message_id, author_id, content))
    mdb.commit()

# Run Bot with token from .env file
asyncio.run(main())