import os
import asyncio
import configparser  # for reading config file
import os.path  # for path joining
import argparse

from song_scraper import scrape_playlist, scrape_file
from youtube_utils import get_id_by_name, download_video, download_cover
from conversion_utils import convert_to_m4a, clean_temp_folder, set_meta_tags, convert_to_mp3
from pathlib import Path


async def run(arguments: argparse.Namespace, songs: dict):
    """
    Iterates over a list of song names, fetches them from youtube and converts them into .m4a format
    :param arguments: Commandline arguments to check how the user wants the script to act
    :param songs: the list of songs to be fetched
    :return: None
    """
    for song_name, section in songs.items():
        print(f"Working on {song_name}...")

        # Get video id
        video_id = await get_id_by_name(song_name)

        # Download Video to wanted location
        mp4_name, video_author, video_title, video_cover_url = download_video(video_id,
                                                                              config["LOCATIONS"]["Mp4TempFolder"])

        # Convert .mp4 video to .m4a SoundFile
        mp4_path = os.path.join(config["LOCATIONS"]["Mp4TempFolder"], Path(mp4_name))

        output_file_path = ""
        print("Checking conversion format...")
        if arguments.convertmp3:
            # Default section is only the case when there were no sections given or songs posted before a section first
            # began
            if section == "Default":
                output_file_path = os.path.join(config["LOCATIONS"]["M4aSaveFolder"], Path(mp4_name).with_suffix('.mp3'))
            else:
                # Create a new folder for the Section / category if it not yet exists
                section_dir = os.path.join(config["LOCATIONS"]["M4aSaveFolder"], section)
                if not os.path.exists(section_dir):
                    os.makedirs(section_dir)
                output_file_path = os.path.join(section_dir, Path(mp4_name).with_suffix('.mp3'))

            print(f"MP4: {mp4_path}")
            print(f"M4A: {output_file_path}")
            convert_to_mp3(mp4_path, output_file_path)
        else:
            # Default section is only the case when there were no sections given or songs posted before a section first
            # began
            if section == "Default":
                output_file_path = os.path.join(config["LOCATIONS"]["M4aSaveFolder"], Path(mp4_name).with_suffix('.m4a'))
            else:
                # Create a new folder for the Section / category if it not yet exists
                section_dir = os.path.join(config["LOCATIONS"]["M4aSaveFolder"], section)
                if not os.path.exists(section_dir):
                    os.makedirs(section_dir)
                output_file_path = os.path.join(section_dir, Path(mp4_name).with_suffix('.m4a'))

            print(f"MP4: {output_file_path}")
            print(f"M4A: {output_file_path}")
            convert_to_m4a(mp4_path, output_file_path)

        # Download cover (-nocover will stop this)
        if arguments.no_cover_in_metadata:
            jpg_path = "NONE"
        else:
            jpg_path = download_cover(video_cover_url, video_id, config["LOCATIONS"]["Mp4TempFolder"])

        # Set the meta-tags
        if not arguments.convertmp3:
            set_meta_tags(output_file_path, video_title, video_author, jpg_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="DS4DJ",
        description="An automated toolchain for fetching a list of songs from YouTube and converting them to the "
                    "desired format (in this case .m4a.) ",
        epilog="This utility was made for private use"
    )
    parser.add_argument("-k", "--keep_temporary_content",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="If set, keeps the temporary files in the temporary folder.")
    parser.add_argument("-c", "--no_cover_in_metadata",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="If set, does not add a cover image to the sound-files.")
    parser.add_argument("-p", "--playlist_url",
                        action="store",
                        help="Allows you to parse an url to a YouTube playlist to be used as the input")
    parser.add_argument("-mp3", "--convertmp3",
                        action=argparse.BooleanOptionalAction,
                        help="Convert to mp3")
    parser.add_argument("-g", "--genre_name_playlist",
                        action="store",
                        default="Default",
                        help="Requires a playlist url to be specified. Allows you to automatically sort all files "
                             "into the given directory name")

    args = parser.parse_args()

    if args.genre_name_playlist != "Default" and args.playlist_url is None:
        parser.error("--genre_name_playlist requires --playlist_url to be set.")

    # Read configuration file config.ini
    if os.path.isfile("config.ini"):  # check if config file exists
        config = configparser.ConfigParser()
        config.read("config.ini")
    else:  # File could not be found
        print("Could not find config.ini file, using default fallbacks (your 'Downloads' folder)")
        config = "DEFAULT"

        # Set default save/temp locations to the download directory if not found in the config
    if "LOCATIONS" not in config or "Mp4TempFolder" not in config["LOCATIONS"]:
        config["LOCATIONS"]["Mp4TempFolder"] = rf"{os.path.join(Path.home(), 'Downloads')}"
    if "LOCATIONS" not in config or "M4aSaveFolder" not in config["LOCATIONS"]:
        config["LOCATIONS"]["M4aSaveFolder"] = rf"{os.path.join(Path.home(), 'Downloads')}"

    # Scrape a song dictionary - contains their category from the scrape file or "Default" if none were found
    if args.playlist_url is None:
        song_dict = scrape_file(config)
    else:
        song_dict = scrape_playlist(args.playlist_url, args.genre_name_playlist)

    # Exit condition if no songs were found
    if len(song_dict) < 1: exit(0)

    # Scrape all Videos
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args, song_dict))
    loop.close()

    # Clean temp folder if flag -k is not set
    if not args.keep_temporary_content:
        clean_temp_folder(config["LOCATIONS"]["Mp4TempFolder"])
    else:
        print("Keeping temporary mp4 files.")

    print("Done. You can now close the window.")
