# Audio Silence Trimmer and Level Normalizer Delete from Middle

A way to make editing music simple.

1. Take directory of music files, and normalize audio.
2. Search the audio file for the actual music and cut out silence and trivial bits.
3. export edited audio to new directory.

## Demo

Fixing the Humma Song to take out the entire unnecessary pop rap verse.
![DEMO](https://github.com/athom031/trimSilence/blob/master/Demo.png)

## Prerequisites

1. Use pip to install python files.
* https://pip.pypa.io/en/stable/installing/pydub 
2. Use pip to install pydub and use AudioSegment.
* https://pypi.org/project/pydub/
3. Make sure you install ffmpeg or libav for dealing with mp3.
* https://ffmpeg.org/download.html
* https://libav.org/

## Getting Started

1. Update global variables with desired directories.
2. Run splitscript and enter the song name along with the time stamps.
```
    python entryWidget.py
```
3. Click the button to run app or exit the window to close the program

## Warnings 
To avoid following runtime warning:
```
RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)
```
run script with -W ignore
```
python -W ignore entryWidget.py
```

## Inspiration

Not being able to do it easily for so many of my favorite songs.