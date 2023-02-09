from socket import *
import threading
import time

def send(socket):
    while True:
        senddata = input('>>>')
        socket.send(senddata.encode())
        
def recve(socket):
    while True:
        recvdata = socket.recv(1024)
        print("상대방",recvdata.decode())
        
        
host ="127.0.0.1"
port = 9999

client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((host,port))

sender = threading.Thread(target = send, args = (client_socket,))
recver = threading.Thread(target = recve, args = (client_socket,))

sender.start()
recver.start()

while True:
    time.sleep(1)
    pass

"""
def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recv:",repr(data.decode()))


while True:
    message = input('message : ')
    if message == 'exit':
        break
    
    client_socket.send(message.encode())"""
