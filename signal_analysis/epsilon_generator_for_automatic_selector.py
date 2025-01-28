#date: - 11/09/2024
#author: - srini

#generates epsilon vs no: of selections plot for given sample and audio

import matplotlib.pyplot as plt
import librosa
import numpy as np

#defining necessary functions

#returns a tuple with three entries: (a set of all collecctions, a list of the lengths of all selections, a list of all epsilon values used)
def get_epsilon(sample, audio):
    epsilons = np.arange(0, 0.5, 0.01)
    gallery = []
    number_of_selections = []
    for i in epsilons:
        gallery.append(get_slice(sample, audio, i))
        number_of_selections.append(len(get_slice(sample, audio, i)))

    return gallery, number_of_selections, epsilons

#returns a list of suitable selections
def get_slice(sample, audio, epsilon):
    collection = [] 
    i = 0
    while i <= len(audio) - len(sample):
        selection = []  
        for j in range(len(sample)):
            if abs(abs(audio[i + j]) - abs(sample[j])) <= epsilon:
                selection.append(audio[i + j])
            else:
                selection = []  
                break
        if len(selection) == len(sample):
            collection.append(selection)
            i = i + len(sample)
        else:
            i = i + 1
    
    return collection

#returns a raw string (required for properly parsing file paths that contain "/" characters)
def to_raw_string(s):
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]   
    s = s.replace("\\", "\\\\")

    return s

#main

audio_file_path = input("Enter the audio file path\n")
sample_file_path = input("Enter the sample file path\n")

audio = librosa.load(to_raw_string(audio_file_path), sr = None)[0]
sample = librosa.load(to_raw_string(sample_file_path), sr = None)[0]

plt.figure(figsize = (15,10))
plt.plot(get_epsilon(sample, audio)[1], get_epsilon(sample, audio)[2], marker='o', color='b', label='Line')
plt.xlabel("number of selections")
plt.ylabel("epsilon")
for x, y in zip(get_epsilon(sample, audio)[1], get_epsilon(sample, audio)[2]):
    plt.text(x, y, f'({x}, {y})', fontsize=12, ha='right', va='bottom')
plt.show() 