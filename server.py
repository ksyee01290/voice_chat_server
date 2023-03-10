import socket
import threading

HOST = '127.0.0.1'
PORT = 10002

clients = []

def receive(client_socket):
    return client_socket.recv(1024)

def send_all(clients, sender_socket, message):
    for client in clients:
        try:
            if client != sender_socket and client.fileno() != -1:
                client.sendall(message)
        except:
            clients.remove(client)
            client.close()

def handle_client(client_socket, address):
    clients.append(client_socket)
    print(f'client {address} connected.')
    
    try:
        while True:
            data = receive(client_socket)
            if not data:
                break
            if data == "exit":  # 클라이언트가 "exit"를 보냈을 경우
                break
            send_all(clients, client_socket, data)
    except Exception as e:
        print(f'client {address} error occurred: {e}')
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
            client_socket.close()
            print(f'client {address} disconnected.')
    
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(5)

    print(f'server listening on {HOST}:{PORT}')

    while True:
        client_socket, address = server_socket.accept()
    
        client_thread = threading.Thread(target=handle_client, args=(client_socket,address))
        client_thread.start()
 
    server_socket.close()

if __name__ == '__main__':
    run_server()