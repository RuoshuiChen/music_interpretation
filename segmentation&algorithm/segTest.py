import madmom
import time
import numpy as np
import librosa
import librosa.display
import librosa.display as Display
from scipy import signal
import math
import ruptures as rpt
import time
import matplotlib.pyplot as plt
import changefinder
from pandas import Series
from pydub import AudioSegment
from pydub.playback import play
from time import sleep
#import pygame
from playsound import playsound
from PIL import Image, ImageDraw
import threading
from colorama import Fore, Style
#import msaf
from pygame.locals import *

def playSong(file_path):
    playsound(file_path)


audio_file = "Fleetwood Mac - The Chain-JDG2m5hN1vo.wav"

audio_rawData, sr = librosa.load(audio_file)
tempo, beats = librosa.beat.beat_track(audio_rawData, sr=sr, units='time')
beats = np.insert(beats, 0, 0)

proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100)
act = madmom.features.onsets.RNNOnsetProcessor()(audio_file)
onsets = proc(act)
onsets = np.insert(onsets, 0, 0)

onset_weight = np.zeros(onsets.shape)
for i in range(len(onsets)):
    onset_weight[i] = int(onsets[i]*sr/512)
#print(onset_weight)

#segmentation (window length 1024, length between windows 512)
audio_length = audio_rawData.shape[0]
num_windows = math.ceil(audio_length/512)
seg_signal_matrix = np.zeros((num_windows, 1024))
for i in range(num_windows):
    curr_window = audio_rawData[i*512 : i*512+1024]
    seg_signal_matrix[i, :len(curr_window)] = curr_window
#corresponding time to windows in seconds
time_seg = (np.arange(0, num_windows) * 512) / sr
rms = np.zeros(num_windows)
for i in range(num_windows):
    curr_window = seg_signal_matrix[i]
    curr_rms = np.sqrt(np.sum(np.square(curr_window))/1024)
    rms[i] = curr_rms
seg = []
time = [0]
for i in range(1, len(onset_weight)-1):
    old_window = rms[int(onset_weight[i - 1]) : int(onset_weight[i])]
    old_std = np.std(old_window)
    old_mean = np.mean(old_window)
    curr_window = rms[int(onset_weight[i]) : int(onset_weight[i+1])]
    curr_std = np.std(curr_window)
    curr_mean = np.mean(curr_window)
    if (abs(curr_mean - old_mean)) > 1.5*((old_std+curr_std)/2):
        seg.append(onset_weight[i])
        time.append(time_seg[int(onset_weight[i])])

song_thread = threading.Thread(target=playSong, args=(audio_file,))
song_thread.start()

for i in range(len(time) - 1):
    sleep(time[i+1] - time[i])
    #print("x" * int(square_rms[verticals[i]] * 100))
    #if time[i+1] - time[i] > (60/tempo)*4:
    print(time[i+1])