# import msaf
import json
import math

import librosa.display
import madmom
import numpy as np
# import pygame
from playsound import playsound
import os

def playSong(file_path):
    playsound(file_path)

dir = "music&data/funk/Locked_out_of_heaven.wav"
# for filename in os.listdir(dir):
#     f = os.path.join(dir, filename)
#     print(f)
#     audio_file = f
#     if ".wav" not in f:
#         continue
audio_file = dir
audio_rawData, sr = librosa.load(audio_file)
tempo, _ = librosa.beat.beat_track(audio_rawData, sr=sr, units='time')
b = madmom.features.beats.RNNBeatProcessor()(audio_file)
beats = madmom.features.beats.BeatTrackingProcessor(fps=100)(b)

proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100)
act = madmom.features.onsets.RNNOnsetProcessor()(audio_file)
onsets = proc(act)
onsets = np.insert(onsets, 0, 0)

# segmentation (window length 1024, length between windows 512)
audio_length = audio_rawData.shape[0]
num_windows = math.ceil(audio_length / 512)
seg_signal_matrix = np.zeros((num_windows, 1024))
for i in range(num_windows):
    curr_window = audio_rawData[i * 512: i * 512 + 1024]
    seg_signal_matrix[i, :len(curr_window)] = curr_window
# corresponding time to windows in seconds
time_seg = (np.arange(0, num_windows) * 512) / sr

# amplitude analysis(rms):
rms = np.zeros(num_windows)
for i in range(num_windows):
    curr_window = seg_signal_matrix[i]
    curr_rms = np.sqrt(np.sum(np.square(curr_window)) / 1024)
    rms[i] = curr_rms

local_min = []
for i in range(1, len(rms) - 1):
    if rms[i - 3] > rms[i - 2] > rms[i - 1] > rms[i] and rms[i] < rms[i + 1] < rms[i + 2] < rms[i + 3]:
        local_min.append(i)
local_min.insert(0, 0)
local_min.append(len(rms) - 1)
# print(len(rms), len(local_min))

# list1 = np.array(local_min[:len(local_min) - 1])
# list2 = np.array(local_min[1:])
# # print(len(list1), len(list2))
# list3 = list2 - list1

# for i in range(len(list3)):
#   if abs(list3[i]) < (tempo*8)/60:
#     target_item = list1[i]
#     local_min.remove(target_item)

square_rms = np.zeros(rms.shape)
old_max = 0
old_start = 0
for i in range(len(local_min) - 1):
    if (i == 0):
        curr_start = local_min[i]
        curr_end = local_min[i + 1]
        curr_window = rms[curr_start: curr_end]
        curr_max = np.max(curr_window)
        # start_energy = rms[curr_start]
        # end_energy = rms[curr_end]
        # square_rms[curr_start] = start_energy
        # square_rms[curr_end - 1] = end_energy
        square_rms[curr_start: curr_end] = curr_max
        old_max = curr_max
        old_start = curr_start
    else:
        curr_start = local_min[i]
        curr_end = local_min[i + 1]
        curr_window = rms[curr_start: curr_end]
        curr_max = np.max(curr_window)
        # start_energy = rms[curr_start]
        # end_energy = rms[curr_end]
        # square_rms[curr_start] = start_energy
        # square_rms[curr_end - 1] = end_energy
        curr_std = np.std(rms[old_start:curr_end])
        if np.abs(curr_max - rms[local_min[i]]) < 2 * curr_std:
            square_rms[curr_start: curr_end] = old_max
        else:
            square_rms[curr_start: curr_end] = curr_max
            old_max = curr_max
            old_start = curr_start
# print(square_rms.shape)

# rearange square wave: find two vertical line that are too close
verticals = []
for i in range(len(square_rms) - 1):
    if np.abs(square_rms[i] - square_rms[i + 1]) > 0:
        verticals.append(i + 1)

