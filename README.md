# DS4DJ
An automated toolchain for fetching a list of songs from YouTube and converting them to the desired format (in this case .m4a).

## Setup
* Rename / Copy the ``config.template`` file to a ``config.txt`` file
    * Input your temporary & output folder, and your input file
* Rename / Copy / add the ``music.txt`` file. It will hold the songs you want to scrape from YouTube.
    * Each line in the file corresponds to one search/song on YouTube. Consider the example given in the ``music.template``.
* Please set up your virtual environment for python (Version 3.9) using the provided ``requirements.txt`` file by executing ``pip install -r requirements.txt``.
* Make sure you have ffmpeg installed...

## Usage
After activating your virtual environment, you can execute the script by just calling main.py with ``python main.py``.
Enjoy :)