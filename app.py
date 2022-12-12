import pickle
import socket
import time
import traceback
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtGui

import start_window
import main_window


PATH_TO_DIR = 'static/img/cards'
card_list = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5060))
count_player = None


class WorkerSignals(QObject):
    finished = pyqtSignal(name='finish')
    error = pyqtSignal(tuple, name='error')
    result = pyqtSignal(name='result')
    progress = pyqtSignal(int, name='progress')


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit()  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Start(QMainWindow, start_window.Ui_StartWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.setupUi(self)
        self.main_window = Game()
        self.duration = 3
        self.threadpool = QThreadPool()

        self.start_button.clicked.connect(lambda: self.start_game())
        self.end_button.clicked.connect(lambda: exit_app())

    def start_game(self):
        client.send(pickle.dumps(self.start_button.objectName()))
        self.main_window.show()

        receive_thread = Worker(receive, self.main_window)
        receive_thread.signals.finished.connect(exit)
        self.threadpool.start(receive_thread)

        window.hide()


class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(Game, self).__init__()
        self.setupUi(self)

        self.open_cards = {}
        self.score1 = 0
        self.score2 = 0
        self.duration = 3

        self.first_turn = True
        self.hide_button = []
        self.count_hide_btn = 0

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

    def check_pair(self, bn, path_to_image):
        card_image = path_to_image.replace(PATH_TO_DIR + '/', '').rsplit('_', 1)[0]
        if card_image in self.open_cards.keys():
            if self.first_turn:
                self.score1 += 1
                self.label_score1.setText(f'Score: {self.score1}')
            else:
                self.score2 += 1
                self.label_score2.setText(f'Score: {self.score2}')

            bn.setStyleSheet("QPushButton {background: #E37936;}")
            self.open_cards[card_image].setStyleSheet("QPushButton {background: #E37936;}")

            self.hide_button.append(bn)
            self.hide_button.append(self.open_cards[card_image])
            self.count_hide_btn += 2
            if self.count_hide_btn == 18:
                self.groupBox.setStyleSheet('QGroupBox#groupBox{border: 1px solid #FFB8CE;}')
                self.groupBox_2.setStyleSheet('QGroupBox#groupBox_2{border: 1px solid #FFB8CE;}')
                self.clear_button()
            return
        self.open_cards[card_image] = bn

    def clear_button(self):
        for button in self.hide_button:
            button.setIcon(QtGui.QIcon())
            button.setStyleSheet('QPushButton {background: #464258;}')
        self.hide_button = []

    def change_label(self):
        if (self.first_turn is True and count_player == 1) or \
                (self.first_turn is False and count_player == 2):
            self.label.setText('Your turn')
        else:
            self.label.setText("Opponent's turn")
        if self.first_turn:
            self.groupBox.setStyleSheet('QGroupBox#groupBox{border: 4px solid #FFB8CE;}')
            self.groupBox_2.setStyleSheet('QGroupBox#groupBox_2{border: 1px solid #FFB8CE;}')
        else:
            self.groupBox_2.setStyleSheet('QGroupBox#groupBox_2{border: 4px solid #FFB8CE;}')
            self.groupBox.setStyleSheet('QGroupBox#groupBox{border: 1px solid #FFB8CE;}')

    def clicker(self, bn, path_to_image, from_server=False):

        if (count_player == 1 and self.first_turn is True) or \
                (count_player == 2 and self.first_turn is False) or from_server:
            self.clear_button()

            if not from_server:
                client.send(pickle.dumps(bn.objectName()))

            icon = QtGui.QIcon(path_to_image)
            bn.setIcon(icon)
            bn.blockSignals(True)

            self.check_pair(bn, path_to_image)

            self.first_turn = False if self.first_turn is True else True
            self.change_label()

    def reset(self):
        self.open_cards = {}
        self.hide_button = []
        self.count_hide_btn = 0
        self.duration = 3

        self.score1 = 0
        self.score2 = 0
        self.first_turn = True
        self.label_score1.setText('Score: 0')
        self.label_score2.setText('Score: 0')

        button_list = [
            self.button_1, self.button_2, self.button_3,
            self.button_4, self.button_5, self.button_6,
            self.button_7, self.button_8, self.button_9,
            self.button_10, self.button_11, self.button_12,
            self.button_13, self.button_14, self.button_15,
            self.button_16, self.button_17, self.button_18,
        ]

        for index, b in enumerate(button_list):
            self.get_reset_button(b, index)

    def get_reset_button(self, button, card):
        button.setEnabled(True)
        button.setIcon(QtGui.QIcon(card_list[card]))
        button.setIconSize(QSize(100, 100))
        QTimer().singleShot(3000, lambda: self.update_img(button))

    @staticmethod
    def update_img(button):
        button.setIcon(QtGui.QIcon())
        button.setStyleSheet('QPushButton {background: #716799;}')


def exit_app():
    app.exit()


def update_timer(game):
    while game.duration != 0:
        game.label.setText(f'Game starts in {game.duration} seconds')
        game.duration -= 1
        time.sleep(1)
    if count_player == 1:
        game.label.setText('Your turn')
        game.groupBox.setStyleSheet('QGroupBox#groupBox{border: 4px solid #FFB8CE;}')
    else:
        game.label.setText("Opponent's turn")


def create_thread(game):
    thread = QThreadPool()
    update_worker = Worker(update_timer, game)
    update_worker.signals.finished.connect(game.reset)
    thread.start(update_worker)


def receive(game):
    global card_list, count_player
    while True:
        data = pickle.loads(client.recv(1024))
        if isinstance(data, list):
            card_list, count_player = data[0], data[1]
            if count_player == 1:
                game.label.setText('Waiting for another player to connect...')
            else:
                client.send(pickle.dumps('two players'))
                create_thread(game)
        else:
            if data == 'two players':
                create_thread(game)
            else:
                button = game.findChild(QPushButton, data)
                if not button.signalsBlocked():
                    index = int(data.split('_')[1])
                    game.clicker(button, card_list[index - 1], from_server=True)


if __name__ == "__main__":
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
