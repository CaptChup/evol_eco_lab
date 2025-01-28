#date: - 11/09/2024
#author: - srini

#outputs a signal of desired frequency, syllable duration, inter-syllable period and inter-chirp period using the given audio envelopes

#loading necessary libraries
import matplotlib.pyplot as plt
import librosa
import librosa.display
import IPython.display as ipd
import scipy.io
from scipy.io.wavfile import write
import json
import numpy as np
import os

#defining necessary functions

#concatenates given np arrays with an np array of zeros (padding, called "gap" in this case) of specified length sandwiched between each of them
def mash_audio_signals(sylls, gap, sr):
    signal = np.empty(0)
    gap_list = np.zeros(int(gap*sr)) 
    for i in range (0, len(sylls)):
        signal = np.concatenate((signal, sylls[i], gap_list))
    return signal[:-int(gap*sr)]

#returns a raw string (required to parse through file paths that contain "/" character)
def to_raw_string(s):
    # Remove surrounding double quotes if they exist
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]   
    # Escape backslashes
    s = s.replace("\\", "\\\\")

    return s


#main
frequency = float(input("Enter the required frequency for the signal\n"))
n = int(input("Enter the number of syllables\n"))
print("Enter the file paths to the envelopes one by one\n")
file_paths = []
for i in range (0,n):
    file_paths.append(to_raw_string(input()))
inter_syllable_duration = float(input("Enter the required inter-syllable duration in milli seconds\n"))/1000
inter_chirp_duration = float(input("Enter the required inter-chirp duration in centi-seconds\n"))/100
number_of_chirps = int(input("Enter the number of chirps required\n"))
sr = int(input("Enter the required sample rate\n"))
timeres = 1/sr
timeline = np.linspace(0, 1, num = int(sr*1), endpoint=False)
sine_wave= np.sin(2*np.pi*frequency*timeline)

#loading necessary envelopes
envelopes = []
for i in range(0, len(file_paths)):
    with open(file_paths[i], 'r') as i:
        i = json.load(i)
        envelopes.append(i)

syllables_list = []
for i in range(0, len(envelopes)):
    syllables_list.append(envelopes[i]*sine_wave[:len(envelopes[i])])

syn_chirp_list = []
for i in syllables_list:
    syn_chirp_list.append(i)

syn_chirp = mash_audio_signals(syn_chirp_list,inter_syllable_duration,sr) #generates a synthetic chirp by concatenating syllables using specified inter-syllables duration

syn_signal_list = []
for i in range(0, number_of_chirps):
    syn_signal_list.append(syn_chirp)

syn_signal = mash_audio_signals(syn_signal_list,inter_chirp_duration,sr) #generates a synthetic signal by concatenating chirps using specified inter-chirp duration

syn_signal_audio = np.int16(syn_signal * 32767)
write(r"D:\Chup\academic\niser\eco-evo_lab\codes\gryllodes_signal_generator\syn_signals\syn_signal_192k_audio.wav", sr, syn_signal_audio)