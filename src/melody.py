from scipy import signal
import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
from utils import *
from math import log


# sr, song = scipy.io.wavfile.read('../Songs/river_flows_in_you_mono.wav')
sr, song = scipy.io.wavfile.read('../Songs/fur_elise.wav')
# sr, song = scipy.io.wavfile.read('../Songs/Deadmau5 - Strobe (Evan Duffy Piano Cover).wav')
song = song[:5*sr]
plt.plot(song)
plt.show()

# # take first ten seconds  ## THIS WAS A PLAYGROUND FOR LOOKING AT DIFFERENT WINDOWS
# song = song[sr:10*sr]
#
# plt.plot(song)
# plt.show()
# hop = 1024
# sample = song[hop*4:hop*5]
# plt.plot(sample)
# plt.show()
#
# window = scipy.signal.windows.hann(hop)
# sample = window * sample
# plt.plot(sample)
# plt.title('After window applied')
# plt.show()
# # x = np.fft.fft(sample)
# length = int(len(song)//hop)
# print(length)
# peaks = np.zeros(length)
# j = 0
# for i in range(25*hop, len(song), hop):
#     sample = song[i:i+hop]
#     if len(sample) == hop:
#         sample = sample * window
#         x = np.fft.fft(sample)
#         plt.plot(abs(x))
#         plt.show()
#         x_peaks = signal.find_peaks(x[:int(len(x)//2)], height =60000)
#         print(x_peaks)
#         # print(np.argmax(x))
#         # peaks[j] = np.argmax(x)
#     j += 1
#     break
#
# # plt.plot(l)
# # print(np.argmax(x))
# print(peaks)
# print(len(peaks))
# # plt.show()

print(len(song)/128)
print(len(song)/sr)
# 128 is each hop , 8192 is how many freq bins there is
f, t, Zxx = signal.stft(song, fs=sr, nperseg=2048, nfft=8192)


# TODO: Move this a into my_stft function
win_len = 2048
w = scipy.signal.get_window("hann", win_len)
hop_size = 128
short = np.zeros(shape=(4096, (len(song)-win_len)//128))
totes = 0

for i in range(0, len(song)-win_len, 128):
    # TODO: Fix the normalisation peak picking
    windowed = song[i:i+win_len]*w
    this = np.fft.fft(windowed, n=8192)
    totes = np.sum(windowed)
    print(i//128)
    this = np.abs(this[:len(this)//2])
    this = 2*(this/totes)
    short[:, (i//128)-1] = this
# This is the peak picking for
print(short.shape)
# for j in range(len(short[0])):
#     short[:, j] = 2*(short[:, j]/totes)

short = log_compression(short)
# l = np.array(l)

# Parabolic interpolation


def parabolic_ip(freq):
    # TODO : Fix this, too slow. Look at book again
    for p in range(1, len(freq)-1):
        if freq[p - 1] > 0 and freq[p] > 0 and freq[p+1] > 0:
            a1 = 20*log(freq[p-1], 10)
            a2 = 20*log(freq[p], 10)
            a3 = 20*log(freq[p+1], 10)
            print(a1, a2, a3)
            d = .5*((a1-a3)/(a1-(2*a2)+a3))
            print(d)
            freq[i] = a2 - (d/4)*(a1-a3)
    return freq
# print(len(short[:, 1]))
# parabolic_ip(abs(short[:, 1]))


# for i in range(len(short[0])):
#     parabolic_ip(abs(short[:, 1]))
#

print("Window size in ms: ", (2048/sr)*1000)
# f, t, Zxx = signal.stf
print(len(Zxx[0]), "Length of STFT")

Zxx = log_compression(Zxx)
# print(Zxx[0])
peaks = np.empty(shape=Zxx.shape)
# for i in range(len(Zxx[0])):
#     test = np.sum((song[i:i+len(w)])*w)
#     # Zxx[:, i] = np.log(Zxx[:, i] * y + 1)
#     peaks[:, i] = 2*(np.abs(Zxx[:, i])/test)

# new_f = log_freq_spec(Zxx)
new_ref = refined_log_freq_spec(short)
# new_ref = log_compression(short)

# # plt.pcolormesh(t, f, np.log(np.abs(Zxx)), vmin=1)
# plt.pcolormesh(np.abs(new_f))
# plt.title('Logged')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
# #
plt.pcolormesh(np.abs(new_ref))
plt.title('Refined Logged')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

plt.pcolormesh(np.abs(short))
plt.title('MY BOY')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()


plt.pcolormesh(np.abs(Zxx))
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
#
plt.pcolormesh(np.abs(peaks))
plt.title('PEAKS')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
# d = note_pitch_midi()
# for key in d:
#     print(key, d[key])

