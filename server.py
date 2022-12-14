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
count_player = 0

PATH_TO_DIR = 'static/img/cards'
card_list = os.listdir(PATH_TO_DIR)
card_list = [(PATH_TO_DIR + '/' + card) for card in card_list]
shuffle(card_list)


def broadcast(data, index):
    clients[(index + 1) % 2].send(pickle.dumps(data))


def handle(client):
    global count_player
    while True:
        try:
            action = pickle.loads(client.recv(1024))
            if action == 'start_button':
                count_player += 1
                data = [card_list, count_player]
                client.send(pickle.dumps(data))
            elif action == 'reset_button':
                shuffle(card_list)
                data = [card_list, 'reset']
                for c in clients:
                    c.send(pickle.dumps(data))
            elif action == 'exit_button':
                client_index = clients.index(client)
                broadcast('exit', client_index)
            else:
                client_index = clients.index(client)
                broadcast(action, client_index)
        except:
            clients.remove(client)
            client.close()
            print('delete', clients)
            if len(clients) == 0:
                count_player = 0
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        print('append', clients)

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


receive()
