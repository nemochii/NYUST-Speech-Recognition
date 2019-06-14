# coding=UTF-8
import tkinter as tk
import wave
import pyaudio
import _thread

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "../B10517047_record/"    #學號
count=0                              #流水號初始值
btn_count = 0
f=open('text.txt','r')
lines = f.readlines()
f.close()

def record_wave_thread():
    _thread.start_new_thread(record_wave,())
    

def record_wave():
    global count
    global lines
    audio = pyaudio.PyAudio()
    frames = []
    stream = audio.open(
            format=FORMAT, 
            channels=CHANNELS,
            rate=RATE, 
            input=True,
            frames_per_buffer=CHUNK
            )
    
    print("Recording...")
    button2.configure(state='disabled')

    
    while 1:
        if btn_count is 0:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            line=lines[count].split(' ')      
            waveFile = wave.open(WAVE_OUTPUT_FILENAME+'_'+str(line[0])+'.wav' , 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            count+=1
            break
        else:
            data = stream.read(CHUNK)
            frames.append(data)
    
    print("finished recording")
    line=lines[count].split(' ') 
    var.set(line[1].replace('\n',''))
    button2.configure(state='normal')
    if(count==len(lines)-1):
        button.configure(state='disabled')
        var.set('finished all recording!!')
    #tkMessageBox.showinfo("Recorder","Recording Finsh!")
    _thread.exit_thread() 

def record_count():
    global btn_count
    global count
    global lines    
    line=lines[count].split(' ')      
    var.set(line[1].replace('\n',''))
    if btn_count is 0:
        record_wave_thread()
        btn_count = 1
    else:
        btn_count = 0


def delete():
    global count
    count-=1
    button.configure(state='normal')
    button2.configure(state='disabled')
    line=lines[count].split(' ') 
    var.set(line[1].replace('\n',''))    
    



top=tk.Tk()
top.geometry('300x150')
top.title("Speaker recognition")
var = tk.StringVar() 
var.set("record & test")
label=tk.Label(top,textvariable=var)
label.pack()
button=tk.Button(top,text="Recording",command=record_count)
button.pack()    
button2=tk.Button(top,text="Re-recording the last",command=delete,state='disabled')
button2.pack()  

if(WAVE_OUTPUT_FILENAME == "student ID" ):
    var.set("You don't change student ID !!")
    button.configure(state='disabled')
    button2.configure(state='disabled') 
    
top.mainloop()

   