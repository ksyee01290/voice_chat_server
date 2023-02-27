import socket
import threading

HOST = '127.0.0.1'
PORT = 10002

clients = []

def receive(client_socket):
    return client_socket.recv(1024)

def send_all(clients,sender_socket,masseg):
    for client in clients:
        if client != sender_socket:
            client.sendall(masseg)

def handle_client(client_socket,address):
    clients.append(client_socket)
    print(f'client {address} commected.')
    
    while True:
        data = receive(client_socket)
        if not data:
            break
        
        send_all(clients,client_socket,data)
    
    clients.remove(client_socket)
    
    print(f'client {address} discommected.')
    
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10)

    print(f'server listening on {HOST}:{PORT}')

    while True:
        client_socket, address = server_socket.accept()
    
        client_thread = threading.Thread(target=handle_client, args=(client_socket,address))
        client_thread.start()
 
    server_socket.close()

if __name__ == '__main__':
    run_server()