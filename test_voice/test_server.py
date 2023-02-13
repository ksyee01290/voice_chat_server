import pyaudio
import numpy as np
import socket

CHUNK = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 48000

def recorder(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    return data

def speaker(stream, data):
    stream.write(data)

def receive(client_socket):
    return client_socket.recv(CHUNK)

def send(client_socket, data):
    client_socket.sendall(data)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 9999))
server_socket.listen(5)

client_socket, address = server_socket.accept()
print('Connected by', address)

speaker_obj = pyaudio.PyAudio()
speaker_stream = speaker_obj.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

mic = pyaudio.PyAudio()
mic_stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

while True:
    data = receive(client_socket)
    speaker(speaker_stream, data)
    data = recorder(mic_stream)
    send(client_socket, bytes(data))