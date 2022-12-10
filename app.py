import pickle
import socket
import threading
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6 import QtGui

import os
import start_window
import main_window

# collecting names of cards' images in card_list
PATH_TO_DIR = 'static/img/cards'
card_list = os.listdir(PATH_TO_DIR)
card_list = [(PATH_TO_DIR + '/' + card) for card in card_list]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5060))


class Start(QMainWindow, start_window.Ui_StartWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.start_window = None
        self.setupUi(self)
        self.main_window = Game()
        self.duration = 3

        self.start_button.clicked.connect(lambda: self.start_game())
        self.end_button.clicked.connect(lambda: exit_app())

    def start_game(self):
        client.send(pickle.dumps(self.start_button.objectName()))
        self.main_window.show()
        timer_update = QTimer()
        timer_update.timeout.connect(lambda: self.update_timer(timer_update))
        timer_update.start(1000)
        timer = QTimer()
        timer.singleShot(4000, lambda: self.main_window.reset(is_start=True))

        window.hide()

        receive_thread = threading.Thread(target=self.main_window.receive)
        receive_thread.start()

    def update_timer(self, timer):
        self.main_window.label.setText(f'Game started in {self.duration} sec')
        if self.duration == 0:
            timer.stop()
            self.main_window.label.setText('Observe the cards and memories them!')
            self.duration = 3
        self.duration -= 1


class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(Game, self).__init__()
        self.setupUi(self)
        self.open_cards = {}
        self.score1 = 0
        self.score2 = 0

        self.first_turn = True

        self.button_1.clicked.connect(lambda: self.clicker(self.button_1, card_list[0]))
        self.button_2.clicked.connect(lambda: self.clicker(self.button_2, card_list[1]))
        self.button_3.clicked.connect(lambda: self.clicker(self.button_3, card_list[2]))
        self.button_4.clicked.connect(lambda: self.clicker(self.button_4, card_list[3]))
        self.button_5.clicked.connect(lambda: self.clicker(self.button_5, card_list[4]))
        self.button_6.clicked.connect(lambda: self.clicker(self.button_6, card_list[5]))
        self.button_7.clicked.connect(lambda: self.clicker(self.button_7, card_list[6]))
        self.button_8.clicked.connect(lambda: self.clicker(self.button_8, card_list[7]))
        self.button_9.clicked.connect(lambda: self.clicker(self.button_9, card_list[8]))
        self.button_10.clicked.connect(lambda: self.clicker(self.button_10, card_list[9]))
        self.button_11.clicked.connect(lambda: self.clicker(self.button_11, card_list[10]))
        self.button_12.clicked.connect(lambda: self.clicker(self.button_12, card_list[11]))
        self.button_13.clicked.connect(lambda: self.clicker(self.button_13, card_list[12]))
        self.button_14.clicked.connect(lambda: self.clicker(self.button_14, card_list[13]))
        self.button_15.clicked.connect(lambda: self.clicker(self.button_15, card_list[14]))
        self.button_16.clicked.connect(lambda: self.clicker(self.button_16, card_list[15]))
        self.button_17.clicked.connect(lambda: self.clicker(self.button_17, card_list[16]))
        self.button_18.clicked.connect(lambda: self.clicker(self.button_18, card_list[17]))
        self.exit_button.clicked.connect(lambda: exit_app())
        self.reset_button.clicked.connect(lambda: self.reset())

    @staticmethod
    def turn_over_card(card):
        card.setIcon(QtGui.QIcon())
        card.setStyleSheet('background-color: #464258;')
        # card.setIcon(QtGui.QIcon('static/img/background/back_side.png'))
        # card.setIconSize(QSize(200, 200))

    def get_rid_of_card(self, card):
        card.setStyleSheet("background-color: #E37936;")
        QTimer().singleShot(1000, lambda: self.turn_over_card(card))

    def check_pair(self, bn, path_to_image):
        card_image = path_to_image.replace(PATH_TO_DIR + '/', '').rsplit('_', 1)[0]
        print(card_image)
        if card_image in self.open_cards.keys():
            if self.first_turn:
                self.score1 += 1
                self.label_score1.setText(f'Score: {self.score1}')
            else:
                self.score2 += 1
                self.label_score2.setText(f'Score: {self.score2}')

            self.get_rid_of_card(self.open_cards[card_image])
            self.get_rid_of_card(bn)
            return

        self.open_cards[card_image] = bn

    def clicker(self, bn, path_to_image):
        if bn.isEnabled():
            icon = QtGui.QIcon(path_to_image)
            # icon.path_to_image = path_to_image
            bn.setIcon(icon)
            bn.setEnabled(False)

            client.send(pickle.dumps(bn.objectName()))

            self.check_pair(bn, path_to_image)

            self.first_turn = False if self.first_turn is True else True

    def reset(self, is_start=False):
        button_list = [
            self.button_1, self.button_2, self.button_3,
            self.button_4, self.button_5, self.button_6,
            self.button_7, self.button_8, self.button_9,
            self.button_10, self.button_11, self.button_12,
            self.button_13, self.button_14, self.button_15,
            self.button_16, self.button_17, self.button_18,
        ]
        self.open_cards = {}

        self.score1 = 0
        self.score2 = 0
        self.first_turn = True
        self.label_score1.setText('Score: 0')
        self.label_score2.setText('Score: 0')

        for index, b in enumerate(button_list):
            self.get_reset_button(b, index, is_start)

    def get_reset_button(self, button, card, is_start):
        if is_start:
            button.setEnabled(True)
        button.setIcon(QtGui.QIcon(card_list[card]))

        # size image to whole button
        button.setIconSize(QSize(100, 100))
        #
        QTimer().singleShot(3000, lambda: self.update_img(button))

    @staticmethod
    def update_img(button):
        button.setIcon(QtGui.QIcon())
        button.setStyleSheet('background-color: #716799;')

    def receive(self):
        global card_list
        while True:
            data = pickle.loads(client.recv(1024))
            if isinstance(data, list):
                card_list = data
            else:
                button = self.findChild(QPushButton, data)
                index = int(data.split('_')[1])  # получить номер кнопки
                self.clicker(button, card_list[index - 1])


def exit_app():
    app.exit()


if __name__ == "__main__":
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
