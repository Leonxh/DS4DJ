import os


def convert_to_m4a(location_mp4: str, location_m4a: str):
    """
    Create a .m4a sound file out of a .mp4 video file
    :param location_mp4: The current location of the .mp4 input file
    :param location_m4a: The location at which the .m4a file should be saved
    :return: None
    """
    os.system(f'ffmpeg -i "{location_mp4}" -vn -c:a copy "{location_m4a}"')
