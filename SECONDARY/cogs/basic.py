# Import main modules
import random
import math
import discord
import sympy

# Import secondary modules
from discord.ext import commands
from discord import app_commands


class Basic(commands.Cog):
    """A Cog for basic commands.

    This Cog provides basic commands for the bot.

    Attributes:
        bot: discord.ext.commands.Bot
            The bot instance associated with the cog.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Ping, Pong. Verificar ping do BOT')
    async def ping(self, interaction: discord.Interaction):
        """A command to check the bot's ping.

        This command calculates and displays the bot's ping in milliseconds.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.

        Returns:
            This function does Not return anything.
        """

        lat = round(self.bot.latency * 1000)
        return await interaction.response.send_message(f'Pong!\n\n`Bot ping {lat} ms`')

    @app_commands.command(name='pong', description='Pong, Ping')
    async def pong(self, interaction: discord.Interaction):
        """A command to respond with "Ping!".

        This command is a simple response to the user's pong command, saying "Ping!".

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.

        Returns:
            This function does Not return anything.
        """

        return await interaction.response.send_message('Ping!')

    @app_commands.command(name='invite', description='Cria convite temporário por tempo pré-determinado')
    @commands.guild_only()
    async def invite(self, interaction: discord.Interaction):
        """A command to create a temporary invite link for a predetermined duration.

        This command generates a temporary invite link for the current channel with a maximum age of 5 minutes.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.

        Returns:
            This function does Not return anything.
        """

        link = await interaction.channel.create_invite(max_age=300)
        await interaction.response.send_message(f'Convite válido por 5 minutos: {link}')

    @app_commands.command(name="matematica", description="Resolva expressões matemáticas de forma rápida")
    async def math(self, interaction: discord.Interaction, expression: str):
        """A command to solve mathematical expressions quickly.

        This command takes a mathematical expression as input and attempts to solve it using the sympy
        library. It then sends a message with the original expression and its calculated result.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            expression: str
                The mathematical expression to be solved.

        Returns:
            This function does Not return anything.
        """

        try:
            # Parse expression
            parsed_expr = sympy.sympify(expression)
            # Evaluate parsed expression (replaced eval)
            calculated = parsed_expr.evalf()
            
            embed = discord.Embed(
                title='Expressão Matemática', 
                description=f'`Expressão` {expression}\n `Resposta` {calculated}', 
                color=discord.Color.green(), 
                timestamp=interaction.created_at
            )

            await interaction.response.send_message(embed=embed)

        except (sympy.SympifyError, ValueError, TypeError):
            await interaction.response.send_message("Isto não é um problema matemático. Tente novamente.")


# Define setup function for Cog
async def setup(bot):
    await bot.add_cog(Basic(bot))
