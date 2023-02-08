import socket
from _thread import *

def threaded(client_socket,addr):
    print('connect:',addr[0],":",addr[1])
    
    while True:
        try:
            data = client_socket.recv(1024)
            
            if not data:
                print("disconnect:" + addr[0],":",addr[1])
                break
            print("recvfrom" + addr[0],":",addr[1],data.decode())
            client_socket.send(data)
            
        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close()
            

host = "127.0.0.1"

port = 9999

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((host,port))
server_socket.listen()
print("server start")

while True: 

    print('wait')


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close()