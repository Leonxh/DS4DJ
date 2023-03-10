from youtubesearchpython.__future__ import VideosSearch

from pytube.helpers import DeferredGeneratorList

from pytube import YouTube, Playlist
from pathlib import Path
import requests
import os


async def get_id_by_name(search_string: str):
    """
    Searches for a fitting video on youtube for the current search string and returns the id
    :param search_string: search keywords for the youtube search
    :return: the video id of the found video
    """
    videos_search = VideosSearch(search_string, limit=1)
    videos_result = await videos_search.next()
    return videos_result.get("result")[0].get("id")


def download_cover(cover_url: str, video_id: str, img_tempdir: str) -> str:
    """
    Downloads a youtube cover image and returns the filename
    :param cover_url: the img_url
    :param video_id: the ID string of the video 
    :param img_tempdir: the temp directory to save the covers to
    :return: filename
    """
    r = requests.get(cover_url, allow_redirects=True)
    open(img_tempdir + os.sep + video_id + ".jpg", 'wb').write(r.content)
    return img_tempdir + os.sep + video_id + ".jpg"


def download_video(video_id: str, save_location: str) -> tuple[Path, str, str, str]:
    """
    Downloads a youtube video as audio only, given a video id
    :param video_id: the youtube video id to use when downloading
    :param save_location: the folder in which to save the file
    :return: [filename, video author, video name, thumbnail url]
    """
    video_object = YouTube.from_id(video_id)
    print(f"{video_object.author} {video_object.title}")

    video_object.streams.get_audio_only().download(save_location)
    file_name = Path(video_object.streams.get_audio_only().default_filename)
    return file_name, video_object.author, video_object.title, video_object.thumbnail_url


def resolve_playlist(playlist_url: str) -> DeferredGeneratorList:
    return Playlist(playlist_url).video_urls


def full_url_to_id(url: str) -> str:
    return url.replace("https://www.youtube.com/watch?v=", '')
