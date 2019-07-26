'''
Author: Alex Thomas
Date:7/10/2019 - xml configuration
Script to split mp3 files into a folder of isolated utterances.
Loosely inspired by Kevin Chuang's audiosplit.py program.
'''
import sys #sys exit
import argparse #how we parse the arguments
import os #most of the stuff dealing with path and directory
from pydub import AudioSegment #main library used to analyze file
import shutil

WAV_DIRECTORY         = r'C:\Users\athomas\Desktop\MusicFiles'
DESTINATION_DIRECTORY = r'C:\Users\athomas\Desktop\SilenceLevels'
FINAL_DIRECTORY       = r'C:\Users\athomas\Desktop\EditedMusicFiles'
ADDED_SILENCE_MS      = 300#int(data[varNames.index('added_silence_ms')].text)
SILENCE_BTWN_MS       = 750#int(data[varNames.index('silence_btwn_ms')].text)
NOISE_INSTANCE_DBFS   = -30#int(data[varNames.index('noise_instance_dBFS')].text)
SILENCE_INSTANCE_DBFS = -54#int(data[varNames.index('silence_instance_dBFS')].text)

def startOfUtterance(sound_file, start_point):
    for i in range(start_point, len(sound_file)):
    #iterate from start point to end of file
        if(sound_file[i].dBFS > NOISE_INSTANCE_DBFS):
        #upon first find of talking noise
            return(i - ADDED_SILENCE_MS)
            #return silence amount index before noise
    #if no noise from start point to end of file then signify no utterance
    return -1


def endOfUtterance(sound_file, ut_start):
    #we get the start of utterance from previous function
    i = ut_start + ADDED_SILENCE_MS
    #start at true start of noise
    while(i < len(sound_file)):
    #should stop at end of sound_file
        enter_loop = False
        # this is the loop that checks if possible end of utterance is desired
        if(sound_file[i].dBFS < SILENCE_INSTANCE_DBFS):
            #possible end of file
            enter_loop = True
            #so we should enter loop at this index
        if (enter_loop):
            #loop that tests if index is the end of utterance
                #if added_silence following possible value is just silence then yeah not an utterance
            noise = False
            #T/F value for noise in silence_btwn value range after possible end
            j = 0
            while(j < SILENCE_BTWN_MS):
                if(sound_file[j + i].dBFS > NOISE_INSTANCE_DBFS):
                    #noise is detected
                    noise = True
                    #set T/F value to true
                    i += j
                    #i should then go to j+i value because saves calculation
                    j = SILENCE_BTWN_MS
                    #want to exit loop because we have found noise
                else:
                    j += 1
                    #if no noise detected have to increment j manually because it is a while loop
            #at this point it has gone silence_btwn value following possible value without noise
            #therfore this is the end of the utterance
            if (noise == False):
                #noise was never changed to true then
                return(i + ADDED_SILENCE_MS)
                #buffer of added_silence value following end of utterance
        i += 1
    return len(sound_file) - 1


def findAllUtterances(sound_file, file_name):
    ut_count = 1
    i = 0
    os.mkdir(DESTINATION_DIRECTORY + '\\' + file_name) #make a folder to put all splits for each mp3 file
    while (i < len(sound_file)):
        ut_start = startOfUtterance(sound_file, i)
        ut_end   = endOfUtterance(sound_file, ut_start)
        if(ut_start == -1): #if start of utterance finds no start till end of file
            break
        new_audio = sound_file[ut_start:ut_end] #creates new audio file
        new_audio.export(file_name + '_%s.mp3' % ut_count, format="mp3") #names audio file with utt_count
        os.rename(os.path.abspath(file_name + '_%s.mp3' % ut_count), DESTINATION_DIRECTORY + '\\' + file_name + '\\' + file_name + '_Utterance_%s.mp3' % ut_count)
        #put mp3 file in the proper folder in destination_directory
        i = ut_end #move i along properly
        ut_count += 1 #increment ut_count
    max = -1
    for file in os.listdir(DESTINATION_DIRECTORY + '\\' + file_name):
        sound_file = AudioSegment.from_mp3(DESTINATION_DIRECTORY + "\\" + file_name + '\\' + file)
        if(len(sound_file) > max):
            max = file

    os.rename(DESTINATION_DIRECTORY + "\\" + file_name + '\\' + max, FINAL_DIRECTORY + '\\' + file_name + '.mp3')
    shutil.rmtree(DESTINATION_DIRECTORY + '\\' + file_name)



def main():
    #error if destination directory is not empty
    if (len(os.listdir(DESTINATION_DIRECTORY)) == 0): #checks if destination directory is empty
        for filename in os.listdir(WAV_DIRECTORY): #goes through every raw mp3 file
            file_name = filename[:-4] #get the filename without the '.mp3'
            sound_file = AudioSegment.from_mp3(WAV_DIRECTORY + "\\" + filename)
            #create a audio segment variable type of the mp3 file from raw folder
            #we moved away from .mp3 read because now we have the .dBFS component used to measure silence and noise
            findAllUtterances(sound_file, file_name)
            #sound_file            -> AudioSegment object type created for raw mp3 file
            #file_name             -> filename without the '.mp3'
    else: #otherwise don't enter program and print error message
        print("ERROR: Destination Directory entered is not empty and must be for a proper Split.")


if __name__ == '__main__':
    sys.exit(main())