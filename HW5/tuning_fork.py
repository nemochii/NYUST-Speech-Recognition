import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plt


rate, data = wav.read("440.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

result = process[80000 : 81024]

time = np.linspace(1, len(data), len(data))
time /= rate

plt.figure()
plt.subplot(2, 1, 1)
plt.title("440fork.wav")
plt.plot(time, process)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(result)

#--------------------------------------------------------------------

rate, data = wav.read("tuningFork.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

result = process[11000 : 11256]

time = np.linspace(1, len(data), len(data))
time /= rate

plt.figure()
plt.subplot(2, 1, 1)
plt.title("tuningFork.wav")
plt.plot(time, process)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(result)
plt.show()