import socket
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
        
"""   
def threaded(client_socket,addr):
    print('connect:',addr[0],":",addr[1])
    
    while True:
        try:
            data = client_socket.recv(1024)         
            if not data:
                print("disconnect:" + addr[0],":",addr[1])
                break          
            print("recvfrom" + addr[0],":",addr[1],data.decode())
            
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close()
            """

host = "127.0.0.1"

port = 9999

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((host,port))
server_socket.listen()

print("wait")

connectionsocket, addr = server_socket.accept()

print(str(addr),'에 접속되었습니다.')

sender = threading.Thread(target = send, args = (connectionsocket,))
recver = threading.Thread(target = recve, args = (connectionsocket,))

sender.start()
recver.start()

while True:
    time.sleep(1)
    pass
    