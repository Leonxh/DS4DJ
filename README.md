# DS4DJ
An automated toolchain for fetching a list of songs from YouTube and converting them to the desired format (in this case .m4a).

## Flags / Options when executing
Command line arguments are as following: 
+ -k : Keep the temporary files (mp4 and jpg)
+ -nocover : Does not add a cover image to the converted m4a
+ -playlist : Tells the program to start in playlist mode
    + you will need to provide the full playlist during runtime

## Setup
* Rename / Copy the ``config.template`` file to a ``config.txt`` file
    * Input your temporary & output folder, and your input file
* Rename / Copy / add the ``music.txt`` file. It will hold the songs you want to scrape from YouTube.
    * Each line in the file corresponds to one search/song on YouTube.
    * If you want to automatically save your music in named folders (genres for example) you can use the "Sections" that are shown in the ``music.template`` example. This is not a must however. unsectioned songs will just be placed into the output folder.
* Please set up your virtual environment for python (Version 3.9) using the provided ``requirements.txt`` file by executing ``pip install -r requirements.txt``.
* Make sure you have ffmpeg installed...

## Usage
After activating your virtual environment, you can execute the script by just calling main.py with ``python main.py``.
Enjoy :)