index_list1 = verticals[:len(verticals) - 1]
index_list2 = verticals[1:]
list1 = time_seg[verticals[:len(verticals) - 1]]
list2 = time_seg[verticals[1:]]
# print(len(list1), len(list2))
list3 = list2 - list1
for i in range(len(list3)):
    # !
    # !
    # !
    if list3[i] < (60 / tempo):
        curr_max = square_rms[index_list2[i] + 1]
        start = index_list1[i]
        end = index_list2[i]
        square_rms[start:end + 1] = curr_max

verticals = []
for i in range(len(square_rms) - 1):
    if square_rms[i] - square_rms[i + 1] < 0:
        verticals.append(i + 1)

# print(len(verticals))

synced_time_list = []
for i in range(len(verticals)):
    curr_timestamp = time_seg[verticals[i]]
    timestamp_array = np.zeros(onsets.shape)
    timestamp_array = curr_timestamp
    time_difference = np.abs(onsets - timestamp_array)
    curr_min = np.min(time_difference)
    synced_time_index = np.where(time_difference == curr_min)[0][0]
    synced_time = onsets[synced_time_index]
    synced_time_list.append(synced_time)

new_verticals = []
for i in range(len(synced_time_list)):
    time_array = np.zeros(time_seg.shape)
    time_array = synced_time_list[i]
    time_difference = np.abs(time_seg - time_array)
    curr_min = np.min(time_difference)
    synced_time_index = np.where(time_difference == curr_min)[0][0]
    new_verticals.append(synced_time_index)

for i in range(len(new_verticals)):
    if verticals[i] == new_verticals[i]:
        continue
    elif verticals[i] < new_verticals[i]:
        start = verticals[i]
        end = new_verticals[i]
        square_rms[start:end + 1] = square_rms[start]
    else:
        start = new_verticals[i]
        end = verticals[i]
        square_rms[start:end + 1] = square_rms[end]

'''
frames = range(len(rms))
t = librosa.frames_to_time(frames, hop_length=512)
plt.figure(figsize=(17,7))
Display.waveshow(audio_rawData)
plt.plot(t,rms,color = "y")
plt.plot(t,square_rms,color = "r")
plt.ylim(-1,1)
plt.show()
'''
# density of lines pass zero
sec_start = []
for i in range(len(square_rms) - 1):
    # postive impluse change
    if abs(square_rms[i] - square_rms[i + 1]) > 0:
        sec_start.append(i)
sec_start = np.array(sec_start) * 512
density = []
for index in sec_start:
    curr_count = 0
    if index - 10000 < 0:
        curr_seg = audio_rawData[index:index + 10000]
        for i in range(len(curr_seg) - 1):
            if (curr_seg[i] > 0 and curr_seg[i + 1] < 0) or (curr_seg[i] < 0 and curr_seg[i + 1] > 0):
                curr_count += 1
        curr_density = curr_count / 10000
    elif index + 10000 > len(audio_rawData):
        curr_seg = audio_rawData[index - 10000:index]
        for i in range(len(curr_seg) - 1):
            if (curr_seg[i] > 0 and curr_seg[i + 1] < 0) or (curr_seg[i] < 0 and curr_seg[i + 1] > 0):
                curr_count += 1
        curr_density = curr_count / 10000
    else:
        curr_seg = audio_rawData[index - 10000:index + 10000]
        for i in range(len(curr_seg) - 1):
            if (curr_seg[i] > 0 and curr_seg[i + 1] < 0) or (curr_seg[i] < 0 and curr_seg[i + 1] > 0):
                curr_count += 1
        curr_density = curr_count / 20000
    density.append(curr_density)

# calculating weights base on power
sec_start = []
for i in range(len(square_rms) - 1):
    # postive impluse change
    if abs(square_rms[i] - square_rms[i + 1]) > 0:
        sec_start.append(i)
sec_start = np.array(sec_start) * 512

power_dif = np.zeros(sec_start.shape)
window_size = 44100
for i in range(len(sec_start)):
    curr_index = int(sec_start[i])
    if curr_index - window_size < 0 or curr_index + window_size > len(audio_rawData):
        continue
    else:
        window1 = np.sqrt(np.mean(np.square(audio_rawData[int(curr_index - window_size): curr_index])))
        window2 = np.sqrt(np.mean(np.square(audio_rawData[curr_index: int(curr_index + window_size)])))
        power_dif[i] = abs(window2 - window1)
