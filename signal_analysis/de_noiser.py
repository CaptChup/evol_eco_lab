#date: - 16/09/2024
# author: - srini
 
#de-noise a given .wav file and output the de-noised version.  

#loading necessary packages

import matplotlib.pyplot as plt
import librosa
import librosa.display
import IPython.display as ipd
import scipy.io
import json
import numpy as np
import os

#defining necessary functions

def de_noiser(audio, multiplier, threshold):
    de_noised_audio = audio*multiplier
    for i in range (0, len(de_noised_audio)):
        if(de_noised_audio[i] < threshold):
            de_noised_audio[i] = float(0)
        else:
            pass
    de_noised_audio = de_noised_audio*(1/multiplier)
    return de_noised_audio