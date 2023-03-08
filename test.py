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
        try:
            buf += client_socket.recv(length - len(buf))
        except:
            print("서버와의 연결이 끊어졌습니다.")
            client_socket.close()
            return None
        if len(buf) >= length:
            break
    return bytes(buf)

def send(client_socket, data):
    try:
        client_socket.sendall(data)
    except:
        print("서버와의 연결이 끊어졌습니다.")
        client_socket.close()

sound_obj = pyaudio.PyAudio()
audio_stream = sound_obj.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,output=True,frames_per_buffer=CHUNK)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10002))    

def audio_thread(sock, stream):
    while True:
        try:
            data = recorder(stream)
            send(client_socket, bytes(data) if data else b'')
            data = receive(client_socket)
            if data:
                speaker(stream, data)
        except Exception as e:
            print("오류 발생:", e)
            client_socket.close()
            break

thread = threading.Thread(target=audio_thread, args=(client_socket, audio_stream))
thread.start()

while True:
    user_input = input("'exit' 입력시 : ")
    if user_input == "exit":
        client_socket.close()
        break

thread.join()
