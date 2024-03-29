import asyncio
import math
import os
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

from bandcamp import Bandcamp
from songs import Song, SongQueue
from youtube_source import YTDLError, YTDLSource
import responses

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
    pass

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if self.current is not None:
                await self.current.source.channel.send(responses.get_song_response(self.bot, self.current.source))

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='help', invoke_without_subcommand=True)
    async def help(self, ctx: commands.Context):
        favourite_bands = [
            "blink-182",
            "+44",
            "Angels & Airwaves",
            "Box Car Racer",
            "The Tragically Hip (with a capital T in the 'The')"
        ]
        favourite_hosts = ["Sam", "Josiah"]

        await ctx.send(
            f'Hello, I am **comp-bot**.\n'                                    \
            f'My favourite band is {random.choice(favourite_bands)}. '        \
            f'The best 155 host is {random.choice(favourite_hosts)}.\n'       \
            f'Here\'s a list of my commands:\n'                               \
            f'>>> '                                                           \
            f'`help`: '                                                       \
            f'Congratulations, you figured this one out.\n'                   \
            f'`join`: '                                                       \
            f'Join a voice channel.\n'                                        \
            f'`now`: '                                                        \
            f'Display what\'s playing right now. '                            \
            f'(aliases: `current`, `np`, `playing`)\n'                        \
            f'`pause`: '                                                      \
            f'Pause the currently playing track.\n'                           \
            f'`play`: '                                                       \
            f'Add a song to the play queue. This takes a URL or YouTube '     \
            f'search term. '                                                  \
            f'(aliases: `add`)\n'                                             \
            f'`queue`: '                                                      \
            f'Show a list of currently queued songs.\n'                       \
            f'`remove`: '                                                     \
            f'Remove a queued song. (E.g. `remove 2`.)\n'                     \
            f'`resume`: '                                                     \
            f'Resume a song that\'s been paused.\n'                           \
            f'`skip`: '                                                       \
            f'Skip the current song, democratically.\n'                       \
            f'`stop`: '                                                       \
            f'Stop the current song and clear the queue.\n'                   \
            f'`summon`: '                                                     \
            f'Invite me to join the current voice channel.\n'                 \
            f'`volume`: '                                                     \
            f'Set the player volume (for everyone).\n'
            .format(self)
        )

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon', aliases=['connect'])
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.

        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        return await ctx.send("Bye!!\n"                                          \
                              "FYI – this bot costs althea 5 bones a month "     \
                              "to maintain. It was built by althea, bw, and "    \
                              "smlbf. You might thank them if you have a minute.")

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing', 'np'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        25% of listeners need to vote to skip.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)
            # votes_needed = (len(ctx.author.voice.members.size))/4

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context):
        """Shows the player's queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs):
            queue += f'{i + 1}. [{str(song.source)}]({song.source.url})\n'

        embed = discord.Embed(
            description="There's {} tracks in the queue:\n{}"
            .format(len(ctx.voice_state.songs), queue)
        )

        await ctx.send(embed=embed)

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', aliases=['add'])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.

        If there are songs in the queue, this will be queued until the other
        songs finished playing.

        This command automatically searches from various sites if no URL is. A
        list of these sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            if "bandcamp.com" in search:
                track_urls = Bandcamp(search).perform()
                if len(track_urls) > 1:
                    await ctx.send("Hold up. Currently enqueuing album...")
                    await self.__enqueue_bandcamp_album(ctx, track_urls)
                    await ctx.send(f'{responses.get_enqueue_response(self.bot)}' \
                                   f' The album is enqueued now.')
                else:
                    await self.__enqueue_single_track(ctx, search, True)
            else:
                await self.__enqueue_single_track(ctx, search, True)

    async def __enqueue_single_track(self, ctx: commands.Context, track_url, enqueued_message: bool):
        try:
            source = await YTDLSource.create_source(
                ctx,
                track_url,
                loop=self.bot.loop
            )

        except YTDLError as e:
            await ctx.send(
                "An error occurred while processing this request: {}" \
                .format(str(e))
            )
        else:
            song = Song(source)
            await ctx.voice_state.songs.put(song)

            if len(ctx.voice_state.songs) > 1 and enqueued_message:
                await ctx.send(f'Enqueued {str(source)}' \
                               f' {responses.get_enqueue_response(self.bot)}')

            if "Rollin" in source.title:
                await ctx.send("Rollin', rollin', rollin', rollin'")

    async def __enqueue_bandcamp_album(self, ctx: commands.Context, album_track_urls):
        for track_url in album_track_urls:
            await self.__enqueue_single_track(ctx, track_url, False)

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')


bot = commands.Bot(
    'music.',
    description='I am made of Sam and Jos and I play full Bandcamp albums.',
    help_command=None
)

bot.add_cog(Music(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(os.environ['TOKEN'])
