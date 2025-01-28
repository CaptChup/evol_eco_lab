#date: - 11/09/2024
#author: - srini

#outputs average max amplitude envelopes of the given wav files

#importing necessary packages

import matplotlib.pyplot as plt
import librosa
import librosa.display
import IPython.display as ipd
import scipy.io
import json
import numpy as np
import os
import math

#defining necessary functions

#returns the max amplitude envelope of a given .wav file
def amplitude_envelope(signal, frame_size, hop_length):
    amplitude_envelope = []
    # calculate amplitude envelope for each frame
    for i in range(0, len(signal), hop_length): 
        amplitude_envelope_current_frame = max(signal[i:i+frame_size])
        amplitude_envelope.append(amplitude_envelope_current_frame)
    return amplitude_envelope

#saves a given list as a .json (JSON is the universally compatible python format) file to the specified directory
def save_to_JSON(directory, array, name):
    array = [float(x) for x in array]  
    file_path = os.path.join(directory, name)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(array, file, indent=4)  # indent for pretty-printing
    print("Saved to :", directory)

#return a raw string (required to properly parse through file paths that contain "/" character)
def to_raw_string(s):
    # Remove surrounding double quotes if they exist
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]   
    # Escape backslashes
    s = s.replace("\\", "\\\\")
    
    return s

#computes the average max amplitude envelope given n number of max amplitude envelopes (Note:- this is tricky because the length of each of the max amplitude envelopes can differ, hecne padding is required)
def average(envelopes):
    lengths = []
    for i in envelopes:
        lengths.append(len(i))
    avg_len = int(sum(lengths)/len(lengths))
    if(len(envelopes[0]) >= avg_len):
        average_envelope = np.array(envelopes[0][math.ceil((len(envelopes[0]) - avg_len)/2):math.ceil((len(envelopes[0]) + avg_len)/2)])
    else:
        average_envelope = np.concatenate([np.zeros(math.floor((avg_len - len(envelopes[0]))/2)), np.array(envelopes[0]), np.zeros(math.ceil((avg_len - len(envelopes[0]))/2))])
    for i in envelopes:
        if(len(i) >= avg_len):
            average_envelope = (average_envelope + np.array(i[math.ceil((len(i) - avg_len)/2):math.ceil((len(i) + avg_len)/2)]))/2
        else:
            average_envelope = (average_envelope + np.concatenate([np.zeros(math.floor((avg_len - len(i))/2)), np.array(i), np.zeros(math.ceil((avg_len - len(i))/2))]))/2
    return average_envelope/len(envelopes)

#main
#A good frame size for 192kHz recording is 30 (found through trial and error) and hop length of 4 allows you to export sample at 48kHz. (Note:- envelope size depends only on hop length)
frame_size = int(input("Enter the required frame size\n")) 
hop_length = int(input("Enter the required hop length\n"))
#sample_rate = int(input("Enter the required sample rate\n"))
n = int(input("Enter the number of wav files to be processed\n"))
print("Enter the file paths of the wav files one by one\n")
file_paths = []
for i in range (0,n):
    file_paths.append(to_raw_string(input()))
directory_path = input("Enter the file path to the desired save directory\n")
file_name = input("Enter the desired filename for the save file\n")
files = []
for i in file_paths:
    files.append(librosa.load(i, sr = None)[0])
envelopes = []
for i in files:
    envelopes.append(np.array(amplitude_envelope(i, frame_size, hop_length)))
save_to_JSON(to_raw_string(directory_path), average(envelopes), file_name)
