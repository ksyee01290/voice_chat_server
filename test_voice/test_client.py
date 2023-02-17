import pyaudio
import numpy as np
import socket
import threading

CHUNK = 256
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000

def recorder(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    return data

def speaker(stream,data):
    stream.write(data)

def receive(client_socket):
    length = CHUNK*4
    buf = []
    while True:
        buf += client_socket.recv(length)
        if len(buf)>=length:
            break
    return bytes(buf)

def send(client_socket, data):
    client_socket.sendall(data)
    
sound_obj = pyaudio.PyAudio()
mic_stream = sound_obj.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
speaker_stream = sound_obj.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True,frames_per_buffer=CHUNK)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10002))    

def writer(sock, mic_stream):
    while True:
        data = recorder(mic_stream)
        send(client_socket, bytes(data))

def reader(sock, speaker_stream):
    while True:
        data = receive(client_socket)
        speaker(speaker_stream, data)
  
writer_thread = threading.Thread(target=writer, args=(client_socket,mic_stream))
reader_thread = threading.Thread(target=reader, args=(client_socket,speaker_stream))

writer_thread.start()
reader_thread.start()
writer_thread.join()
reader_thread.join()