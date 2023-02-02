import os
import music_tag

from PIL import Image
from pathlib import Path


def convert_to_m4a(location_mp4: str, location_m4a: str):
    """
    Create a .m4a sound file out of a .mp4 video file
    :param location_mp4: The current location of the .mp4 input file
    :param location_m4a: The location at which the .m4a file should be saved
    :return: None
    """
    os.system(f'ffmpeg -i "{location_mp4}" -vn -c:a copy "{location_m4a}"')


def clean_temp_folder(location_mp4_tempdir: str) -> None:
    """
    Deletes all files in the temporary folder.
    :param location_mp4_tempdir: Directory of the temp saved mp4s
    :return: None
    """
    print("Removing temporary mp4 files (pass -k to keep)")
    for subdir, dirs, files in os.walk(location_mp4_tempdir):
        for file in files:
            if file.title() == ".Gitkeep":
                continue
            print("Removing " + os.path.join(subdir, file))
            os.remove(os.path.join(subdir, file))
    print("Done removing temp files. (pass -k to keep)")


def set_meta_tags(location_m4a: str, title: str, author: str, jpg_path: str) -> None:
    file = music_tag.load_file(location_m4a)
    file['title'] = title
    file['artist'] = author

    # Convert the jpg picture to png (music-tag package wants this for some reason)
    png_path = Path(jpg_path).with_suffix(".png")
    jpg_img = Image.open(jpg_path)
    jpg_img.save(png_path)

    # Set the cover image if provided (suppressed by -nocover)
    if os.path.isfile(png_path) or png_path != "NONE":
        with open(png_path, 'rb') as img_in:
            file['artwork'] = img_in.read()

    file.save()
