import socket

host ="127.0.0.1"
port = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((host,port))

while True:
    message = input('message : ')
    if message == 'exit':
        break
    client_socket.send(message.encode())
    data = client_socket.recv(1024)

    print('recev from the server :',repr(data.decode()))

client_socket.close()



HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 