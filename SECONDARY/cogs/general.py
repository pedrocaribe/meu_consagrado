# Import main modules
import discord, random, asyncio, time, difflib, requests, json

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

    '''Commands defined in this cog are general purpose commands
    mostly fun and useful commands for users to enjoy
    
    v1.0'''

    @app_commands.command(name='pesquisa', description='Google Search. Uso: "Termo" qtDeLinks (de 1 a 10)')
    async def pesquisa(self, interaction: discord.Interaction, term: str, am: int):

        # Check if amount of links entered by user is more than 15
        if am > 15:

            # Reply to user informing max number of results
            await interaction.response.send_message(f'O número máximo de resultados é 15, **{random.choice(FRASE_MEIO)}**, segue abaixo os 15 resultados.')

        else:

            # Reply to user informing the next messages will be regarding their search
            await interaction.response.send_message(f'Segue abaixo o que encontrei no Google **{random.choice(FRASE_MEIO)}**')

        # Perform search
        results = search(term, num_results=am)

        counter = 0
        for result in results:
            if counter == am:
                break
            counter += 1
            await interaction.followup.send(f'**Resultado {counter} de {am}\n\n{result}**')

    @app_commands.command(name='translate', description='Uso: Sua Frase Aqui // LinguaDestino(Opcional - padrão PTBR). Acentuação importa.')
    async def translate(self, interaction: discord.Interaction, *, text:str, lang: str = 'pt'):

        # Usage of translator api to translate portions of text to desired language

        embed = discord.Embed(
            title=f'Tradução:', description='', colour=discord.Color.purple()
            )
        async with interaction.channel.typing():
            transText = ts.translate_text(
                translator='google', 
                query_text=text, 
                to_language=lang
                )

        embed.add_field(
            name='Frase Original:', 
            value=text, 
            inline=False
            )
        embed.add_field(
            name='Frase Traduzida:', 
            value=transText, 
            inline=False
            )
        embed.add_field(
            name='Lingua Destino:', 
            value=lang.upper(), 
            inline=False
            )
        
        await interaction.response.send_message(f'Ta na mão sua tradução **{random.choice(FRASE_MEIO)}**')
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='avatar', description='Nome de usuário opcional.')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        
        # If user did not specify another user to treieve the avatar from, retrieve his own avatar
        if member == None:
            member = interaction.user

        # If requested user does not have an avatar
        if member.avatar.url == None:
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

        # Standard response
        resp = (f'Ok, **{random.choice(FRASE_MEIO)}**, vou te lembrar em {minutes} minutos')

        # If a reason was given, append to response
        if reason != None:
            resp += f'de "__{reason}__".'
        await interaction.response.send_message(resp)

        # async sleep the request amount of minutes
        await asyncio.sleep(minutes * 60)

        # Let user know the timer is done
        new_resp = f'{interaction.user.mention} Apenas para te lembrar que o timer finalizou, **{random.choice(FRASE_MEIO)}**\n**Tempo decorrido**: {minutes} minutos.'

        # If a reason was given, append to response
        if reason != None:
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
