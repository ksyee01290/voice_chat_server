import pyaudio
import numpy as np
import socket
import threading

CHUNK = 256
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000


def handle_client(client_socket,client_address):
    # 연결된 클라이언트 소켓을 리스트에 추가합니다.
    client.append(client_socket)

    print(f'Client {client_address} connected.')

    # 클라이언트로부터 데이터를 받아서 모든 클라이언트에게 전송합니다.
    while True:
        # 클라이언트로부터 데이터를 받습니다.
        data = client_socket.recv(1024)
        if not data:
            break

        # 받은 데이터를 모든 클라이언트에게 전송합니다.
        for cl in client:
            # 자신에게는 보내지 않도록 조건문으로 필터링합니다.
            if cl != client_socket:
                cl.sendall(data)

    # 클라이언트 소켓을 리스트에서 제거합니다.
    client.remove(client_socket)

    print(f'Client {client_address} disconnected.')

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
    client_socket.sendall(data)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10002)) 
server_socket.listen(3)

client = []

while True:
    
    client_socket, client_address = server_socket.accept()
    print('연결 되었다 : ', client_address)
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
    client_thread.start()
    
server_socket.close()

    