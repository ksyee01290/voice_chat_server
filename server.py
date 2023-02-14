import pyaudio
import numpy as np
import socket
import threading

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

def handle_client(client_socket):
    speaker_obj = pyaudio.PyAudio()
    speaker_stream = speaker_obj.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    mic = pyaudio.PyAudio()
    mic_stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = recorder(mic_stream)
            send(client_socket, bytes(data))
            data = receive(client_socket)
            speaker(speaker_stream, data)
            
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {client_socket.getpeername()} disconnected.")
    finally:
        client_socket.close()
        speaker_stream.close()
        speaker_obj.terminate()
        mic_stream.close()
        mic.terminate()
        
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 9999))
server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    print('연결 되었다 : ', address)
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()