import pytest
import unittest
import urllib3

from unittest.mock import MagicMock
from unittest.mock import patch

from songs import Song
from youtube_source import YTDLSource

class TestSong(unittest.TestCase):
    @patch('youtube_source.YTDLSource')
    def setUp(self, mock_ytdl_source):
        self.mock_ytdl_source = MagicMock(autospec=YTDLSource)
        self.mock_ytdl_source.url = "https://example.com/track"
        self.song = Song(self.mock_ytdl_source)

    def test_nice_desc_with_one_hyphen(self):
        self.mock_ytdl_source.title = "Baby Tyler - Pet Sematary"

        assert self.song.nice_desc(self.mock_ytdl_source) == \
            'Baby Tyler - [Pet Sematary](https://example.com/track)'

    def test_nice_desc_with_multiple_hyphens(self):
        self.mock_ytdl_source.title = "Baby Tyler - Baby Tyler - Pet Sematary"

        assert self.song.nice_desc(self.mock_ytdl_source) == \
            'Baby Tyler - [Pet Sematary](https://example.com/track)'

    def test_nice_desc_with_no_hyphens(self):
        self.mock_ytdl_source.title = "Baby Tyler: Pet Sematary"

        assert self.song.nice_desc(self.mock_ytdl_source) == \
            '**[Baby Tyler: Pet Sematary](https://example.com/track)**'
