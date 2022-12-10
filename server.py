import os
import socket
import threading
import pickle
from random import shuffle

host = '127.0.0.1'
port = 5060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen(2)
print("Waiting for a connection, Server Started")

clients = []
card_list = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H', 'I', 'I']
shuffle(card_list)


def broadcast(data, index):
    clients[(index + 1) % 2].send(pickle.dumps(data))


def handle(client):
    while True:
        try:
            action = pickle.loads(client.recv(1024))
            if action == 'start_button' or action == 'reset_button':
                client.send(pickle.dumps(card_list))
            else:
                client_index = clients.index(client)
                print('client index', client_index)
                # отправить название кнопки, для которой выполняется нажатие
                broadcast(action, client_index)
        except ValueError as e:
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


os.system('clear')
receive()
