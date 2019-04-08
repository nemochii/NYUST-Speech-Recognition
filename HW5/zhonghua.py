import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plt

rate, data = wav.read("Zhonghua.wav")

process = np.zeros(data.size, dtype = data.dtype)
process = data / pow(2, 15)

result = process[20000 : 20512]

time = np.linspace(1, len(data), len(data))
time /= rate

plt.subplot(2, 1, 1)
plt.title("Zhonghua.wav")
plt.plot(time, process)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(result)
plt.show()