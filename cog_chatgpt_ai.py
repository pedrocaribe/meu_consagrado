# Import main modules
import discord, random, openai, os
from dotenv import load_dotenv

# Import secondary modules
from discord.ext import commands
from math import floor

# Import variables and standard functions from local file
from var_Reuse import *

# Load hidden TOKEN
load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_TOKEN')

# Define class
class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        '''Commands defined in this cog are for the use of ChatGPT 3.5 AI.

        cog_chatgpt_ai v2.00'''


    # Mario Less function
    @commands.command(name='ai', aliases=['chatgpt'], help='API do ChatGPT com limite de 1000 caracteres por resposta\n\n Uso: %ai EscrevaOQueQuiser')
    async def ai(self, ctx, *, message):

            if ctx.message.author == self.bot:
                return
            
            reply = await ctx.reply(f'Aguarde, buscando resposta.')        
            
            async with ctx.message.channel.typing():
                bot_response = chatgpt_response(prompt=message)
                await discord.Message.edit(reply, content = bot_response)


def chatgpt_response(prompt):
    response = openai.Completion.create(
    model = 'text-davinci-003',
    prompt = prompt,
    temperature = 0.7,
    max_tokens = 1000
    )

    response_dict = response.get('choices')

    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]['text']
        return prompt_response
    
# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(ChatGPT(bot))