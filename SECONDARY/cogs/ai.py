# Import main modules
import discord
import random
import openai
import os

# Import secondary modules
from discord.ext import commands
from discord import app_commands
from math import floor
from dotenv import load_dotenv

# Import variables and standard functions from local file
from utils import *

# Load hidden TOKEN
load_dotenv()

openai.api_key = CHATGPT_API_TOKEN

# Define class
class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        '''Commands defined in this cog are for the use of ChatGPT 3.5 AI.

        cog_chatgpt_ai v2.00'''


    # Chat GPI AI
    @app_commands.command(name='ai', description='API do ChatGPT com limite de 1000 caracteres por resposta. Uso: EscrevaOQueQuiser')
    async def ai(self, interaction: discord.Interaction, *, message: str):

            # Check if user is not the bot itself
            if interaction.user == self.bot:
                return
            
            reply = await interaction.response.send_message(f'Aguarde, buscando resposta.', ephemeral=False)

            # Trigger typing decorator and call main function
            async with interaction.channel.typing(): 
                bot_response = chatgpt_response(prompt=message)

            # Send response to user
            await interaction.followup.send(bot_response, ephemeral=False)


def chatgpt_response(prompt):
    
    response = openai.Completion.create(
    model = 'text-davinci-003',
    prompt = prompt,
    temperature = 0.3,
    max_tokens = 1000
    )

    response_dict = response.get('choices')

    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]['text']
        # TODO: If response contains <code> or </code> replace by a `
        return prompt_response
    
async def setup(bot):
    await bot.add_cog(ChatGPT(bot))