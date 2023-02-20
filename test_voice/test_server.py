import pyaudio
import numpy as np
import socket
import threading

CHUNK = 256
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000

def writer(sock, mic_stream):
    while True:
        data = recorder(mic_stream)
        send(client_socket,bytes(data))

def reader(sock, speaker_stream):
    while True:
        data = receive(client_socket)
        speaker(speaker_stream, data)
        

def handle_client(client_socket):
    sound_obj = pyaudio.PyAudio()
    speaker_stream = sound_obj.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    mic_stream = sound_obj.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
    writer_thread = threading.Thread(target=writer, args=(client_socket,mic_stream))
    reader_thread = threading.Thread(target=reader, args=(client_socket,speaker_stream))
    
    writer_thread.start()
    reader_thread.start()
    writer_thread.join()
    reader_thread.join()
    

def recorder(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    return data

def speaker(stream, data):
    stream.write(data)
    
lock = threading.Lock()

def receive(client_socket):
    length = CHUNK*4
    buf = bytearray()
    while True:
        data = client_socket.recv(length - len(buf))
        buf += data
        if len(buf) == length:
            break
    return bytes(buf)

def send(client_socket, data):
    lock.acquire()
    try:
        for c in client:
            if c != client_socket:
                continue
            c.sendall(data)
    finally:
        lock.release()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10002))
server_socket.listen(3)

client = []

while True:
    
    client_socket, address = server_socket.accept()
    print('연결 되었다 : ', address)
    
    client.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

    