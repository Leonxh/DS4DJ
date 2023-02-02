import os


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
            print("Removing " + os.path.join(subdir, file))
            os.remove(os.path.join(subdir, file))
    print("Done removing temp files. (pass -k to keep)")