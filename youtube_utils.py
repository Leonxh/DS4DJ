from youtubesearchpython.__future__ import VideosSearch
from pytube import YouTube
from pathlib import Path


async def get_id_by_name(search_string: str):
    """
    Searches for a fitting video on youtube for the current search string and returns the id
    :param search_string: search keywords for the youtube search
    :return: the video id of the found video
    """
    videos_search = VideosSearch(search_string, limit=1)
    videos_result = await videos_search.next()
    return videos_result.get("result")[0].get("id")


def download_video(video_id: str, save_location: str):
    """
    Downloads a youtube video as audio only, given a video id
    :param video_id: the youtube video id to use when downloading
    :param save_location: the folder in which to save the file
    :return: the final filepath of the file
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_object = YouTube(url=url)
    video_object.streams.get_audio_only().download(save_location)
    file_name = Path(video_object.streams.get_audio_only().default_filename)
    return file_name
