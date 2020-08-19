# Audio Silence Trimmer and Level Normalizer Delete from Middle

Music is such a beautiful thing.

I grew up with Indian music and when I was growing up songs were 10 minutes long.

Literally.

10 minutes with 2 minutes being a part in the movie where the storyline is progressing and it is just instrumentals.

Now that isn't what you want for your road trip.

Or when you grow up a little bit and now every Bollywood song has an annoying rap verse for no reason.

Let's get rid of that.


##### Python Desktop Widget to Take out sections of Music

1. Search Repository for User Suggested song.
2. Convert time index of start and stop to ms.
3. Export the desired music segment to new directory.


## Demo

Fixing the Humma Song to take out the entire unnecessary pop rap verse.
![DEMO](https://github.com/athom031/SubMusic/blob/master/Demo.png)

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