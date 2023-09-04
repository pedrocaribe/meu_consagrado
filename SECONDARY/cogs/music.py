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

@app_commands.guild_only()
class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing_guilds = {}  # dict of Play objects representing guilds playing -> guild_id : object

    class Play:
        def __init__(self, interaction: discord.Interaction, bot):
            self.bot = bot
            self.song_queue = []
            self.vc = None
            # self.isPlaying = False
            self.current = ""
            self.FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
            }

        async def join_(self, interaction: discord.Interaction):
            """Join Voice Channel

            This method checks if the user is in a Voice Channel, if the Bot is already connected
            to a Voice Channel within that guild, and if the Bot is already connected, it checks if
            the user's connected Voice Channel is the same as the Bot's connected Voice Channel.

            Parameters:
                interaction: discord.Interaction
                    The interaction object representing the command invocation.

            Returns:
                Bool:
                    True if Error joining
                    False if No Error joining
            """

            # If user is not in Voice Channel
            if interaction.user.voice is None:
                await interaction.response.send_message(
                    f'Não deu pra entrar no canal de voz não, **{random.choice(FRASE_MEIO)}**. '
                    f'Tenta entrar lá primeiro e me chama.')
                return True

            else:
                # If bot is not already in a voice channel within that server
                if not self.vc:
                    self.vc = await interaction.user.voice.channel.connect()
                    return False

                # If bot is already in a voice channel within that server
                else:
                    if interaction.user.voice.channel.id == self.vc.channel.id:  # if same channel as user, do nothing
                        return False
                    await interaction.response.send_message(
                        f'A banda já está tocando em outro canal de voz, **{random.choice(FRASE_MEIO)}**.')
                    return True

        async def play_(self, interaction: discord.Interaction, song: str):
            try:
                url = pafy.new(song).getbestaudio().url
                if len(self.song_queue) >= 1:
                    self.song_queue.pop(0)
            except Exception as e:
                print(e)
                self.vc.stop()  # This is due to YouTube error for when a video is rated for over 18 audience
                pass
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
                await self.now_(interaction)

            # If no song in queue
            else:
                return

        async def now_(self, interaction: discord.Interaction):

            if not self.vc.is_playing():
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
            try:
                await interaction.response.send_message(embed=embed)
            except discord.InteractionResponded:
                await interaction.followup.send(embed=embed)

        async def music_info_(self, url: str):
            music = Video.getInfo(url)
            thumb = music['thumbnails'][0]['url']
            title = music['title']
            channel_name = music['channel']['name']

            # Returns a tuple [0] and [1] values
            return title, thumb, channel_name

        async def youtube_playlist_(self, interaction: discord.Interaction, pl: str):

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

        async def spotify_parse_(self, interaction: discord.Interaction, url: str, playlist: bool = True):

            cid = SPOTIFY_CID

            # Personal Client Secret from Spotify API
            secret = SPOTIFY_SECRET

            # Set IDs for usage with API
            client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            # List to be returned after parsing data
            data = []

            if playlist:
                # Extract URI from url provided
                playlist_URI = url.split("/")[-1].split("?")[0]
                track_uris = [x["track"] for x in sp.playlist_tracks(playlist_URI)["items"]]

                # Extract Song and Artist name for each track
                for track in track_uris:
                    track_name = track["name"]  # Track Name
                    artist = track["artists"][0]["name"]  # Artist Name

                    # Add to data list combining both information and adding - in between them
                    data += [track_name + " - " + artist]
            else:
                track_uri = url.split("/")[-1].split("?")[0]
                track = sp.track(track_uri)
                track_name = track["name"]  # Track Name
                artist = track["artists"][0]["name"]
                data += [track_name + " - " + artist]

            # Return data to caller
            return data

        async def stop_leave_(self, interaction: discord.Interaction):
            if self.vc:
                self.vc.stop()
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
                    f"Mas eu não estou nem tocando, **{random.choice(FRASE_MEIO)}**...")

        async def ads_(self, interaction: discord.Interaction):
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

        async def skip_(self, interaction: discord.Interaction, qty: int = 1):
            # If bot is not in a Voice Channel
            if not self.vc:
                return await interaction.response.send_message(f"Não estamos com serviço couvert hoje. Obrigado.")
            # If caller is not in a Voice Channel
            if interaction.user.voice is None:
                return await interaction.response.send_message(f"Entra num canal de voz primeiro, e me chama de lá, "
                                                               f"**{random.choice(FRASE_MEIO)}**.")
            # If caller's Voice Channel is different from the Bot's
            if interaction.user.voice.channel.id != self.vc.channel.id:
                return await interaction.response.send_message(f"A banda já está tocando em outro canal de voz, "
                                                               f"**{random.choice(FRASE_MEIO)}**. Vamos ter que "
                                                               f"aguardar ela finalizar lá, ou utilizar outro bot "
                                                               f"no meio tempo.")

            # If no more music in queue
            if not self.song_queue[0] or not self.song_queue:
                return await interaction.response.send_message(f"Não tem mais músicas na lista. Se quiser parar "
                                                               f"completamente a música, utilize o /stop")

            self.song_queue = self.song_queue[qty - 1:]
            self.vc.stop()

        async def queue_(self, interaction: discord.Interaction):
            # If no songs in queue and not currently playing
            if len(self.song_queue) == 0 and not self.isPlaying:
                return await interaction.response.send_message(
                    f"Não tem nenhuma música na lista, **{random.choice(FRASE_MEIO)}**")
            # If playing song and no other songs in queue
            elif len(self.song_queue) == 0 and self.isPlaying:
                await interaction.response.send_message(f"Só tem a música que está tocando, na lista. Dá uma olhadinha")
                return await self.now_(interaction)

            e = discord.Embed(
                title=":notes: Lista de músicas do momento:",
                description="",
                colour=discord.Color.dark_gold())

            for i, music in enumerate(self.song_queue):
                actual = await self.music_info_(music)
                title = actual[0]

                # Check if embed fits next song
                if len(str(e)) < 5800 and len(e.description) < 4000:
                    e.description += f"{i + 1}) {title}\n"
                else:
                    e.description += f"{i + 1}) [...]\n"
                    break
            e.set_footer(text=f"\nProntinho, **{random.choice(FRASE_MEIO)}**. Da uma olhada na lista.")
            return await interaction.response.send_message(embed=e)

        async def search_(self, amount: int, song: str, get_url=False):
            # Loop until YoutubeDL returns the expected amount of links
            info = await self.bot.loop.run_in_executor(
                None, lambda: YoutubeDL({"format": "bestaudio/best", "quiet": True, "noplaylist": True}).extract_info(
                    f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))

            # If nothing found, return
            if len(info['entries']) == 0:
                return None

            # If results were found, return the URLs for parsing or the whole list
            return [entry['webpage_url'] for entry in info['entries']] if get_url \
                else [[entry['webpage_url'], entry['title'], entry['thumbnails'][0]['url']] for entry in info['entries']]

    @app_commands.command(name='play', description='Tocar musicas')
    async def play(self, interaction: discord.Interaction, *, url: str = None):
        """Play music.

        Play a song or playlist from a URL either from YouTube or Spotify, or search for a song by name
        and add it to the queue.

        Parameters:
            self: The instance of the cog.
            interaction: discord.Interaction
                The interaction object representing the user's command.
            url: str [OPTIONAL]
                The URL of the song or playlist to play or name of the song/artist/video. Defaults to None.

        Returns:
            This function does Not return anything.
        """

        try:
            guild_id = interaction.guild_id

            # If no Voice Client for the caller Guild, instantiate
            if guild_id not in self.playing_guilds:
                self.playing_guilds[guild_id] = Player.Play(interaction, self.bot)

            # Set variables for easier reference
            player = self.playing_guilds[guild_id]
            queue = player.song_queue
            q_len = len(queue)

            # Try to join Voice Channel
            error_joined = await player.join_(interaction)
            if error_joined:
                return

            # Check if user provided a URL or Song Name
            if url:
                # Check if URL is from Spotify
                if "spotify" in url:
                    # Check if URL is for a Playlist in Spotify
                    if "playlist" in url:
                        await interaction.response.send_message(f"Isso aí é uma playlist, né **{chosen_phrase()}**? "
                                                                f"Analisando músicas!")
                        async with interaction.channel.typing():
                            song_names_array = await player.spotify_parse_(interaction, url)
                            counter = 0

                            for song in song_names_array:
                                result = await player.search_(1, f"music {song}", get_url=True)

                                if not result:
                                    await interaction.followup.send(
                                        f"Não rolou de adicionar a música {song}. Parece que o formato está errado "
                                        f"ou a música não existe. Tenta uma palavra diferente?"
                                    )
                                else:
                                    song_url = result[0]
                                    queue.append(song_url)
                                    counter += 1

                            await interaction.followup.send(f"Adicionei {counter} músicas na playlist!")
                            if player.vc.is_playing():
                                return
                            else:
                                await interaction.followup.send(f"Tocando: {queue[0]}")
                                await player.play_(interaction, queue[0])

                    # Check if URL is for a Track in Spotify
                    elif "track" in url:
                        await interaction.response.send_message(f"Segura aí **{chosen_phrase()}**!")

                        song_name = await player.spotify_parse_(interaction, url, playlist=False)
                        result = await player.search_(1, f"music {song_name}", get_url=True)

                        if not result:
                            await interaction.followup.send(
                                f"Não rolou de adicionar a música {song_name}. Parece que o formato está errado "
                                f"ou a música não existe. Tenta uma palavra diferente?"
                            )
                        else:
                            song_url = result[0]
                            queue.append(song_url)

                        if player.vc.is_playing():
                            return await interaction.followup.send(
                                f"Música adicionada à lista na posição **{q_len + 1}**. Essa é braba!"
                            )
                        else:
                            await interaction.followup.send(f"Tocando: {queue[0]}")
                            await player.play_(interaction, queue[0])

                # Check if URL is from YouTube
                elif "youtube.com" in url or "youtu.be" in url:
                    # Check if URL is for a Playlist in YouTube
                    if "playlist?" in url:
                        # Initial response
                        await interaction.response.send_message(f"Isso aí é uma playlist, né **{chosen_phrase()}**? "
                                                                f"Analisando músicas!")

                        async with interaction.channel.typing():
                            # Parse all songs in playlist and add to queue
                            counter = await player.youtube_playlist_(interaction, url)
                            # Inform user how many songs were successfully processed and added to queue
                            await interaction.followup.send(f"Adicionei {counter} músicas na playlist.")

                            # If Bot is already playing, return
                            if player.vc.is_playing():
                                return

                            # If Bot is Not playing, initiate call play method
                            await interaction.followup.send(f"Tocando: {queue[0]}")
                            return await player.play_(interaction, queue[0])

                    # If URL from YouTube, but not playlist handle as individual video
                    else:
                        queue.append(url)
                        await interaction.response.send_message(f"Tocando: {queue[0]}")
                        await player.play_(interaction, queue[0])

                else:
                    await interaction.response.send_message(f"Vou procurar sua música aqui na lista de CDs que o patrão"
                                                            f" deixou. Segura aí que vai demorar alguns segundinhos, "
                                                            f"**{chosen_phrase()}**")
                    async with interaction.channel.typing():
                        result = await player.search_(1, url, get_url=True)

                    if not result:
                        return interaction.followup.send(
                            f"Não rolou de baixar essa música. Parece que o formato tá errado "
                            f"ou a música não existe. Tenta uma palavra diferente?")

                    song_url = result[0]
                    queue.append(song_url)

                    if player.vc.is_playing():
                        return await interaction.followup.send(
                            f"Música adicionada à lista na posição **{q_len + 1}**. Essa é braba!"
                        )
                    else:
                        await interaction.followup.send(f"Tocando: {queue[0]}")
                        await player.play_(interaction, queue[0])

            else:
                if player.vc.is_playing():
                    await interaction.response.send_message(f"Mas eu já estou tocando, **{chosen_phrase()}**")
                elif player.vc.is_paused():
                    player.vc.resume()

        except Exception as e:
            await interaction.response.send_message(f"{e}")
            return await interaction.followup.send(f"Não consegui processar nenhuma música ou playlist a partir "
                                                   f"desse link, **{chosen_phrase()}**, bora tentar outra? "
                                                   f"Usa o comando `/search NomeDaMusica`")

    @app_commands.command(name="stop", description="Parar musicas e desconectar do canal de voz")
    async def stop(self, interaction: discord.Interaction):
        """Stops music playback and disconnects from the voice channel.

        This command stops the playback of music and disconnects the bot from the voice channel.

        Parameters:
            self: The instance of the cog.
            interaction: discord.Interaction
                The interaction object representing the user's command.

        Returns:
            This function does Not return anything.
        """

        guild_id = interaction.guild_id
        player = self.playing_guilds[guild_id]
        await player.stop_leave_(interaction)
        self.playing_guilds.pop(guild_id)

    @app_commands.command(name="pause", description="Pausar música em reprodução")
    async def pause(self, interaction: discord.Interaction):
        """Pause or Resume Voice Client

        Pauses or resumes the currently playing music within that guild.

        Parameters:
            self: The instance of the cog.
            interaction: discord.Interaction
                The interaction object representing the user's command.

        Returns:
            This function does Not return anything.
        """

        try:
            guild_id = interaction.guild_id
            player = self.playing_guilds[guild_id]
        except KeyError:
            return await interaction.response.send_message(f"Mas eu não estou tocando, **{chosen_phrase()}**")
        else:
            if player.vc.is_playing():
                await interaction.response.send_message("Música pausada")
                return player.vc.pause()
            else:
                await interaction.response.send_message("Continuando música")
                return player.vc.resume()

    @app_commands.command(name="resume", description="Continuar música em reprodução")
    async def resume(self, interaction: discord.Interaction):
        """Resumes Voice Client

        Checks if Bot is playing within this guild, and pauses the Voice Client.

        Parameters:
            self: The instance of the cog.
            interaction: discord.Interaction
                The interaction object representing the user's command.

        Returns:
            This function does Not return anything.
        """

        try:
            guild_id = interaction.guild_id
            player = self.playing_guilds[guild_id]
        except KeyError:
            return await interaction.response.send_message(f"Mas eu não estou tocando, **{chosen_phrase()}**")
        else:
            if player.vc.is_paused():
                return player.vc.resume()
            else:
                return await interaction.response.send_message(f"A música não está pausada, **{chosen_phrase()}**. "
                                                               f"Pra pausar é só mandar um `/pause`.")

    @app_commands.command(name="now", description="Mostra a música tocando no momento")
    async def now(self, interaction: discord.Interaction):
        """Display the currently playing song.

        This command displays information of the currently playing song, including Song Name,
        URL and Channel name.

        Parameters:
            self: The instance of the cog.
            interaction: discord.Interaction
                The interaction object representing the user's command.

        Returns:
            This function does Not return anything.
        """

        try:
            guild_id = interaction.guild_id
            player = self.playing_guilds[guild_id]
        except KeyError:
            return await interaction.response.send_message(f"Não estamos com serviço couvert hoje, "
                                                           f"**{chosen_phrase()}**. Obrigado.")
        else:
            await player.now_(interaction)

    @app_commands.command(name="criador", description="Mostra informações do criador do Bot")
    async def creator(self, interaction: discord.Interaction):
        ...

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        """A listener to monitor voice state updates and disconnect the bot if it's not playing for 180 seconds.

        This listener checks for voice state updates in the server and disconnects the bot from the voice
        channel if it's not playing for 180 seconds. Events from users are ignored.

        Parameters:
            self: The instance of the cog.
            member: discord.Member
                The member whose voice state was updated.
            before: discord.VoiceState
                The voice state before the update.
            after: discord.VoiceState
                The voice state after the update.

        Returns:
            This function does Not return anything.
        """

        guild_id = member.guild.id
        player = self.playing_guilds[guild_id]

        # If change of Voice Channel not from Bot
        if not member.id == self.bot.user.id:
            return

        # Check if playing when IN Voice Channel, every 180 seconds
        else:
            while True:
                await asyncio.sleep(180)
                if not player.vc.is_playing():
                    await player.vc.disconnect()
                    self.playing_guilds.pop(guild_id)
                    player.vc = None
                    break


async def setup(bot):
    await bot.add_cog(Player(bot))
