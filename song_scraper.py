import configparser
from youtube_utils import resolve_playlist, full_url_to_id


def scrape_playlist():
    songs = []
    full_urls = resolve_playlist(input("YouTube Playlist url: "))
    for full_url in full_urls:
        songs.append(full_url_to_id(full_url))
    return songs


def scrape_file(config: configparser.ConfigParser):
    songs = []
    with open(config["INPUT"]["ScrapeFile"].strip(), 'r') as s_file:
        for song_line in s_file:
            song = song_line.strip()
            songs.append(song)
    return songs


def scrape_songs(config: configparser.ConfigParser, is_playlist: bool = False):
    # This is where we decide if we download a playlist or nah
    if is_playlist:  # we download a whole playlist
        songs = scrape_playlist()
    else:  # Download from the file
        songs = scrape_file(config)
    return songs
