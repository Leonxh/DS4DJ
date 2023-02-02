import configparser
from youtube_utils import resolve_playlist, full_url_to_id
from pathlib import Path


def scrape_playlist(playlist_url: str, genre: str):
    song_dict = {}
    full_urls = resolve_playlist(playlist_url)
    for full_url in full_urls:
        song_dict.update({full_url_to_id(full_url): genre})
    return song_dict


def scrape_file(config: configparser.ConfigParser):
    file_path = Path(config["INPUT"]["ScrapeFile"].strip())
    if not file_path.is_file():
        print(f"Was not able to find file '{file_path.name}' for scraping...")
        exit(1)

    song_dict = scrape_section_file(file_path)
    return song_dict


def scrape_section_file(file):
    song_dict = {}

    with open(file, 'r') as file_to_validate:
        line_num = 0
        current_section = "Default"
        for line in file_to_validate:
            line_num += 1
            if line == "":
                print(f"Found empty line in line {line_num}")
                continue

            if line.startswith("\\\\[SECTION] "):
                current_section = " ".join(line.split(" ")[1:]).strip()
            else:
                song_dict.update({line.strip(): current_section})

    return song_dict
