import scipy.io.wavfile as wav
import numpy as np
from onesidespectra import One_sided_spectra
from matplotlib import pyplot as plt

rate, data = wav.read("a.wav")

frq, db = One_sided_spectra(data[10000 : 10512], rate)

process = np.append(data[0], data[1:] - 0.98 * data[:-1])
frq2, db2 = One_sided_spectra(process[10000 : 10512], rate)

wav.write("AfHightPass.wav", rate, process)

plt.subplot(2, 1, 1)
plt.title("a.wav")
plt.plot(frq, db)
plt.subplots_adjust(hspace = 0.5)
plt.subplot(2, 1, 2)
plt.title("Processed")
plt.plot(frq2, db2)
plt.show()