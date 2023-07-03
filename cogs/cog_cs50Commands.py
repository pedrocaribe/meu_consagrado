# Import main modules
import discord, random

# Import secondary modules
from discord.ext import commands
from math import floor

# Import variables and standard functions from local file
from var_Reuse import *


# Define class
class Cs50(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        '''Commands defined in this cog are for demonstration purpose of projects
        completed throughout cs50x course.

        cog_cs50Commands v2.09'''


    # Mario Less function
    @commands.command(name='mario-less', help='Projeto criado durante Week 1/pset1 do curso CS50\n\n Uso: %mario-less QtDeAndares (de 1 a 8)')
    async def marioLess(self, ctx, bricks: int):

        # Check if user inputted value between 1 and 8
        if bricks < 1 or bricks > 8 or bricks == None:
            await ctx.reply(f'Quantidade deve ser de 1 a 8, {random.choice(fraseMeio)}')
        else:

            # Send bricks increasing per message
            for i in range(bricks):
                j = (bricks - i) - 1
                await ctx.send('...' * j + '#' * (i + 1))


    # Mario More function
    @commands.command(name='mario-more', help='Uso: Projeto criado durante Week 1/pset1 do curso CS50\n\nUso: %mario-more QtDeAndares (de 1 a 9)')
    async def marioMore(self, ctx, bricks: int):

        # Check if user inputted value between 1 and 8
        if bricks < 1 or bricks > 8 or bricks == None:
            await ctx.reply(f'Quantidade deve ser de 1 a 8, {random.choice(fraseMeio)}')
        else:

            # Send bricks increasing per message
            for i in range(bricks):
                j = (bricks - i) - 1
                await ctx.send(('...' * j) + ('#' * (i + 1)) + ' ' + ('#' * (i + 1)))


    # Command to check if credit card number is valid according to Luhn's Algorithm
    @commands.command(name='cccheck', aliases=['cc', 'ccvalidation', 'cc_check'], help='Uso: Projeto criado durante Week 1/pset1 do curso CS50\n\nUso: %cccheck 1234123412341324')
    async def cccheck(self, ctx, ccnumber: int):

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
            return await ctx.reply(f'Número de cartão de crédito válido! Bandeira: **{vendor}**')
        else:
            return await ctx.reply(f'Número de cartão de crédito **inválido**!')

# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(Cs50(bot))

