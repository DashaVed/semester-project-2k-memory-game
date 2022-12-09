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


def handle(client):
    while True:
        try:
            client.send(pickle.dumps(card_list))
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
