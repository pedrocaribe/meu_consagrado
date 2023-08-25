# Import main modules
import discord, random, sqlite3, asyncio

# Import secondary modules
from discord.ext import commands, tasks
from math import floor
from datetime import datetime

# Import variables and standard functions from local file
from var_Reuse import *

# Start SQL DB
db = sqlite3.connect('database.db')
cursor = db.cursor()

# Define class
class gameEngine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.passive_health.start()
        self.passive_mana.start()

        '''Commands defined in this cog are for playing a MMORPG created to have fun under discord server.

        cog_Game v2.00'''

    # Define group of commands
    @commands.group()
    async def game(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply('Dúvidas? Tenta `%help game`')

    @game.command(name = 'registrar', aliases = ['register'], help = 'Comando utilizado se registrar no MMORPG. Todas as informações solicitadas são necessárias.')
    async def register(self, ctx):

        # Trigger typing decorator
        async with ctx.message.channel.typing():  

            user_id = ctx.author.id
            username = ctx.author.name
            date = datetime.today().strftime('%Y-%m-%d')

            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            player = cursor.fetchone()

            if player:
                await ctx.reply(f'Você já está registrado, **{random.choice(fraseMeio)}**!')

            else:
                cursor.execute("INSERT INTO players (user_id, username, exp, level, health, mana, joined) VALUES (?, ?, 100, 1, 100, 100, ?)", (user_id, username, date))
                db.commit()
                cursor.execute("INSERT INTO backpack (user_id) VALUES (?)", (user_id,))
                db.commit()

                await ctx.reply(f'Jogador registrado com sucesso, **{random.choice(fraseMeio)}**!')

    @game.command(name = 'perfil', aliases = ['profile'], help = 'Comando utilizado para visualizar o perfil de um dos jogadores.')
    async def profile(self, ctx, player : discord.Member = None):

        # Trigger typing decorator
        async with ctx.message.channel.typing():

            # If user did not specify another user to retrieve the profile from, retrieve his own profile
            if player == None:
                player = ctx.message.author

            user_id = player.id
            username = player.name

            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            player = cursor.fetchone()


            if player:
                await ctx.reply(f'Nome: {player[2]}\nLevel: {player[4]}\nEXP: {player[3]}\nJogando Desde: {player[9]}')

            else:
                await ctx.reply(f'Jogador não , **{random.choice(fraseMeio)}**!')
    
    @game.command(name = 'atacar', aliases = ['attack', 'ataque'], help = 'Comando utilizado para atacar outros jogadores, podendo enviá-lo para a UTI e aproveitar de seus itens')
    async def attack(self, ctx, target : discord.Member):

        # Trigger typing decorator
        async with ctx.message.channel.typing():

            attacker_id = ctx.author.id
            cursor = db.cursor()
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (attacker_id,))
            attacker = cursor.fetchone()

            target_id = target.id
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (target_id,))
            target_player = cursor.fetchone()

            if not target_player:
                return await ctx.reply(f'Jogador alvo não encontrado, **{random.choice(fraseMeio)}**')
            elif target_id == attacker_id:
                return await ctx.reply(f'Você não pode atacar a si mesmo, **{random.choice(fraseMeio)}**!')
            elif target_player[8] == True:
                return await ctx.reply(f'Jogador alvo está em recuperação na **UTI**!')

            attacker_damage = random.randint(5, 10) * attacker[4]
            attacker_exp = attacker[3]
            target_health = target_player[5]
            new_level = attacker[4]

            target_health -= attacker_damage

            if target_health < 0: target_health = 0

            cursor.execute("UPDATE players SET health = ? WHERE user_id = ?", (target_health, target_id))
            db.commit()
            
            if target_health <= 0:
                cursor.execute("UPDATE players SET uti = ? WHERE user_id = ?", (True, target_id))
                db.commit()

                await ctx.reply(f'{target.mention} foi enviado para a **UTI**!')
                attacker_exp += 20
                
                await asyncio.sleep(5 * 60)
                cursor.execute("UPDATE players SET uti = ? WHERE user_id = ?", (False, target_id))
                db.commit()

            else:
                await ctx.reply(f'{target.mention} foi atacado, o dano causado foi {attacker_damage} e a vida atual do alvo é {target_health}!')
                attacker_exp += random.randint(5, 10) * 2
            
            if attacker_exp > (attacker[4] * 100) + 1:
                new_level = attacker[4] + 1

            cursor.execute("UPDATE players SET exp = ?, level = ? WHERE user_id = ?", (attacker_exp, new_level, attacker_id))
            db.commit()
            
    @tasks.loop(seconds=6)
    async def passive_health(self):
        cursor.execute("SELECT * FROM players")
        all_players = cursor.fetchall()
        for each_player in all_players:
            
            max_health = 100 + each_player[4] * 10
            cursor.execute("UPDATE players SET max_health = ? WHERE id = ?", (max_health, each_player[0]))
            db.commit()

            if each_player[5] >= max_health:
                cursor.execute("UPDATE players SET uti = ? WHERE id = ?", (False, each_player[0]))
                db.commit()
                continue
            
            if each_player[10] == True and each_player[5] < max_health / 2:
                cursor.execute("UPDATE players SET health = ? WHERE id = ?", (each_player[5] + 2, each_player[0]))
                db.commit()
                continue
            else:    
                cursor.execute("UPDATE players SET health = ?, uti = ? WHERE id = ?", (each_player[5] + 1, False, each_player[0]))
                db.commit()
                continue

    @tasks.loop(seconds=12)
    async def passive_mana(self):
        cursor.execute("SELECT * FROM players")
        all_players = cursor.fetchall()
        for each_player in all_players:

            max_mana = 100 + each_player[4] * 20
            cursor.execute("UPDATE players SET max_mana = ? WHERE id = ?", (max_mana, each_player[0]))
            db.commit()
            
            if each_player[7] >= max_mana:
                continue
            
            else:
                cursor.execute("UPDATE players SET mana = ? WHERE id = ?", (each_player[7], each_player[0]))
                db.commit()
                

async def setup(bot):
    await bot.add_cog(gameEngine(bot))


# IDEIAS

# Conforme a quantidade de minutos gastos em call estudando, sao somados pontos ao usuario.
# O acumulo de pontos da direito a regalias como alterar cor do nick.

# Pausa para descanso de estudo, tempo personalizavel.
# Alerta para voltar aos estudos.