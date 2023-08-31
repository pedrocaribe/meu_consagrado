# Import main modules
import random
import discord

# Import secondary modules
from discord.ext import commands
from discord import app_commands


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='moeda', description='Jogue a moeda rapidamente.')
    async def coin(self, interaction: discord.Interaction):
        """A command to quickly flip a coin.

        This command simulates a coin flip and sends the result as "Cara!" (Heads) or "Coroa!" (Tails).

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.

        Returns:
            This function does Not return anything.
        """

        a = random.random()  # Random floating number between 0 and 1

        return await interaction.response.send_message('**Coroa!**' if a > 0.50 else '**Cara!**')

    # Roll dices
    @app_commands.command(
        name='dados', description='Role os dados rapidamente. Uso (num de 1 a 3 representando a quantidadee de dados)')
    async def dice(self, interaction: discord.Interaction, dicenum: int = 1):
        """A command to quickly roll dice.

        This command simulates rolling dice(s) and sends the results.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            dicenum: int [OPTIONAL]
                The number of dice to be rolled. Defaults to 1.

        Returns:
            This function does Not return anything.
        """

        await interaction.response.send_message(
            f'Rolando {dicenum} dados... 🎲🎲\n' if dicenum > 1 else f'Rolando dado... 🎲\n')
        
        embed = discord.Embed(
            title='Dados', 
            description='Rolando Dados...', 
            colour=discord.Colour.blue()
        )

        # Roll for each dice
        for i in range(dicenum):

            r = random.randint(1, 6)

            embed.add_field(
                name=f'**__DADO {i + 1}__**',
                value=f'**-> {r} <-**')

        await interaction.edit_original_response(embed=embed)

    # Greater than or smaller than 6 faced dices
    @app_commands.command(name='dd', description='Role dados de mais ou menos de 6 faces')
    async def dice_dd(self, interaction: discord.Interaction, faces: int):
        await interaction.response.send_message(f'Rolando dado DD de {faces} faces...\n')

        embed = discord.Embed(
            title=f'Dado DD {faces} faces', 
            description='Rolando Dados...', 
            colour=discord.Colour.blue()
        )

        # Random number between 1 and maximum number of faces
        r = random.randint(1, faces)

        embed.add_field(
            name=f'**__RESULTADO__**', 
            value=f'**-> {r} <-**'
        )

        await interaction.edit_original_response(embed=embed)


# Define setup function for Cog
async def setup(bot):
    await bot.add_cog(Gamble(bot))
