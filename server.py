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
PATH_TO_DIR = 'static/img/cards'
card_list = os.listdir(PATH_TO_DIR)
card_list = [(PATH_TO_DIR + '/' + card) for card in card_list]
shuffle(card_list)


def broadcast(data, index):
    clients[(index + 1) % 2].send(pickle.dumps(data))


def handle(client, turn):
    while True:
        try:
            action = pickle.loads(client.recv(1024))
            if action == 'start_button' or action == 'reset_button':
                data = [card_list, turn]
                client.send(pickle.dumps(data))
            else:
                client_index = clients.index(client)
                broadcast(action, client_index)
        except ValueError as e:
            print(e)
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        turn = 2 if len(clients) % 2 == 0 else 1

        thread = threading.Thread(target=handle, args=(client, turn, ))
        thread.start()


receive()
