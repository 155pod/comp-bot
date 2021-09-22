import re
import urllib.request

class Bandcamp:
    TRACK_LINK_RE = "https://[\d\w-]+.bandcamp.com/track/[\d\w-]+"

    def __init__(self, url):
        self.url = url

    # Usage:
    #
    #     Bandcamp("https://155pod.bandcamp.com/album/j-a-r").perform()
    #
    # Returns an array of tracks. If no tracks can be found, it returns an
    # empty array.
    def perform(self):
        # If the link isn't a Bandcamp link, do nothing.
        if not self.__is_bandcamp_link():
            return []

        # If the link is a Bandcamp album link, return a list of links to each
        # individual track. If there are no track links, return an empty array.
        if self.__is_album_link():
            album_links = self.__album_track_links(self.url)

            if len(album_links) == 0:
                return []
            else:
                return album_links

        # If the link is a Bandcamp track link, return the single track link as
        # a list.
        elif self.__is_track_link():
            return self.url.split()

        # Otherwise, return an empty array.
        else:
            return []

    def __album_track_links(self, album_link):
        track_list = []
        all_track_links = re.findall(
            self.TRACK_LINK_RE,
            self.__webpage_html(album_link)
        )

        for track_link in all_track_links:
            if not track_link in track_list:
                track_list.append(track_link)

        return track_list

    def __is_bandcamp_link(self):
        if "https://" in self.url and ("bandcamp.com" in self.url):
            return True
        else:
            return False

    def __is_album_link(self):
        if "/album/" in self.url:
            return True
        else:
            return False

    def __is_track_link(self):
        if "/track/" in self.url:
            return True
        else:
            return False

    def __webpage_html(self, url):
        content = ""

        try:
            content = urllib.request.urlopen(url).read().decode("utf-8")
        except urllib.error.HTTPError:
            print("Sorry, that doesn't seem to be a valid album or track.")

        return content
