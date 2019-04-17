import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plt
from dspBox import frameMat

rate, data = wav.read("hello.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)
time = np.linspace(1, np.size(process), np.size(process)) / rate

cut = frameMat(process, 512, 128)
row, col = cut.shape
abs_array = np.zeros(col)

for i in range(0, col, 1):
	frame = cut[:, i] - np.mean(cut[:, i])
	abs_array[i] = np.sum(np.absolute(frame))

index = []
for i in range(len(abs_array)):
	if abs_array[i] > 3:
		index.append(i)

point_range = np.array([index[0], index[-1]])

step = 512 - 128
time_range = point_range * step / rate

plt.title("hello.wav")
plt.plot(time, data)
plt.axvline(x = time_range[0], color = 'red')
plt.axvline(x = time_range[1], color = 'red')

plt.show()