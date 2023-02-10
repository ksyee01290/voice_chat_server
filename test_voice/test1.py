import pyaudio
import numpy as np
 
def reacorder(stream):
    data = stream.read(1024)
    return data

def speaker(stream,data):
    stream.write(data)
    
def send():
    pass

mic = pyaudio.PyAudio()
mic_stream = mic.open(format=pyaudio.paFloat32,channels=1,rate=44100,input=True,frames_per_buffer=1024)

speaker_obj = pyaudio.PyAudio()
speaker_stream = speaker_obj.open(format=pyaudio.paFloat32,channels=1,rate=44100,output=True,frames_per_buffer=1024)

while True:
    data = reacorder(mic_stream)
    data = np.frombuffer(data,np.single)
    data = data
    speaker(speaker_stream,data.tobytes())