sec_start = []
sec_dif = []
for i in range(len(square_rms) - 1):
    if abs(square_rms[i] - square_rms[i + 1]) > 0:
        sec_start.append(i)
        sec_dif.append(abs(square_rms[i] - square_rms[i + 1]))
density_line = np.zeros(rms.shape)
weight_dif = power_dif * np.array(sec_dif) * np.array(density)
power_std = np.std(weight_dif)
power_mean = np.mean(weight_dif)
# print(power_dif)
segmentation = []
for i in range(len(sec_start)):
    if weight_dif[i] - power_mean >= .5 * power_std:
        density_line[sec_start[i]] = weight_dif[i] * 30
        segmentation.append([sec_start[i], weight_dif[i] * 30])
segmentation.insert(0, [0, 0])
segmentation.append([len(square_rms) - 1, 0])
segmentation = np.array(segmentation)
delete_index = []
for i in range(segmentation.shape[0] - 1):
    if segmentation[i + 1, 0] - segmentation[i, 0] <= 200:
        delete_index.append(i)
segmentation = np.delete(segmentation, delete_index, 0)

verticals = []
verticals_without_energyInfo = []
for i in range(len(square_rms) - 1):
    if abs(square_rms[i] - square_rms[i + 1]) > 0:
        verticals.append([time_seg[i], square_rms[i + 1] - square_rms[i]])
        verticals_without_energyInfo.append(time_seg[i])
# time = time_seg[verticals]
# time = np.insert(time, 0, 0)
# time = time.round(2)
# print(time)
#
# print_list = ["x"]
# energy_list = [0]
# for i in range(len(verticals)):
#     curr_list = "x" + "x" * int(square_rms[verticals[i]] * 100)
#     print_list.append(curr_list)
#     energy_list .append(1+square_rms[verticals[i]] * 100)
# print_list.insert(0,"x")
#song_thread = threading.Thread(target=playSong, args=(audio_file,))
# song_thread.start()
'''
for i in range(len(time_seg) - 1):
    if i in verticals:
        print(Fore.RED + print_list[i])
        print(Style.RESET_ALL)
    else:
        print(print_list[i])
    sleep(time_seg[i+1] - time_seg[i])
'''
final_time_seg = []
for i in range(len(segmentation)):
    final_time_seg.append(time_seg[int(segmentation[i][0])])
    segmentation[i][0] = time_seg[int(segmentation[i][0])]
segmentation = segmentation.tolist()
print(segmentation)

beats = beats.tolist()
info_dict = {"segmentation": segmentation, "verticals": verticals, "beats": beats, "tempo":tempo}
json_object = json.dumps(info_dict)
file_name = audio_file.replace(".wav", "") + ".json"
with open(file_name, "w") as outfile:
    outfile.write(json_object)
# for i in range(len(final_time_seg) - 1):
#     sleep(final_time_seg[i + 1] - final_time_seg[i])
#     # print("x" * int(square_rms[verticals[i]] * 100))
#     # if time[i + 1] - time[i]:
#     #     #print("x" + "x" * int(square_rms[verticals[i]] * 100))
#     #     if (i > 5):
#     #         if abs(sum(energy_list[i-5:i]) - sum(energy_list[i:i+5])) > 2*statistics.stdev(energy_list[i-5:i+5]):
#     #             print(Fore.RED + print_list[i+1])
#     #             print(Style.RESET_ALL)
#     #         else:
#     #             print(print_list[i + 1])
#     print("x")
#
#     # if square_rms[verticals[i]] - square_rms[verticals[i] + 1] < 0:
#     #     print("up" + "up"*int(square_rms[verticals[i]]*100))
#     # else:
#     #     print("dn" + "dn"*int(square_rms[verticals[i]]*100))
#
#     # sleep(onsets[i+1] - onsets[i])
#     # print(onsets[i])
