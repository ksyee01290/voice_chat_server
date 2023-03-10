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
    buf = bytearray()
    while True:
        data = client_socket.recv(length - len(buf))
        if not data:
            return None
        buf += data
        if len(buf) >= length:
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
    global is_running
    while is_running:
        try:
            data = recorder(mic_stream)
            send(sock, bytes(data))
        except:
            print('Connection lost. Closing socket.')
            is_running = False
            client_socket.close()
            break

def reader(sock, speaker_stream):
    global is_running
    while is_running:
        try:
            data = receive(sock)
            speaker(speaker_stream, data)
        except:
            break

is_running = True
writer_thread = threading.Thread(target=writer, args=(client_socket,mic_stream))
reader_thread = threading.Thread(target=reader, args=(client_socket,speaker_stream))


writer_thread.start()
reader_thread.start()

while is_running:
    user_input = input("'exit' 입력시 : ")
    if user_input == "exit":
        client_socket.send("exit".encode())
        is_running = False
        client_socket.close()
        
writer_thread.join()
reader_thread.join()
