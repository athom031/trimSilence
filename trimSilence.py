'''
Author: Alex Thomas

Cleanup Audio, trim silence and normalize audio
'''

import json
import sys 
import argparse 
import shutil                  # for space delete utterance file after completion 
import os                      # make directory and paths for new utterence folders
from pydub import AudioSegment # Open Source Python Library to process Audio as array


#---------------------------- Open config.json and assign global variables ----------------------------#
with open('config.json') as config_file:
    data = json.load(config_file)

MUSIC_DIR             = data['music_directory']
TEMP_DIR              = data['temp_directory']
DEST_DIR              = data['destination_directory']
ADDED_SILENCE_MS      = data['added_silence_ms']
SILENCE_BTWN_MS       = data['silence_btwn_ms']
NOISE_INSTANCE_DBFS   = data['noise_instance_dBFS']
SILENCE_INSTANCE_DBFS = data['silence_instance_dBFS']
NORMALIZE_DBFS        = data['normalize']
SYSTEM                = data['system_type']


if SYSTEM == "mac":
    dirChar = "/"
else:
    dirChar = "\\"

SIL_BUFFER = AudioSegment.silent(duration = ADDED_SILENCE_MS)

#------------------------------------------------------------------------------------------------------#


#--------------------------------------------- Normalize ----------------------------------------------#

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

#------------------------------------------------------------------------------------------------------#


#-------------------------------------- Utterence Slice Indices ---------------------------------------#
def startOfUtterance(sound_file, start_point):
    for i in range(start_point, len(sound_file)):
        if(sound_file[i].dBFS > NOISE_INSTANCE_DBFS):
        #found starting instance of noise
            return i
            #return silence amount index before noise
    return -1
    #if no noise from start point to end of file then signify no utterance


def endOfUtterance(sound_file, ut_start):
    i = ut_start
    #we get the start of utterance from previous function and adjust 
    while(i < len(sound_file)):
    
        enter_loop = False
        if(sound_file[i].dBFS < SILENCE_INSTANCE_DBFS):
            #possible end of file
            enter_loop = True
        if (enter_loop):
            #test if index is the end of utterance
            noise = False
            j = 0
            while(j < SILENCE_BTWN_MS):
                if(sound_file[j + i].dBFS > NOISE_INSTANCE_DBFS):
                    #noise is detected
                    noise = True
                    
                    i += j
                    #i should then go to j+i value 
                    #OPTIMIZE CALCULATIONS
                    
                    j = SILENCE_BTWN_MS
                    #forces exit of loop

                else:
                    j += 1
                
            if (noise == False):
                return i 
                #buffer of added_silence value following end of utterance
        i += 1
    return len(sound_file) - 1 
    #if sound occurs untill end, soundfiles end is the end of the utterence

#------------------------------------------------------------------------------------------------------#


def findAllUtterances(sound_file, file_name):
    ut_count = 1
    i = 0
    max_audio = AudioSegment.silent()
    try:
        os.mkdir(TEMP_DIR + dirChar + file_name)  # make a folder to put all splits for each mp3 file
    except:
        return

    while (i < len(sound_file)):
        ut_start = startOfUtterance(sound_file, i)
        if (ut_start == -1):  # if start of utterance finds no start till end of file
            break
        ut_end   = endOfUtterance(sound_file, ut_start)
        
        #TERNARY: (if_test_is_false, if_test_is_true)[test]
        ut_start =  (0, ut_start - 300)[ut_start > 300]
        ut_end   =  (len(sound_file - 1), ut_end + 300)[ut_end + 300 < len(sound_file)]
        new_audio = sound_file[ut_start:ut_end]

        if (len(new_audio) > len(max_audio)):
            max_audio = new_audio

        new_audio.export(file_name + '_%s.mp3' % ut_count, format="mp3") #names audio file with utt_count
        os.rename(os.path.abspath(file_name + '_%s.mp3' % ut_count), 
                TEMP_DIR + dirChar + file_name + dirChar + file_name + '_Utterance_%s.mp3' % ut_count)
        i = ut_end #move i along properly
        ut_count += 1 #increment ut_count

    max_audio.export(file_name + '_final.mp3', format = "mp3")
    os.rename(os.path.abspath(file_name + '_final.mp3'), DEST_DIR + dirChar + file_name + '.mp3')


def main():
    for filename in os.listdir(MUSIC_DIR):  # goes through every raw mp3 file
        if(filename[-4:] != '.mp3'):
            continue #ignore .DS_store on mac or likewise for windows
        
        file_name = filename[:-4]  # get the filename without the '.mp3'
        sound_file = AudioSegment.from_mp3(MUSIC_DIR + dirChar + filename)
        normalized_sound = match_target_amplitude(sound_file, NORMALIZE_DBFS)
        i = 0
        findAllUtterances(normalized_sound, file_name)
    
    shutil.rmtree(TEMP_DIR) # will clear ut file for space (treated as temp directory)
    os.mkdir(TEMP_DIR)      # delete these lines if not wanted


if __name__ == '__main__':
    sys.exit(main())