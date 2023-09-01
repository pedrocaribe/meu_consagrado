# Import main modules
import discord
import random
import asyncio
import time
import difflib
import requests
import json

# Import secondary modules
from discord import app_commands
from discord.ext import commands
from googlesearch import search
from datetime import datetime
import translators as ts

# Import variables and standard functions from local file
from utils import *


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Add meeting command to create a voice channel and invite users specified after command

    @app_commands.command(name='pesquisa', description='Google Search. Uso: "Termo" qtDeLinks (de 1 a 10)')
    async def pesquisa(self, interaction: discord.Interaction, term: str, am: int):
        """A command to perform a Google search and display search results.

        This command searches Google for the specified term and displays a specified number of search results.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            term: str
                The search term.
            am: int
                The number of search results to display with maximum of 15.

        Returns:
            This function does Not return anything.
        """

        # Check if amount of links entered by user is more than 15
        if am > 15:

            # Reply to user informing max number of results
            await interaction.response.send_message(f'O número máximo de resultados é 15, **{random.choice(FRASE_MEIO)}**, segue abaixo os 15 resultados.')

        else:
            await interaction.response.send_message(f'Segue abaixo o que encontrei no Google **{random.choice(FRASE_MEIO)}**')

        # Perform search
        results = search(term, num_results=am)

        for counter, result in enumerate(results):
            if counter == am:
                break
            await interaction.followup.send(f'**Resultado {counter + 1} de {am}\n\n{result}**')

    @app_commands.command(name='translate',
                          description='Uso: LinguaDestino(Opcional - padrão PTBR). Acentuação importa.')
    async def translate(self, interaction: discord.Interaction, *, text: str, lang: str = 'pt'):
        """A command to translate text to the specified language.

        This command translates the provided text to the desired language using the translators API.
        The translator engine used is 'google'.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            text: str
                The text to be translated.
            lang: str [OPTIONAL]
                The destination language for translation. Defaults to 'pt'.

        Returns:
            This function does Not return anything.
        """

        embed = discord.Embed(
            title=f'Tradução:',
            description='',
            colour=discord.Color.purple())

        async with interaction.channel.typing():
            try:
                trans_text = ts.translate_text(
                    translator='google',
                    query_text=text,
                    to_language=lang
                )
            except (commands.CommandInvokeError, ts.server.TranslatorError):
                await interaction.response.send_message(f"A lingua `{lang}` não existe, "
                                                        f"**{random.choice(FRASE_MEIO)}**. Vamos tentar novamente?")

        embed.add_field(
            name='Frase Original:', 
            value=text, 
            inline=False
            )
        embed.add_field(
            name='Frase Traduzida:', 
            value=trans_text,
            inline=False
            )
        embed.add_field(
            name='Lingua Destino:', 
            value=f"{lang.upper()} : {LANGUAGES[lang]}",
            inline=False
            )
        
        await interaction.response.send_message(f'Ta na mão sua tradução **{random.choice(FRASE_MEIO)}**')
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='avatar', description='Nome de usuário opcional.')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """A command to display the avatar of a user.

        This command retrieves and displays the avatar of the specified user. If no user is provided,
        it displays the avatar of the user who invoked the command.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            member: discord.Member [OPTIONAL]
                The user whose avatar needs to be displayed. Defaults to None.

        Returns:
            This function does Not return anything.
        """

        # If user did not specify another user to retrieve the avatar from, retrieve his own avatar
        member = interaction.user if not member else member

        # If requested user does not have an avatar
        if not member.avatar:
            return await interaction.response.send_message(f'Esse usuário não tem um avatar.')
        
        url = member.avatar.url
        name = await self.bot.fetch_user(member.id)

        # Create embed to reply to user
        embed = discord.Embed(
            title='',
            description=''
        )
        embed.set_author(
            name=name,
            icon_url=url
        )
        embed.set_image(
            url=url
        )
        embed.set_footer(text=f'Solicitado por {interaction.user.name}')

        return await interaction.response.send_message(embed=embed)

    @app_commands.command(name='timer', description='Tempo em minutos. Ex.: 120 Lembrar de boostar o servidor!')
    async def timer(self, interaction: discord.Interaction, minutes: int, *, reason: str = None):
        """A command to set a timer for a specified number of minutes.

        This command sets a timer for the specified number of minutes and sends a reminder to the user after
        the timer expires. An optional reason can be provided for the timer.

        Args:
            interaction: discord.Interaction
                The interaction object representing the command invocation.
            minutes: int
                The duration of the timer in minutes.
            reason: str [OPTIONAL]
                The reason for setting the timer. Defaults to None.

        Returns:
            This function does Not return anything.
        """

        # Standard response
        resp = f'Ok, **{random.choice(FRASE_MEIO)}**, vou te lembrar em {minutes} minutos'

        # If a reason was given, append to response
        if reason:
            resp += f'de "__{reason}__".'
        await interaction.response.send_message(resp)

        # async sleep the request amount of minutes
        await asyncio.sleep(minutes * 60)

        # Let user know the timer is done
        new_resp = f'{interaction.user.mention} Apenas para te lembrar que o timer finalizou, **{random.choice(FRASE_MEIO)}**\n**Tempo decorrido**: {minutes} minutos.'

        # If a reason was given, append to response
        if reason:
            new_resp += f'\n**Descrição**: "{reason}".'

        # Send response to user
        await interaction.followup.send(new_resp)


    @app_commands.command(name='insulto', description='Ofenda a mãe dos seus colegas')
    async def insult(self, interaction: discord.Interaction, member: discord.Member):

        # Call external method to collect random insult from local file
        insult = await get_jokes()

        # Mention member
        await interaction. response.send_message(f'{member.mention}, {insult}')

        
    @app_commands.command(name='motivacional', description='Frase motivacional para boostar o ânimo!')
    async def timer(self, interaction: discord.Interaction):

        # TODO: Add timer tracker by user in order user wants to cancel the timer
        compliment = requests.get('https://complimentr.com/api').text
        compliment = json.loads(compliment)

        trans = ts.translate_text(translator='bing', query_text=compliment['compliment'], to_language='pt')
        await interaction.response.send_message(trans.capitalize())

    # @app_commands.command(name='pomodoro', description='Sistema pomodoro de estudos')
    # async def pomodoro(self, interaction: discord.Interaction, total: int, study: int, pause: int):

    #     if study > total or pause > total:
    #         return await interaction.response.send_message(f'Tempo inválido. Maior que o tempo total de estudo.')

    #     try:
    #         db = sqlite3.connect(STUDY_DB)
    #     except Exception as e:
    #         raise SystemError
        
    #     with db:
    #         cursor = db.cursor()

    #         validate = cursor.execute("SELECT * FROM study WHERE user_id = ? AND study = ?", (interaction.user.id, True))

    #         if validate:
    #             return await interaction.response.send_message(f'Você já está num estudo programado, **{random.choice(FRASE_MEIO)}**, pra configurar um novo estudo, execute o comando /pomodoro com a opção stop!')
            

    #     embed = discord.Embed(
    #         title=f'__MÉTODO POMODORO DE ESTUDOS__ - {datetime.now().strftime("%d/%m - %H:%M")} - TOTAL **__{total} MINUTOS__**',
    #         description=''
    #     )
    #     embed.set_footer(
    #         text = '\nO método Pomodoro é uma técnica de produtividade que envolve períodos de trabalho focado seguidos por pausas curtas e regulares.'
    #         )
    #     embed.add_field(
    #         name = f'Intervalo de estudo: `{study} min`', 
    #         value = '---'
    #         )
    #     embed.add_field(
    #         name = f'Intervalo de pausa: `{pause} min`', 
    #         value = '---'
    #         )

    #     # Create task
    #     coro = asyncio.sleep()
    #     task = await asyncio.create_task(name=interaction.user.name)

async def setup(bot):
    await bot.add_cog(General(bot))
