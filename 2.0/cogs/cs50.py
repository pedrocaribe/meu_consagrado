# Import main modules
import discord
import random

# Import secondary modules
from discord.ext import commands
from discord import app_commands

# Import variables and standard functions from local file
from utils import *
from settings_files import *


class Cs50(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mario-less", description='Projeto criado durante Week 1/pset1 do curso CS50')
    async def mario_less(self, interaction: discord.Interaction, bricks: int):
        """A command to print a Mario pyramid with specified number of bricks.

        This command creates a pyramid of bricks similar to the ones seen in the game Mario.
        The number of bricks in each row is determined by the user input.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            bricks: int
                The number of bricks to be used in the pyramid.

        Returns:
            This function does Not return anything.
        """

        # Check if user inputted value between 1 and 8
        if not 1 <= bricks <= 8:
            return await interaction.response.send_message(
                f'Quantidade deve ser entre 1 e 8, **{random.choice(FRASE_MEIO)}**.')

        # Send bricks increasing all in one message
        text = ''
        for i in range(bricks):
            j = (bricks - i) - 1
            text += ('...' * j + '#' * (i + 1) + '\n')
        await interaction.response.send_message(text)

    @app_commands.command(name='mario-more', description='Projeto criado durante Week 1/pset1 do curso CS50. Uso: QtDeAndares (de 1 a 8)')
    async def mario_more(self, interaction: discord.Interaction, bricks: int):
        """A command to print a Mario pyramid with mirroed specified number of bricks.

        This command creates a pyramid of bricks similar to the ones seen in the game Mario.
        The number of bricks in each row side is determined by the user input.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            bricks: int
                The number of bricks to be used in the pyramid.

        Returns:
            This function does Not return anything.
        """

        # Check if user inputted value between 1 and 8
        if not 1 <= bricks <= 8:
            return await interaction.response.send_message(
                f'Quantidade deve ser entre 1 e 8, **{random.choice(FRASE_MEIO)}**.')

        # Send bricks increasing all in one message
        text = ''
        for i in range(bricks):
            j = (bricks - i) - 1
            text += (('...' * j) + ('#' * (i + 1)) + ' ' + ('#' * (i + 1)) + '\n')

        await interaction.response.send_message(text)

    # Credit Card Check Function
    @app_commands.command(name='cccheck', description='Projeto criado durante Week 1/pset1 do curso CS50. Uso: NumeroDoCartao')
    async def cccheck(self, interaction: discord.Interaction, ccnumber: int):
        """
        A command to check the validity of a credit card number using the Luhn's Algorithm.

        This command checks whether a given credit card number is valid or not based on the Luhn's Algorithm.
        It also determines the vendor (VISA, MasterCard, AMEX, or INVALID) based on the number's length and range.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            ccnumber: int
                The credit card number to be checked.

        Returns:
            This function does Not return anything.
        """

        # TODO: Re-do algorithm, use regex maybe? https://www.informit.com/articles/article.aspx?p=1223879&seqNum=12

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
        elif cc_digits == 16 and (4e15 < ccnumber < 5e15):
            vendor = "VISA"
            loopCounter = 8
        elif cc_digits == 16 and (51e14 < ccnumber < 56e14):
            vendor = "MASTERCARD"
            loopCounter = 8
        elif cc_digits == 15 and ((34e13 < ccnumber < 35e13) or (37e13 < ccnumber < 38e13)):
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