import socket
import threading

clients = []
lock = threading.Lock()

def add_client(client_socket):
    with lock:
        clients.append(client_socket)

def remove_client(client_socket):
    with lock:
        clients.remove(client_socket)
        client_socket.close()
        broadcast('Client {} disconnected\n'.format(client_socket))

def broadcast(msg):
    with lock:
        for client_socket in clients:
            try:
                client_socket.sendall(msg.encode('utf-8'))
            except:
                remove_client(client_socket)

def handle_client(client_socket):
    add_client(client_socket)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                raise Exception("연결 종료")
            broadcast(data)
    except:
        remove_client(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 10002))
    server_socket.listen(3)

    while True:
        client_socket, address = server_socket.accept()
        print('연결 되었다 : ', address)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_server()