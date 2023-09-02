# Import main modules
import discord
import asyncio
import pafy
import random
import requests
import re
import spotipy

# Import secondary modules
from discord import app_commands
from discord.ext import commands
from youtube_dl import YoutubeDL
from youtubesearchpython import *
from urllib.request import urlopen
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ui import Button, View

# Import variables and standard functions from local file
from utils import *


# TODO: Add artist to now playing

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing_guilds = {}  # dict of Play objects representing guilds playing -> guild_id : object

    class Play:
        def __init__(self, interaction: discord.Interaction, bot):
            self.bot = bot
            self.song_queue = []
            self.vc = None
            self.isPlaying = False
            self.current = ""
            self.FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
            }

        async def join_(self, interaction: discord.Interaction):

            # If user is not in Voice Channel
            if interaction.user.voice is None:
                return await interaction.response.send_message(
                    f'Não deu pra entrar no canal de voz não, **{random.choice(FRASE_MEIO)}**. '
                    f'Tenta entrar lá primeiro e me chama.')

            else:
                # If bot is not already in a voice channel within that server
                if not self.vc:
                    self.vc = await interaction.user.voice.channel.connect()
                    return 0

                # If bot is already in a voice channel within that server
                else:
                    if interaction.user.voice.channel.id == self.vc.channel.id:  # if same channel as user, do nothing
                        return 0
                    return await interaction.response.send_message(
                        f'A banda já está tocando em outro canal de voz, **{random.choice(FRASE_MEIO)}**.')

        async def play_(self, interaction: discord.Interaction, song: str):
            self.isPlaying = True
            try:
                url = pafy.new(song).getbestaudio().url
                self.song_queue.pop(0)
            except Exception as e:
                self.vc.stop()  # This is due to YouTube error for when a video is rated for over 18 audience
            else:
                if not url:
                    return
                pass
                self.vc.play(
                    discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)),
                    after=lambda error: self.bot.loop.create_task(self.check_queue(interaction)))
                self.vc.source.volume = 0.5

        async def check_queue(self, interaction: discord.Interaction):
            queue = self.song_queue

            # If song in queue
            if len(self.song_queue) > 0:
                self.current = queue[0]
                await self.play_(interaction, queue[0])
                self.isPlaying = True
                await self.now_(interaction)

            # If no song in queue
            else:
                self.isPlaying = False

        async def now_(self, interaction: discord.Interaction):

            # TODO: Test if channel_name actually works

            if not self.isPlaying:
                return await interaction.response.send_message(
                    f'Não estamos com serviço couvert hoje, **{random.choice(FRASE_MEIO)}**. Obrigado.')

            # Create embedded message containing Title and Thumbnail
            music = await self.music_info_(self.current)
            embed = discord.Embed(
                title=':notes: Tocando agora:',
                description=f'[{music[0]}]({self.current})',
                colour=discord.Colour.green()
            )
            embed.add_field(name="Artista", value=music[2])

            # Reply to user
            await interaction.response.send_message(embed=embed)

        async def music_info_(self, url: str):
            music = Video.getInfo(url)
            thumb = music['thumbnails'][0]['url']
            title = music['title']
            channel_name = music['channel']['name']

            # Returns a tuple [0] and [1] values
            return title, thumb, channel_name

        async def playlist_(self, interaction: discord.Interaction, pl: str):

            # Parse playlist and extract url for each video in playlist
            pl_p = Playlist.getVideos(pl)

            # Variables
            counter = 0

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

        async def spotify_parse_playlist_(self, interaction: discord.Interaction, url: str):

            cid = SPOTIFY_CID

            # Personal Client Secret from Spotify API
            secret = SPOTIFY_SECRET

            # Set IDs for usage with API
            client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            # Extract URI from url provided
            playlist_URI = url.split("/")[-1].split("?")[0]
            track_uris = [x["track"] for x in sp.playlist_tracks(playlist_URI)["items"]]

            # List to be returned after parsign data
            data = []

            # Extract Song and Artist name for each track
            for track in track_uris:
                track_name = track["name"]  # Name
                artist_uri = track["artists"][0]["name"]  # Artist Name

                # Add to data list combining both information and adding - in between them
                data += [track_name + ' - ' + artist_uri]

            # Return data to caller
            return data

        async def stop_leave_(self, interaction: discord.Interaction):
            if self.vc:
                self.vc.stop()
                self.isPlaying = False
                await self.vc.disconnect()
                self.vc = None
                self.song_queue.clear()
                return await self.ads_(interaction)
            else:
                try:
                    await self.vc.disconnect()
                    return await self.ads_(interaction)
                except:
                    pass
                return await interaction.response.send_message(
                    f"Mas eu não estou nem tocando, **{random.choice(FRASE_MEIO)}**..."
                )

        async def ads_(self, interaction):
            linkedin = Button(
                label="LinkedIn",
                style=discord.ButtonStyle.green,
                url="https://www.linkedin.com/in/pedro-caribe/")
            github = Button(
                label="GitHub",
                style=discord.ButtonStyle.green,
                url="https://github.com/pedrocaribe")

            view = View()
            view.add_item(linkedin)
            view.add_item(github)
            e = discord.Embed(
                title="**Desconectado**",
                description="Curtiu o bot? Manda uma alô pro criador:\n\nAté a próxima!",
                colour=discord.Color.green())

            thumb, e = await icon("profile", e)
            return await interaction.response.send_message(embed=e, file=thumb, view=view)


        async def pause_(self):
            ...

        async def stop_(self):
            ...

        async def skip_(self):
            ...

        async def queue_(self):
            ...

        async def search_(self):
            ...


    @app_commands.command(name='play', description='Tocar musicas')
    async def play(self, interaction: discord.Interaction, *, url: str = None):
        guild_id = interaction.guild_id

        if not guild_id in self.playing_guilds:
            self.playing_guilds[guild_id] = Player.Play(interaction, self.bot)
        player = self.playing_guilds[guild_id]
        
        # If user didn't provide URL, but there is a song queue, means player is paused
        if url is None and len(player.song_queue) != 0 and player.isPlaying == False:
            player.isPlaying = True
            await player.play_(interaction, player.song_queue[0])
            return player.song_queue.pop(0)
        
        # Else, if there isn't a queue, and user didn't provide URL
        if url is None: return await interaction.response.send_message(f'Tem que colocar uma música aí né, **{random.choice(FRASE_MEIO)}**!')

        join_channel = await player.join_(interaction)
        if join_channel != 0: return

    @app_commands.command(name="stop", description="Parar musicas e desconectar do canal de voz")
    async def stop(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        player = self.playing_guilds[guild_id]
        try:
            await player.stop_leave_(interaction)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Player(bot))