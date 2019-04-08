import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plt

rate, data = wav.read("hello.wav")

reverse = np.zeros(data.size, dtype = data.dtype)
i = 0
while i < data.size:
	if data[i] > 0:
		reverse[i] = 1 - data[i]
	if data[i] < 0:
		reverse[i] = -1 - data[i]
	i += 1		
reverse = reverse[::-1]

wav.write("reverse_hello.wav", rate, reverse)

time = np.linspace(1, data.size, data.size)
time /= rate

plt.subplot(2, 1, 1)
plt.title("Original")
plt.plot(time, data)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(time, reverse)
plt.show()