
# Import main modules
import discord, asyncio, pafy, random, requests, re, spotipy, yt_dlp

# Import secondary modules
from discord.ext import commands
from youtube_dl import YoutubeDL
from youtubesearchpython import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
from calendar import isleap
from discord.ui import Button, View
from spotipy.oauth2 import SpotifyClientCredentials

# Import variables and standard functions from local file
from var_Reuse import *


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.song_queue = []
        self.vc = None
        self.isPlaying = False
        self.current = ""

        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        # Bound to lines 38-42
        # self.setup()

        '''Commands defined in this cog are for music playing through a voice channel.
        It was designed to always use YouTube and FFMPEG, as no other APIs seem to work
        as expected.

        cog_Music v5.03'''

    # Create a Playlist for the Server the Bot is connected to
    # Not working somehow
    # def setup(self):
    #     for guild in self.bot.guilds:
    #         self.song_queue[guild.id] = []

    # Join Voice Channel
    async def join_(self, ctx):

        # If caller is not in a voice channel
        if ctx.author.voice is None:
            return await ctx.reply(f'Não deu pra entrar no canal de voz não, **{random.choice(fraseMeio)}**. Tenta entrar lá primeiro e me chama.')

        # If caller is in a voice channel
        else:

            # If bot is not already in a voice channel
            if self.vc == None:
                self.vc = await ctx.author.voice.channel.connect()
                return 0

            # If bot is already in a voice channel
            else:
                if ctx.author.voice.channel.id == ctx.voice_client.channel.id:
                    return 0
                return await ctx.reply(f'A banda já está tocando em outro canal de voz, **{random.choice(fraseMeio)}**.')

    # Checks the queue for songs, set Current, play and pop first item in Playlist
    async def check_queue_(self, ctx):

        # Boudn to lines 38-42
        # queue = self.song_queue[ctx.guild.id]

        queue = self.song_queue

        # If song in queue
        if len(queue) > 0:
            self.current = queue[0]
            await self.play_(ctx, queue[0])
            self.isPlaying = True
            await self.now(ctx)
            # queue.pop(0)

        # If no song in queue
        else:
            self.isPlaying = False

    # Recursive function to play songs
    async def play_(self, ctx, song):
        self.isPlaying = True
        try:
            url = pafy.new(song).getbestaudio().url

            # Bound to lines 38-42
            # self.song_queue[ctx.guild.id].pop(0)

            self.song_queue.pop(0)

        except Exception as e:
            ctx.voice_client.stop() # This is a test due to YouTube error for when video is rated for over 18 audience

            # await ctx.reply(f'{e}')
            if url == None: return
            pass
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)), after = lambda error: self.bot.loop.create_task(self.check_queue_(ctx)))
        ctx.voice_client.source.volume = 0.5

    # Add whole YouTube playlist to queue
    async def playlist_(self, ctx, pl):

        # Parse playlist and extract url for each videos in playlist
        pl_p = Playlist.getVideos(pl)

        # Variables
        counter = 0

        # Bound to lines 38-42
        # queue = self.song_queue[ctx.guild.id]
        queue = self.song_queue

        # Add URL's parsed to the queue
        for music in pl_p['videos']:
            if counter < 99:
                queue.append(music['link'].split('&', 1)[0])
                counter += 1
            else:
                break

        # Return counter to caller in order to inform how many songs were added to queue
        return counter

    async def list_(self, ctx, pl):

        ydl_opts = {'format': 'm4a/bestaudio/best', 'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a',}]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            pl_p = ydl.extract_info(pl, download = False)
            return pl_p['entries']
        

    # Parse Spotify playlist, search for songs in YouTube and extract URLs
    async def spotify_parse_playlist_(self, ctx, url):

        # Personal Client ID from Spotify API
        cid = "08d9e59cabea42c29b7c44e45e688693"

        # Personal Client Secret from Spotify API
        secret = "e96fa23c36664f46bacc02703c7dfc99"

        # Set IDs for usage with API
        client_credentials_manager = SpotifyClientCredentials(client_id=cid,client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        # Extract URI from url provided
        playlist_URI = url.split("/")[-1].split("?")[0]
        track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

        # List to be returned after parsign data
        data = []

        # Extract Song and Artist name for each track
        for track in sp.playlist_tracks(playlist_URI)["items"]:

            # Name
            track_name = track["track"]["name"]

            # Artist Name
            artist_uri = track["track"]["artists"][0]["name"]

            # Add to data list combining both information and adding - in between them
            data += [track_name + ' - ' + artist_uri]

        # Return data to caller
        return data

    # Stop playing and Leave Voice Channel
    async def stopLeave_(self, ctx):
        if self.vc != None:
            self.vc.stop()
            self.isPlaying = False
            self.vc = None
            self.song_queue.clear()
            await ctx.voice_client.disconnect()
            return await self.ads_(ctx)
        else:
            try:
                await ctx.voice_client.disconnect()
                return await self.ads_(ctx)
            except:
                pass
            return await ctx.reply(f'Mas eu não estou nem tocando, **{random.choice(fraseMeio)}**..')

    # Show queue to user
    async def queue_(self, ctx):

        # Bound to lines 38-42
        # # If no songs in queue and not currently playing
        # if len(self.song_queue[ctx.guild.id]) == 0 and not self.isPlaying: return await ctx.reply(f'Não tem nenhuma música na lista, **{random.choice(fraseMeio)}**.')
        # # If playing song and no other songs in queue
        # elif len(self.song_queue[ctx.guild.id]) == 0 and self.isPlaying:

        # If no songs in queue and not currently playing
        if len(self.song_queue) == 0 and not self.isPlaying: return await ctx.reply(f'Não tem nenhuma música na lista, **{random.choice(fraseMeio)}**.')
        # If playing song and no other songs in queue
        elif len(self.song_queue) == 0 and self.isPlaying:
            await ctx.reply(f'Só tem a música que está tocando na lista. Da uma olhadinha:')
            return await self.now(ctx)
        # Else
        embed = discord.Embed(title = ':notes: Lista de músicas do momento:', description = "", colour = discord.Color.dark_gold())
        i = 1

        # Bound to lines 38-42
        # for music in self.song_queue[ctx.guild.id]:
        for music in self.song_queue:
            actual = await self.musicInfo_(music)

            title = actual[0]

            if len(str(embed)) < 5800 and len(embed.description) < 4000:
                embed.description += f'{i}) {title}\n'
                i += 1
            else:
                embed.description += f'{i}) [...]\n'
                break

        embed.set_footer(text = f'\nProntinho, {random.choice(fraseMeio)}. Da uma olhada na lista.')
        return await ctx.reply(embed = embed)

    # Search for songs in YouTube if no url was passed
    async def search_(self, amount, song, get_url=False):

        # Loop until YoutubeDL returns the expected amount of links
        info = await self.bot.loop.run_in_executor(None, lambda: YoutubeDL({"format": "bestaudio/best", "quiet": True, "noplaylist": True}).extract_info(f'ytsearch{amount}:{song}', download = False, ie_key = 'YoutubeSearch'))

        # If nothing found, return
        if len(info['entries']) == 0 : return None

        # If results were found, return the URLs for parsing or the whole list
        return [entry['webpage_url'] for entry in info['entries']] if get_url else [entry['webpage_url'] for entry in info['entries']] if get_url else [[entry['webpage_url'], entry['title'], entry['thumbnails'][0]['url']] for entry in info['entries']]

    # Credits after leaving channel
    async def ads_(self, ctx):

        linkedIn = Button(label = 'LinkedIn', style = discord.ButtonStyle.green, url = 'https://www.linkedin.com/in/pedro-caribe/')
        gitHub = Button(label = 'GitHub', style = discord.ButtonStyle.green, url = 'https://github.com/pedrocaribe')

        view = View()
        view.add_item(linkedIn)
        view.add_item(gitHub)
        embed = discord.Embed(title = '**Desconectado**', description = 'Curtiu o bot? Manda uma alô pro criador:\n\nAté a próxima!', colour = discord.Color.greyple())
        embed.set_thumbnail(url = 'https://media-exp1.licdn.com/dms/image/C4D03AQEHnP7Kmm-rbg/profile-displayphoto-shrink_800_800/0/1659108850478?e=1669248000&v=beta&t=SbVf8jeQEe_mDXQeoKd_swUCbcB-F36uuQcqTaALq7g')

        return await ctx.send(embed = embed, view = view)

    # Extract info from Video
    async def musicInfo_(self, url):
        music = Video.getInfo(url)
        thumb = music['thumbnails'][0]['url']
        title = music['title']

        # Returns a tuple [0] and [1] values
        return title, thumb

    # Monitor for playing activity and quit if not playing for 180s
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Ignore if change from Voice Channels was not from bot
        if not member.id == self.bot.user.id: return

        # Ignore if change from Voice Channels was triggered by disconnect() (LINE 89)
        elif before.channel is not None: return

        # Check if playing when IN Voice Channel, every 180 seconds
        else:
            voice = after.channel.guild.voice_client
            while True:
                await asyncio.sleep(180)
                # await asyncio.sleep(600) #for testing purposes, change back afterwards

                # If not playing, disconnect
                if voice.is_playing() == False:
                    self.isPlaying = False
                    await voice.disconnect()
                    self.vc = None
                    break

    # On command 'pause'
    @commands.command(name = 'pause', aliases = ['pausar'])
    async def pause(self, ctx):

        # If Playing, then pause
        if self.isPlaying:
            self.vc.pause()
            self.isPlaying = False

        # If not playing, then resume
        else:
            self.vc.resume()
            self.isPlaying = True

    # On command 'resume'
    @commands.command(name = 'resume', aliases = ['continuar', 'despausar', 'despause', 'r'])
    async def resume(self, ctx):

        # If not in Voice Channel
        if self.vc == None: return await ctx.reply(f'Mas eu não estou nem tocando, **{random.choice(fraseMeio)}**..')

        # If in Voice Channel and NOT playing, resume
        elif not self.isPlaying: return self.vc.resume()

        # If in Voice Channel, and playing
        return await ctx.reply(f'A música não tá pausada, **{random.choice(fraseMeio)}**. Pra pausar é só mandar um `%pause` ou `%p`.')

    # On command 'stop'
    @commands.command(name = 'stop', aliases = ['parar', 's', 'leave', 'l', 'q'])
    async def stop(self, ctx):
        await self.stopLeave_(ctx)

    # On command 'nowplaying'
    @commands.command(name = 'tocando', aliases = ['now', 'nowplaying', 'agora', 'playing'])
    async def now(self, ctx):

        if not self.isPlaying: return await ctx.reply(f'Não estamos com serviço couvert hoje, **{random.choice(fraseMeio)}**. Obrigado.')

        # Create embedded message containing Title and Thumbnail
        music = await self.musicInfo_(self.current)
        embed = discord.Embed(title = ':notes: Tocando agora:', description = f'[{music[0]}]({self.current})', colour = discord.Colour.green())
        embed.set_thumbnail(url = music[1])

        # Reply to user
        await ctx.send(embed = embed)

    # On command 'criador'
    @commands.command(name = 'criador', aliases = ['owner', 'dono', 'creator'])
    async def creator(self, ctx):
        return await self.ads_(ctx)

    # On command 'search'
    @commands.command(name = 'procurar_musica', aliases = ['music_search', 'buscar_musica', 'musica'])
    async def music_search(self, ctx, *, song=None):

        # If no song names were given during command
        if song is None: return await ctx.reply('Esqueceu de falar o nome da música, **meu Idoso**?')

        # Else, look for 5 results of the song name
        await ctx.reply(f'Pesquisando...')
        search_result = await self.search_(5, song)

        i = 1
        embed = discord.Embed(title = f'Resultado da pesquisa por "{song}":', description = "Você pode utilizar essas URL's para tocar uma música, usando a sintaxe `%play URL` \n", colour = discord.Colour.blurple())

        buttons = []

        for music in search_result:
            embed.add_field(name = f'{i}) {music[1]}', value = f'{music[0]}', inline = False)
            # buttons.append(Button(label = f'{i}', style = discord.ButtonStyle.blurple, url =
            i += 1

        embed.set_footer(text = f'Mostrando os 5 primeiros resultados na Web')
        await ctx.reply(embed = embed)

    # On command 'queue'
    @commands.command(name = 'queue', aliases = ['fila', 'f'])
    async def queue(self, ctx):
        await ctx.reply(f'Segura aí só uma minutinho enquanto eu processo a lista, **{random.choice(fraseMeio)}**.\nSe a lista estiver muito cheia, pode demorar um pouco pra eu te responder.')
        # Removed due to context not having trigger typing attribute
        # await ctx.trigger_typing()
        async with ctx.message.channel.typing():
            await self.queue_(ctx)

    # On command 'skip'
    @commands.command(name = 'skip', aliases = ['pular', 'next', 'n'])
    async def skip_(self, ctx, *qty):

        # If bot is not in a Voice Channel
        if ctx.voice_client is None: return await ctx.reply(f'Não estamos com serviço couvert hoje. Obrigado.')

        # If caller is not in a Voice Channel
        if ctx.author.voice is None: return await ctx.reply(f'Entra num canal de voz primeiro, e me chama de lá, **{random.choice(fraseMeio)}**.')

        # If caller's Voice Channel is different from the Bot's
        if ctx.author.voice.channel.id != ctx.voice_client.channel.id: return await ctx.reply(f'A banda já está tocando em outro canal de voz, **{random.choice(fraseMeio)}**, vamos ter que aguardar ela finalizar lá, ou utilizar outro bot no meio tempo.')

        # If no more music in queue

        # Bound to lines 38-42
        #  if not self.song_queue[ctx.guild.id][0] or not self.song_queue[ctx.guild.id]: return await ctx.reply(f'Não tem mais música na lista. Se quiser parar completamente a música, manda um `%stop` ou `%parar`')
        if not self.song_queue[0] or not self.song_queue: return await ctx.reply(f'Não tem mais música na lista. Se quiser parar completamente a música, manda um `%stop` ou `%parar`')
        # If caller is in the same Voice Channel as the Bot and there are other songs in queue
        # If a quantity to be skipped was given, delete from beggining to end the amount of elements
        if qty and int(qty[0]) >= 1:

            # Bound to lines 38-42
            # self.song_queue[ctx.guild.id] = self.song_queue[ctx.guild.id][(int(qty[0]) - 1):]
            self.song_queue = self.song_queue[(int(qty[0]) - 1):]
        ctx.voice_client.stop()

    # On command 'play'
    @commands.command(name = 'play', aliases = ['p', 'tocar'])
    async def play(self, ctx, *, url = None):

        try:
            
            if url is None and self.song_queue != None and self.isPlaying == False:
                self.isPlaying = True
                await self.play_(ctx, self.song_queue[0])
                return self.song_queue.pop(0)
                

            # If no url was inputted from user
            if url is None: return await ctx.reply(f'Tem que colocar uma música aí né, **{random.choice(fraseMeio)}**!')

            # Join Voice Channel, if not successful, return
            if self.vc == None:
                joinChannel = await self.join_(ctx)
                if joinChannel != 0: return

            songs = []

            queue = self.song_queue
            q_len = len(queue)

            # If spotify, search and play from youtube
            if 'spotify' in url:
                if 'playlist' in url:
                    await ctx.reply(f'Isso aí é uma playlist né, **{random.choice(fraseMeio)}**? Analisando músicas!')
                    async with ctx.message.channel.typing():
                        song_names_array = await self.spotify_parse_playlist_(ctx, url)
                        counter = 0

                    async with ctx.message.channel.typing():
                        for song in song_names_array:
                            result = await self.search_(1, f'music {song}', get_url = True)

                            if result is None:
                                await ctx.send(f'Não rolou de adicionar a música {song} . Parece que o formato ta errado ou a música não existe. Tenta uma palavra diferente?')
                                # break
                            else:
                                url = result[0]
                                queue.append(url)
                                counter += 1

                    await ctx.reply(f'Adicionei {counter} músicas na playlist.')
                    if self.isPlaying: return
                    await ctx.send(f'Tocando: {queue[0]}')

                    # # NEW WAY v
                    # return await self.play_(ctx, queue[0])

                    # OLD WAY v
                    await self.play_(ctx, queue[0])
                    return queue.pop(0)


            # If not a link from youtube, search
            elif not ('youtube.com' in url or 'youtu.be' in url):
                await ctx.send(f'Vou procurar sua música aqui na lista de CDs que o patrão deixou. Segura aí que vai demorar uns segundinhos, **{random.choice(fraseMeio)}**.')

                async with ctx.message.channel.typing():
                    result = await self.search_(1, url, get_url = True)

                if result is None: return ctx.reply('Não rolou de baixar essa música. Parece que o formato ta errado ou a música não existe. Tenta uma palavra diferente?')

                url = result[0]

            # If playlist, add all songs
            elif 'playlist?' in url:
                await ctx.reply(f'Isso aí é uma playlist né, **{random.choice(fraseMeio)}**? Adicionando!')

                async with ctx.message.channel.typing():
                    counter = await self.playlist_(ctx, url)

                await ctx.reply(f'Adicionei {counter} músicas na playlist.')

                if self.isPlaying: return
                await ctx.send(f'Tocando: {queue[0]}')

                # NEW WAY v
                return await self.play_(ctx, queue[0])

                # OLD WAY v
                # await self.play_(ctx, queue[0])
                # return queue.pop(0)
            
            elif 'list=' in url:
                await ctx.reply(f'Isso aí é um mix do YouTube né, **{random.choice(fraseMeio)}**? Adicionando!')

                async with ctx.message.channel.typing():
                    counter = await self.list_(ctx, url)

                await ctx.reply(f'Adicionei {counter} músicas na playlist.')

                if self.isPlaying: return
                await ctx.send(f'Tocando: {queue[0]}')

                return await self.play_(ctx, queue[0])
                
        except Exception as e:
            await ctx.reply(f'{e}')
            return await ctx.reply(f'Não consegui processar nenhuma música ou playlist a partir desse link, **{random.choice(fraseMeio)}**, boa tentar outra? Usa o comando `%search Nome Da Musica`.')

        if not ctx.voice_client.source == None:
            queue.append(url)
            return await ctx.reply(f'Música adicionada à lista na posição {q_len + 1}. Essa é braba!')

        await self.play_(ctx, url)
        self.isPlaying = True # Added as an experiment
        self.current = url
        await ctx.send(f'Tocando: {url}')

# Define setup function for Cog according to recent changes (//https://gist.github.com/Rapptz/6706e1c8f23ac27c98cee4dd985c8120//)

async def setup(bot):
    await bot.add_cog(Player(bot))