import asyncio
import itertools
import random
import re

import discord

from youtube_source import YTDLSource

class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        track_info = self.nice_desc(self.source)
        embed = (discord.Embed(title='Now playing',
                               description=track_info.format(self),
                               color=discord.Color.blurple())
        .add_field(name='Duration', value=self.source.duration)
        .set_thumbnail(url=self.source.thumbnail))

        return embed

    def nice_desc(self, source: YTDLSource):
        description_elements = source.title.split(" - ")
        separator_count = len(re.findall("\s\-\s", source.title))

        # If there's only one separator found, we can be confident that we can
        # format the artist and track title separately.
        if separator_count == 1:
            artist, title = description_elements
        # If there's more than one separator found, we can naively split on
        # the first separator and hope that's the right one to split on...
        elif separator_count > 1:
            elements = list(dict.fromkeys(description_elements))
            artist = "".join(elements[:1])
            title = " - ".join(elements[1:])
        # In other cases there's no clear way to do anything cool. I'm scared
        # of all the spiders. Catching things and eating their insides.
        else:
            artist = ""
            title = source.title

        # If the track is from YouTube we can maybe strip out some of the
        # garbage like (Official Music Video) from the track name.
        if "youtube.com" in source.url:
            title = source.nice_track_title(title)

        if len(artist) > 0:
            return f'{artist} - [{title}]({source.url})'
        else:
            return f'**[{title}]({source.url})**'

class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]
