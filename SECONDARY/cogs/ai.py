# Import main modules
import discord
import random
import openai
import os
import re

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


class ChatGPT(commands.Cog):
    """A Cog for integrating ChatGPT AI functionality into the bot.

    This Cog provides a command to interact with the ChatGPT model, allowing users to have conversations with the AI.
    The AI's responses are limited to 1000 characters per message.

    Attributes:
        bot: discord.ext.commands.Bot
            The bot instance associated with the cog.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ai', description='ChatGPT com limite de 1000 caracteres por resposta')
    async def ai(self, interaction: discord.Interaction, *, message: str):
        """A command to interact with the ChatGPT AI.

        This command allows users to send a message to the ChatGPT model and receive a response.
        The response is limited to 1000 characters per message due to pay-per-tokens.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.

            message: str
                The message provided by the user as input to the AI.

        Returns:
            This function does Not return anything.
        """

        # Check if user is not the bot itself
        if interaction.user == self.bot:
            return

        await interaction.response.send_message(f'Aguarde, buscando resposta.', ephemeral=False)

        # Trigger typing decorator and call main function
        async with interaction.channel.typing():
            bot_response = chatgpt_response(prompt=message)

        # Send response to user
        await interaction.followup.send(
            f"**Pergunta:**\n\n"
            f"`{message}`\n\n"
            f"**Resposta:**\n"
            f"{bot_response}", ephemeral=False)


def chatgpt_response(prompt: str):
    """Generate a response from the ChatGPT AI model.

    This function sends a prompt to the ChatGPT AI model and retrieves a response. Model utilized is
    'text-davinci-003', with 'temperature=0.3'

    Args:
        prompt: str
            The prompt to send to the AI model.

    Returns:
        prompt_response: str
            The response generated by the AI model.
    """

    response = openai.Completion.create(model='text-davinci-003', prompt=prompt, temperature=0.3, max_tokens=1000)

    response_dict = response.get('choices')

    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]['text']
        prompt_response = re.sub(r"</?code>", "`", prompt_response)
        return prompt_response


async def setup(bot):
    await bot.add_cog(ChatGPT(bot))