import pytest
import unittest
import urllib3
import vcr

from bandcamp import Bandcamp

class TestBandcamp:
    def test_with_no_arguments(self):
        with pytest.raises(TypeError):
            Bandcamp()

    def test_perform_with_invalid_link(self):
        invalid_link = "https://not-a-bandcamp-link.com/haha"

        assert Bandcamp(invalid_link).perform() == []

    def test_perform_with_invalid_album_link(self):
        invalid_album_link = "https://155pod.bandcamp.com/not-an-album/haha"

        assert Bandcamp(invalid_album_link).perform() == []

    @vcr.use_cassette("tests/cassettes/perform_with_nonexistent_album_link.yaml")
    def test_perform_with_404_album_link(self):
        nonexistent_album_link = "https://155pod.bandcamp.com/album/not-yet"

        assert Bandcamp(nonexistent_album_link).perform() == []

    @vcr.use_cassette("tests/cassettes/perform_with_album_link.yaml")
    def test_perform_with_album_link(self):
        valid_album_link = "https://155pod.bandcamp.com/album/j-a-r"
        expected_result = [
            "https://155pod.bandcamp.com/track/j-a-r-5",
            "https://155pod.bandcamp.com/track/j-a-r-jason-andrew-relva",
            "https://155pod.bandcamp.com/track/j-a-r-for-three-basses",
            "https://155pod.bandcamp.com/track/j-a-r-6",
            "https://155pod.bandcamp.com/track/p-l-u-r-yul-ibz-mix",
            "https://155pod.bandcamp.com/track/m-a-s-o-n",
            "https://155pod.bandcamp.com/track/there-is-no-such-thing-as-rhythm-or-timing",
            "https://155pod.bandcamp.com/track/j-a-r-4",
            "https://155pod.bandcamp.com/track/j-a-r-2",
            "https://155pod.bandcamp.com/track/a-d-k",
            "https://155pod.bandcamp.com/track/joz-augmented-reality-j-a-r",
            "https://155pod.bandcamp.com/track/j-a-r-things-that-made-my-previous-roommates-upset-demo",
            "https://155pod.bandcamp.com/track/j-a-r-8",
            "https://155pod.bandcamp.com/track/j-a-r-11",
            "https://155pod.bandcamp.com/track/j-a-r-10",
            "https://155pod.bandcamp.com/track/j-a-r-abridged",
            "https://155pod.bandcamp.com/track/jar",
            "https://155pod.bandcamp.com/track/j-a-r-t-y-h-a-r-d",
            "https://155pod.bandcamp.com/track/j-a-r-7",
            "https://155pod.bandcamp.com/track/j-a-r-3",
            "https://155pod.bandcamp.com/track/jason-andrew-relva",
            "https://155pod.bandcamp.com/track/philosophy-of-the-j-a-r",
            "https://155pod.bandcamp.com/track/jar-4",
            "https://155pod.bandcamp.com/track/jars-of-clay-ft-cake",
            "https://155pod.bandcamp.com/track/j-a-r-but-the-a-stands-for-angus-just-like-angus-stands-for-all-of-us-bless-up",
            "https://155pod.bandcamp.com/track/jar-2",
            "https://155pod.bandcamp.com/track/while-im-young-and-while-im-able",
            "https://155pod.bandcamp.com/track/tiny-fuel-drum",
            "https://155pod.bandcamp.com/track/jar-bass-cover",
            "https://155pod.bandcamp.com/track/j-a-r-egghead-bunson-cover",
            "https://155pod.bandcamp.com/track/j-a-r-jacques-antoine-rousseau",
            "https://155pod.bandcamp.com/track/jar-demo",
            "https://155pod.bandcamp.com/track/pod-laundry",
            "https://155pod.bandcamp.com/track/j-a-r-9",
            "https://155pod.bandcamp.com/track/grouch-stew-j-a-r-ed",
            "https://155pod.bandcamp.com/track/sason-kandrew-alva",
            "https://155pod.bandcamp.com/track/skar",
            "https://155pod.bandcamp.com/track/jar-5",
            "https://155pod.bandcamp.com/track/jargonaut",
            "https://155pod.bandcamp.com/track/h-b-g-happy-birthday-globehellremix",
            "https://155pod.bandcamp.com/track/j-a-r-electro-swing-mix",
            "https://155pod.bandcamp.com/track/j-a-r-jason-andrew-relva-cover",
            "https://155pod.bandcamp.com/track/j-a-r-jarring-ambient-roomy",
            "https://155pod.bandcamp.com/track/jar-3",
            "https://155pod.bandcamp.com/track/crass-loops-155-jar"
        ]

        assert Bandcamp(valid_album_link).perform() == expected_result

    def test_perform_with_track_link(self):
        valid_track_link = "https://155pod.bandcamp.com/track/jargonaut"
        expected_result = ["https://155pod.bandcamp.com/track/jargonaut"]

        assert Bandcamp(valid_track_link).perform() == expected_result
