# Import main modules
import discord
import random

# Import secondary modules
from discord import app_commands
from utils import *

# Define class
class Cs50(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Mario Less function
    @app_commands.command(name="mario-less", description='Projeto criado durante Week 1/pset1 do curso CS50. Uso: QtDeAndares (de 1 a 8)')
    async def mario_less(self, interaction: discord.Interaction, bricks: int):

        # Check if user inputted value between 1 and 8
        if bricks < 1 or bricks > 8 or bricks == None:
            await interaction.response.send_message(f'Quantidade deve ser entre 1 e 8, **{random.choice(FRASE_MEIO)}**.')
        
        else:

            # Send bricks increasing in one message
            if bricks == 1:
                await interaction.response.send_message(f'#')
            else:
                text = ''
                for i in range(bricks):
                    j = (bricks - i) -1
                    text += ('...' * j + '#' * (i + 1) + '\n')
                await interaction.response.send_message(text)
    
    # Mario More Function
    @app_commands.command(name='mario-more', description='Projeto criado durante Week 1/pset1 do curso CS50. Uso: QtDeAndares (de 1 a 8)')
    async def mario_more(self, interaction: discord.Interaction, bricks: int):

        # Check if user inputted value between 1 and 8
        if bricks < 1 or bricks > 8 or bricks == None:
            await interaction.response.send_message(f'Quantidade deve ser entre 1 e 8, **{random.choice(FRASE_MEIO)}**.')

        else:

            # Send bricks increasing in one message
            text = ''
            for i in range(bricks):
                j = (bricks - i) - 1
                text += (('...' * j) + ('#' * (i + 1)) + ' ' + ('#' * (i + 1)) + '\n')
            
            await interaction.response.send_message(text)

    # Credit Card Check Function
    @app_commands.command(name='cccheck', description='Projeto criado durante Week 1/pset1 do curso CS50. Uso: NumeroDoCartao')
    async def cccheck(self, interaction: discord.Interaction, ccnumber: int):

        # Initialize variables
        ccnumber2 = ccnumber // 10
        cc = ccnumber
        cc_digits = sumOfDigits1 = sumOfDigits2 = checkSum = loopCounter = 0

        # Extract last digit from credit card number
        lastDigit = lastDigitExtractedProcessed(ccnumber)

        # Calculate how many digits in credit card number
        while cc > 1:
            cc = cc / 10
            cc_digits += 1

        # Conditions to define vendor
        if cc_digits == 13:
            vendor = "VISA"
            loopCounter = 7
        elif cc_digits == 16 and (ccnumber > 4000000000000000 and ccnumber < 5000000000000000):
            vendor = "VISA"
            loopCounter = 8
        elif cc_digits == 16 and (ccnumber > 5100000000000000 and ccnumber < 5600000000000000):
            vendor = "MASTERCARD"
            loopCounter = 8
        elif cc_digits == 15 and ((ccnumber > 340000000000000 and ccnumber < 350000000000000) or (ccnumber > 370000000000000 and ccnumber < 380000000000000)):
            vendor = "AMEX"
            loopCounter = 7
        else:
            vendor = "INVALID"

        # Loop and retrieve sum of first half of Luhn's Algorithm
        for i in range(loopCounter):
            sumOfDigits1 += digitExtractedProcessed(ccnumber)
            ccnumber = reduceCardN(ccnumber)

        # Loop and retrieve sum of second half of Luhn's Algorithm
        for j in range(loopCounter):
            sumOfDigits2 += digitExtractedProcessed2(ccnumber2)
            ccnumber2 = reduceCardN(ccnumber2)

        # Final calculations and checksum
        checkSum = sumOfDigits1 + sumOfDigits2 + lastDigit

        # Return to user if CC number is valid or not
        if checkSum % 10 == 0:
            return await interaction.response.send_message(f'Número de cartão de crédito válido! Bandeira: **{vendor}**')
        else:
            return await interaction.response.send_message(f'Número de cartão de crédito **inválido**!')



async def setup(bot):
    await bot.add_cog(Cs50(bot))