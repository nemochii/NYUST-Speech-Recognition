import scipy.io.wavfile as wav
import numpy as np
from DSPbox import frameMat
from matplotlib import pyplot as plt

rate, data = wav.read("HappyNewYear.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

cut = frameMat(process, 512, 128)
row, col = cut.shape
abs_array = np.zeros(col)
db_array = np.zeros(col)

for i in range(0, col, 1):
	frame = cut[:, i] - np.mean(cut[:, i])
	abs_array[i] = np.sum(np.absolute(frame))

	frame = cut[:, i] - np.median(cut[:, i])
	db_array[i] = 10 * np.log10(np.sum(frame ** 2))

org_time = np.linspace(1, np.size(process), np.size(process)) / rate
process_time = np.linspace(0, col, col) * 384 / rate

plt.subplot(3, 1, 1)
plt.plot(org_time, data)
plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

plt.subplots_adjust(hspace = 0.5)
plt.subplot(3, 1, 2)
plt.plot(process_time, abs_array)
plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

plt.subplots_adjust(hspace = 0.5)
plt.subplot(3, 1, 3)
plt.plot(process_time, db_array)
plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

plt.show()