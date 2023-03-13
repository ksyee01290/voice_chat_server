import socket
import threading

HOST = '127.0.0.1'
PORT = 10002

#clients_lock = threading.Lock() 
clients = []

def receive(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        send_all(clients, client_socket, data)
    client_socket.close()

def send_all(clients, sender_socket, sound_message):
#   with clients_lock: # 락 오브젝트를 획득한 후 클라이언트 리스트 접근
    for client in clients:
        try:
            if client != sender_socket and client.fileno() != -1:
                client.sendall(sound_message)
        except:
            clients.remove(client)
            client.close()

def handle_client(client_socket, address):
    clients.append(client_socket)
    print(f'client {address} connected.')

    receive_thread = threading.Thread(target=receive, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_all, args=(clients, client_socket,b''))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    if client_socket in clients:
        client_socket.close()
        clients.remove(client_socket)
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