import madmom
import time
import numpy as np
import librosa
import librosa.display
from scipy import signal
import math
import ruptures as rpt
import time
import matplotlib.pyplot as plt
import changefinder
from pandas import Series


def findChangePoints(ts, r, order, smooth):
    '''
       r: Discounting rate
       order: AR model order
       smooth: smoothing window size T
    '''
    cf = changefinder.ChangeFinder(r=r, order=order, smooth=smooth)
    ts_score = [cf.update(p) for p in ts]
    plt.figure(figsize=(16, 4))
    plt.plot(ts)
    plt.figure(figsize=(16, 4))
    plt.plot(ts_score, color='red')
    return (ts_score)


audio_file = "wish_you_were_here.wav"
audio_rawData, sr = librosa.load(audio_file)
tempo, beats = librosa.beat.beat_track(audio_rawData, sr=sr, units='time')
#proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100)
#act = madmom.features.onsets.RNNOnsetProcessor()(audio_file)
#onsets = proc(act)
audio_rawData = audio_rawData.flatten()
#print(audio_rawData.shape)


#segmentation (window length 1024, length between windows 512)
audio_length = audio_rawData.shape[0]
num_windows = math.ceil(audio_length/512)
seg_signal_matrix = np.zeros((num_windows, 1024))
for i in range(num_windows):
    curr_window = audio_rawData[i*512 : i*512+1024]
    seg_signal_matrix[i, :len(curr_window)] = curr_window
#corresponding time to windows in seconds
time_seg = (np.arange(0, num_windows) * 512) / sr

#amplitude analysis(rms):
rms = np.zeros(num_windows)
for i in range(num_windows):
    curr_window = seg_signal_matrix[i]
    curr_rms = np.sqrt(np.sum(np.square(curr_window))/1024)
    rms[i] = curr_rms

rms_std = np.std(rms)
rms_peaks, _ = signal.find_peaks(rms)#, threshold=rms_std)
#plot rms and raw signal


'''
x = np.arange(0,len(rms), 1)
plt.plot(x, rms)
plt.plot(rms_peaks, rms[rms_peaks], "x")
plt.show()
print(len(rms_peaks))
'''

#power changing in rms:
power_change = np.zeros(num_windows - 1)
for i in range(num_windows - 1):
    power_change[i] = abs(rms[i+1] - rms[i])

weighted_time = np.zeros(num_windows - 1)
for i in range(math.ceil((num_windows-100))):
    curr_data = rms[i:i+100]
    curr_mean = np.mean(curr_data)
    curr_std = np.std(curr_data)
    for j in range(len(curr_data)):
        if abs(rms[i+j] - curr_mean) > 4*curr_std:
            weighted_time[i+j] += 1
'''
for i in range(len(weighted_time)):
    if (weighted_time[i]) >= 37:
        print(time_seg[i])
'''

algo = rpt.Pelt(model="rbf").fit(rms)
result = algo.predict(pen=10)
result = result[:len(result)-2]
changing_points = time_seg[result].tolist()
print(changing_points)


index_list = []
distance = (tempo/60) * 16
flag = False
for i in range(len(changing_points) - 1):
    if changing_points[i + 1] - changing_points[i] < distance:
        index_list.append(changing_points[i+1])
        flag = True
    else:
        if flag:
            index_list.pop(len(index_list) - 1)
            flag = False
for index in index_list:
    changing_points.remove(index)

#a = [1805, 2505, 3375, 3545, 3670, 3750, 3825, 3920, 3985, 4200, 4300, 4385, 4460, 4555, 4625, 5835, 5860, 5910, 6035, 6145, 6875, 7555, 7725, 7780, 8020, 8770, 8830, 8950, 9925, 9975, 10260, 10550, 10765, 10920, 11690, 12025, 12300]
print(changing_points)
sliding_index = []
window_power = 0
for i in range(len(result) - 1):
    if i == 0:
        window1 = rms[:result[i]]
        window2 = rms[result[i]:result[i+1]]
    else:
        window1 = rms[result[i-1]::result[i]]
        window2 = rms[result[i]:result[i + 1]]
    mean1 = np.mean(window1)
    mean2 = np.mean(window2)
    if abs(mean2 - mean1) >= rms_std:
        sliding_index.append(result[i])

print(time_seg[sliding_index])

frames = range(len(rms))
t = librosa.frames_to_time(frames, hop_length=512)
plt.figure(figsize=(15,17))
librosa.display.waveplot(audio_rawData)
plt.plot(t,rms,color = "r")
plt.ylim(-1,1)
for time in changing_points:
    plt.axvline(x = time, color = "g")
plt.show()



#change finder test
segments = findChangePoints(rms, 0.01, 3, 5)
ts_change_loc2 = Series(segments).nlargest(20)
ts_change_loc2 = ts_change_loc2.index
print(time_seg[ts_change_loc2])

