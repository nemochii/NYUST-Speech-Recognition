import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plt

rate, data = wav.read("p.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)


result = process[18400 : 18912]

time = np.linspace(1, len(data), len(data))
time /= rate

plt.figure()
plt.subplot(2, 1, 1)
plt.title("p.wav")
plt.plot(process)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(result)

#--------------------------------------------------------------------

rate, data = wav.read("a.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

result = process[18400 : 18912]

time = np.linspace(1, len(data), len(data))
time /= rate

plt.figure()
plt.subplot(2, 1, 1)
plt.title("a.wav")
plt.plot(process)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(result)
plt.show()