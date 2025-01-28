#date: - 11/09/2024
#author: - srini

#generates a collection of slices of audio from a given .wav file that resembles a sample .wav file and represents the result using a waveform plot

#importing necessary packages
import scipy.io
from scipy.io.wavfile import write
import librosa
import json
import numpy as np
import os
import matplotlib.pyplot as plt

#defining necessary functions

#returns a collection of slices matching the given sample .wav file within epsilon error margin
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

#returns indices corresponding to selection position
def find_selection_position(target_audio, selection_audio):
    target_len = len(target_audio)
    selection_len = len(selection_audio)
    
    # Iterate through the target audio to find where the selection starts
    for i in range(target_len - selection_len + 1):
        if np.allclose(target_audio[i:i + selection_len], selection_audio, atol=1e-4):
            return i
    return -1  # If the selection is not found

#generates a waveform plot of the given .wav file and highlights the selected slices using an overlayed transparent red rectangle
def plot_waveform_with_highlights(target_file, selection_arrays, zoom_factor=1.0):
    # Load the target audio file
    target_audio, target_sr = librosa.load(target_file, sr=None)
    
    # Prepare the plot for the waveform
    plt.figure(figsize=(18, 8))  # Increased figure size for better visibility
    time_axis = np.linspace(0, len(target_audio) / target_sr, len(target_audio))
    
    # Plot the entire waveform of the target audio first
    plt.plot(time_axis, target_audio, label='Target Audio', color='cyan', lw=1, alpha = 0.5)
    
    # color for the regions corresponding to each selection
    color = ['red']
    
    # Find and highlight each selection region by overlaying it
    for i, selection in enumerate(selection_arrays):
        start_sample = find_selection_position(target_audio, selection)  # Find start position in samples
        if start_sample == -1:
            print(f"Selection {i+1} not found in target audio.")
            continue  # Skip this selection if it isn't found
        
        end_sample = start_sample + len(selection)  # End position of the selection in samples
        
        start_time = start_sample / target_sr  # Convert start sample to time (seconds)
        end_time = end_sample / target_sr  # Convert end sample to time (seconds)
        
        # Add a semi-transparent rectangle overlay for each selection
        plt.axvspan(start_time, end_time, color=color[i % len(color)], alpha=0.5, label=f'Selection {i+1}')
    
    # Adjust x-axis limit for zoom
    total_duration = len(target_audio) / target_sr
    zoomed_duration = total_duration * zoom_factor
    plt.xlim(0, zoomed_duration)  # Set x-axis to show a portion based on zoom_factor
    
    plt.title('Waveform with Highlighted Selection Regions')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.tight_layout()  # Ensures no overlap in labels and plot
    plt.show()

#returns a raw string (required for properly parsing through file paths that contain "/" character)
def to_raw_string(s):
    # Remove surrounding double quotes if they exist
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]   
    # Escape backslashes
    s = s.replace("\\", "\\\\")

    return s

#main

target_file_path = input("Enter target audio file path\n")
sample_file_path = input("Enter sample audio file path\n")
epsilon = float(input("Enter the matching parameter epsilon\n"))


target = librosa.load(to_raw_string(target_file_path), sr = None)[0]
sample = librosa.load(to_raw_string(sample_file_path), sr = None)[0]

collection = get_slice(sample, target, epsilon)

print(len(collection))
plot_waveform_with_highlights(to_raw_string(target_file_path), collection)