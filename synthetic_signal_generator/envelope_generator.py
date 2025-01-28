#date: - 11/09/2024
#author: - srini

#outputs max amplitude envelopes of the given wav files

import matplotlib.pyplot as plt
import librosa
import librosa.display
import IPython.display as ipd
import scipy.io
import json
import numpy as np
import os

#defining necessary functions

def amplitude_envelope(signal, frame_size, hop_length):
    """Calculate the amplitude envelope of a signal with a given frame size and hop length."""
    amplitude_envelope = []
    
    # calculate amplitude envelope for each frame
    for i in range(0, len(signal), hop_length): 
        amplitude_envelope_current_frame = max(signal[i:i+frame_size])
        amplitude_envelope.append(amplitude_envelope_current_frame)
    return amplitude_envelope

def save_to_JSON(directory, array, name):
    array = [float(x) for x in array]  
    file_path = os.path.join(directory, name)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(array, file, indent=4)  # indent for pretty-printing
    print("Saved to :", directory)

def to_raw_string(s):
    # Remove surrounding double quotes if they exist
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]   
    # Escape backslashes
    s = s.replace("\\", "\\\\")
    
    return s

#main
#A good frame size for 192kHz recording is 30 and hop length of 4 allows you to export sample at 48kHz
frame_size = int(input("Enter the required frame size\n")) 
hop_length = int(input("Enter the required hop length\n"))
#sample_rate = int(input("Enter the required sample rate\n"))
n = int(input("Enter the number of wav files to be processed\n"))
print("Enter the file paths of the wav files one by one\n")
file_paths = []
for i in range (0,n):
    file_paths.append(to_raw_string(input()))
files = []
for i in file_paths:
    files.append(librosa.load(i, sr = None)[0])
envelopes = []
for i in files:
    envelopes.append(amplitude_envelope(i, frame_size, hop_length))
for i in range (0, len(envelopes)):
    save_to_JSON(r"D:\Chup\academic\niser\eco-evo_lab\codes\gryllodes_signal_generator\envelopes", envelopes[i], "syll_192k_" + str(i+1) + ".json")
    # save_to_JSON(r"D:\Chup\academic\niser\eco-evo_lab\codes\gryllodes_signal_generator", envelopes[i], "chirp1_" + str(i+1) + ".json")
