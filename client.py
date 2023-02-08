import socket

host ="127.0.0.1"
port = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((host,port))

client_socket.sendall("안녕".encode())

data = client_socket.recv(1024)
print("recv",repr(data.decode()))

client_socket.close()