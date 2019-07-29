'''
Author: Alex Thomas
Date:7/29/2019 - xml configuration
Script that looks at a folder of mp3 files
Each file
 Split the file into utterances
 Choose the utterance that is the longest
 Output that file into destination directory
'''


import sys #sys exit
import argparse #how we parse the arguments
import os #most of the stuff dealing with path and directory
from pydub import AudioSegment #main library used to analyze file
import shutil


WAV_DIRECTORY         = r'C:\Users\athomas\Desktop\trimSilence\MusicFiles'
DESTINATION_DIRECTORY = r'C:\Users\athomas\Desktop\trimSilence\EditedMusicFiles'
UTT_DIRECTORY         = r'C:\Users\athomas\Desktop\trimSilence\UttFiles'
ADDED_SILENCE_MS      = 300
SILENCE_BTWN_MS       = 750
NOISE_INSTANCE_DBFS   = -30
SILENCE_INSTANCE_DBFS = -54

SIL_BUFFER = AudioSegment.silent(duration = ADDED_SILENCE_MS)


def startOfUtterance(sound_file, start_point):
    for i in range(start_point, len(sound_file)): #iterate from start point to end of file
        if(sound_file[i].dBFS > NOISE_INSTANCE_DBFS): #upon first find of talking noise
            return i    #return utterance start
    return -1       #from start_point to end of file no noise, then no utterance


def endOfUtterance(sound_file, ut_start):
    i = ut_start #get start from startOfUtterance function
    while(i < len(sound_file)): #should stop at end of sound_file
        if(sound_file[i].dBFS < SILENCE_INSTANCE_DBFS):     #possible end of file
            noise = False #T/F value for noise after possible end of utterance
            j = 1
            while(j < SILENCE_BTWN_MS):
                if(j+i > len(sound_file)):
                    return len(sound_file) - 1
                elif(sound_file[j + i].dBFS > NOISE_INSTANCE_DBFS):  #noise is detected
                    noise = True        #set T/F value to true
                    i += j              #i -> j+i saves calculation
                    j = SILENCE_BTWN_MS #will not enter while loop again now
                else:
                    j += 1  #if no noise increment
            if (noise == False): # still false means no instance of noise SILENCE_BTWN_MS amaount
                return(i)
        i += 1
    return len(sound_file) - 1


def findAllUtterances(sound_file, file_name):
    ut_count = 1
    i = 0
    max_audio = AudioSegment.silent()
    try:
        os.mkdir(UTT_DIRECTORY + '\\' + file_name)  # make a folder to put all splits for each mp3 file
    except:
        return

    while (i < len(sound_file)):
        ut_start = startOfUtterance(sound_file, i)
        if (ut_start == -1):  # if start of utterance finds no start till end of file
            break
        ut_end   = endOfUtterance(sound_file, ut_start)
        new_audio = SIL_BUFFER + sound_file[ut_start:ut_end] + SIL_BUFFER #creates new audio file

        if (len(new_audio) > len(max_audio)):
            max_audio = new_audio

        new_audio.export(file_name + '_%s.mp3' % ut_count, format="mp3") #names audio file with utt_count
        os.rename(os.path.abspath(file_name + '_%s.mp3' % ut_count), UTT_DIRECTORY + '\\' + file_name + '\\' + file_name + '_Utterance_%s.mp3' % ut_count)
        i = ut_end #move i along properly
        ut_count += 1 #increment ut_count

    max_audio.export(file_name + '_sil.mp3', format = "mp3")
    os.rename(os.path.abspath(file_name + '_sil.mp3'), DESTINATION_DIRECTORY + '\\' + file_name + '_sil.mp3')


def main():
    for filename in os.listdir(WAV_DIRECTORY):  # goes through every raw mp3 file
        file_name = filename[:-4]  # get the filename without the '.mp3'
        sound_file = AudioSegment.from_mp3(WAV_DIRECTORY + "\\" + filename)
        findAllUtterances(sound_file, file_name)


if __name__ == '__main__':
    sys.exit(main())