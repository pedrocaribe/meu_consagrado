# Import main modules
import random
import discord

# Import secondary modules
from discord.ext import commands
from discord import app_commands


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        '''Commands defined in this cog are for entertainment of gambling commands.

                        gamble v1.00'''

    # Flip coin
    @app_commands.command(name='moeda', description='Jogue a moeda rapidamente.')
    async def coin(self, interaction: discord.Interaction):

        # Random floating number between 0 and 1
        a = random.random()

        return await interaction.response.send_message('**Coroa!**' if a > 0.50 else '**Cara!**')

    # Roll dices
    @app_commands.command(name='dados', description='Role os dados rapidamente. Uso (num de 1 a 3 representando a quantidadee de dados)')
    async def dice(self, interaction: discord.Interaction, dicenum: int = 1):

        await interaction.response.send_message(f'Rolando {dicenum} dados... 🎲🎲\n' if dicenum > 1 else f'Rolando dado... 🎲\n')
        
        embed = discord.Embed(
            title='Dados', 
            description='Rolando Dados...', 
            colour=discord.Colour.blue()
        )

        # Roll for each dice
        for i in range(1, dicenum + 1):
            
            r = random.randint(1, 6)
            
            embed.add_field(
                name=f'**__DADO {i}__**', 
                value=f'**-> {r} <-**'
            )

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
