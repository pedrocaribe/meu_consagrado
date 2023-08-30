# Import main modules
import json
import os
import random
import discord
import dill

# Import secondary modules
from settings import *
from discord.ext import commands
from discord import app_commands
from typing import NoReturn
from math import floor

units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']


async def embed_empty_field(embed: discord.Embed):
    return embed.add_field(name="\u200b", value="\u200b")


async def icon(name: str, embed: discord.Embed):
    icons = {os.path.splitext(x)[0]: x for x in os.listdir("ICONS")}
    if name in icons:
        file = discord.File(f'ICONS/{icons[name]}', icons[name])
        embed.set_thumbnail(url=f'attachment://{icons[name]}')
        return file, embed


async def get_jokes():
    with open(os.path.join(DATA_DIR, "badwords.json"), encoding='utf8') as bw_file:
        bws = json.load(bw_file)
    bw = random.choice(list(bws['badwords']))
    return bw


async def dummy_awaitable_callable(*args, **kwargs) -> NoReturn:
    raise NotImplementedError("This function is a dummy function and is not meant to be called.")


# Connect to DB
def db_connect(db):
    if os.path.isfile(db):
        dbc = sqlite3.connect(db)
        return dbc
    else:
        return None


# Function to load cogs when initiating Bot
async def load_cogs(bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init.py__":
            await bot.load_extension(f'cogs.{filename[:-3]}')


def humanizer(size, d_unit):
    for unit in units:
        if unit == d_unit:
            break
        size /= 1024.0
    return f'{size:.{2}f}{unit}'


def get_size(size):
    for unit in units:
        if size < 1024.0:
            break
        size /= 1024.0
    return f'{size:.{2}f}{unit}'


def digitExtractedProcessed(card_number):
    a = floor(floor(card_number % 100) // 10) * 2
    if a > 9:
        a = a // 10 + a % 10
    return a


def digitExtractedProcessed2(card_number):
    a = (floor(card_number % 100) // 10)
    return a


def reduceCardN(card_number):
    rdCardN = 0
    if card_number > 134:
        rdCardN = card_number // 100
    elif card_number < 100:
        rdCardN = card_number // 10
    else:
        rdCardN = card_number
    return rdCardN


def lastDigitExtractedProcessed(card_number):
    a = card_number % 10
    return a


class EnableModal(discord.ui.Modal, title='Regras'):

    info = discord.ui.Button


class Ticket:
    def __init__(self, ctx: commands.Context, db: sqlite3.Connection, error: commands.CommandError = None):
        self.timestamp = ctx.message.created_at.now()
        self.guild_name = ctx.guild.name if ctx.guild else None
        self.guild_id = ctx.guild.id if ctx.guild else None
        self.channel_id = ctx.channel.id if ctx.guild else None
        self.channel_name = ctx.channel.name if ctx.guild else None
        self.message_id = ctx.message.id
        self.error = str(error)
        self.user = ctx.author.name
        self.user_id = ctx.author.id
        self.db = db

    def create_ticket(self):
        with self.db:
            cur = self.db.cursor()
            cur.execute(
                "INSERT INTO tickets ("
                "guild_id, "
                "channel_id, "
                "message_id, "
                "timestamp, "
                "error, "
                "user_id, "
                "status) VALUES (?,?,?,?,?,?,?)",
                (self.guild_id,
                 self.channel_id,
                 self.message_id,
                 self.timestamp,
                 self.error,
                 self.user_id,
                 "OPEN")
                )
            self.db.commit()
