import scipy.io.wavfile as wav
import numpy as np
import librosa as lb
from matplotlib import pyplot as plt

rate, data = wav.read("hello.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

mfcc = lb.feature.mfcc(process, rate, n_mfcc = 13, n_fft = int(rate * 0.025), hop_length = int(rate * 0.01))

plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.title("MFCC")
plt.plot(mfcc[0])
plt.plot(mfcc[1])
plt.plot(mfcc[2])

#p must be >=3 and is a odd can't figure out why :(
delta_mfcc = lb.feature.delta(mfcc, 3)

plt.subplots_adjust(hspace = 0.5)
plt.subplot(3, 1, 2)
plt.title("Delta_MFCC")
plt.plot(delta_mfcc[0])
plt.plot(delta_mfcc[1])
plt.plot(delta_mfcc[2])

#p must be >=3 and is a odd can't figure out why :(
double_delta_mfcc = lb.feature.delta(delta_mfcc, 3)

plt.subplots_adjust(hspace = 0.5)
plt.subplot(3, 1, 3)
plt.title("Double_Delta_MFCC")
plt.plot(double_delta_mfcc[0])
plt.plot(double_delta_mfcc[1])
plt.plot(double_delta_mfcc[2])

plt.show()