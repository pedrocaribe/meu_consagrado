# Import main modules
import discord, humanize, os, psutil, time, datetime, math

# Import secondary modules
from multiprocessing import set_forkserver_preload
from discord.ext import commands

# Import variables and standard functions from local file
from var_Reuse import *

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''Commands defined in this cog are for study purposes.

    cog_Study v1.00'''

# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(Study(bot))