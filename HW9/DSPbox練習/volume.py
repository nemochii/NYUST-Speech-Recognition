#coding=UTF-8
import DSPbox as dsp
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

frameSize = 512
overlap = 128
rate , signal = wav.read('hello.wav')
frameCut = dsp.frameMat(signal , frameSize , overlap )
rows,cols=frameCut.shape
volumeArray=np.zeros(cols)
volumeDBArray=np.zeros(cols)

for i in range (0 ,cols,1):
    # abs sum 
    frame = frameCut[:,i] -np.mean(frameCut[:,i])  
    volumeArray[i]=np.sum(np.absolute( frame))     
    # Decibels 
    frame = frameCut[:,i] -np.median(frameCut[:,i]) 
    volumeDBArray[i] =10*np.log10(np.sum( frame**2))

sampleTime  =np.linspace( 1,np.size(signal),np.size(signal))/ rate 
frameTime = (np.linspace( 0,cols,cols)*(frameSize-overlap)) /rate
plt.subplot(311)
plt.plot( sampleTime,signal,)
# 設定y軸刻度單位為科學符號,在style = sci情況下,scilimits會對於範圍以外數字使用科學符號表示,而scilimits(0,0)則代表include all number
# 若要使用scilimits限制需注意scilimits=(m,n)代表是 10^m ~10^n   
plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0))     
plt.ylabel('Amplitude')

plt.subplot(312)
plt.plot(frameTime,volumeArray)
plt.ticklabel_format(style='sci',axis='y')
plt.ylabel('volume, Abs_sum' )
# 設定y軸刻度單位為科學符號
plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0))  

plt.subplot(313)
plt.plot(frameTime ,volumeDBArray)
plt.xlabel('Time')
plt.ylabel('volume ,decibels')
plt.show()




