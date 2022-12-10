from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import QtGui
from random import shuffle, randint
import os

import start_window
import main_window

# collecting names of cards' images in card_list
path_to_dir = 'static/img/cards'
card_list = os.listdir(path_to_dir)
card_list = [(path_to_dir + '/' + card) for card in card_list]

class Start(QMainWindow, start_window.Ui_StartWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.ui = None
        self.start_window = None
        self.setupUi(self)
        self.main_window = Game()
        self.duration = 3

        # connect start and end buttons with slots
        self.start_button.clicked.connect(lambda: self.start())
        self.end_button.clicked.connect(lambda: exit_app())

    def start(self):

        # open main window
        self.main_window.show()

        # creating a timer for reversed count
        timer_update = QTimer()
        timer_update.timeout.connect(lambda: self.update_timer(timer_update))
        timer_update.start(1000)

        # creating a timer for pictures collapsing
        timer = QTimer()
        timer.singleShot(4000, lambda: self.main_window.reset(is_start=True))

        window.hide()

    def update_timer(self, timer):
        self.main_window.label.setText(f'Game starts in {self.duration} seconds')
        if self.duration == 0:
            timer.stop()
            self.main_window.label.setText('Observe the cards and memories them!')
            self.duration = 3
        self.duration -= 1


class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(Game, self).__init__()
        self.setupUi(self)

        # {card's name : object of button}
        self.open_cards = {}

        self.score = 0

        # QTimer.singleShot(1, self.reset)

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
        self.start_button.clicked.connect(lambda: self.reset())
        self.exit_button.clicked.connect(lambda: exit_app())

    def check_pair(self, bn, path_to_image):
        card_image = path_to_image.replace(path_to_dir + '/', '').rsplit('_',1)[0]
        if card_image in self.open_cards.keys():
            self.score += 1
            self.label_score1.setText(f'Score: {self.score}')
            return
        self.open_cards[card_image] = bn

    def clicker(self, bn, path_to_image):

        icon = QtGui.QIcon(path_to_image)
        icon.path_to_image = path_to_image
        bn.setIcon(icon)
        # b.setEnabled(True)
        self.check_pair(bn, icon.path_to_image)

    def reset(self, is_start=False):
        button_list = [
            self.button_1, self.button_2, self.button_3,
            self.button_4, self.button_5, self.button_6,
            self.button_7, self.button_8, self.button_9,
            self.button_10, self.button_11, self.button_12,
            self.button_13, self.button_14, self.button_15,
            self.button_16, self.button_17, self.button_18,
        ]

        shuffle(card_list)
        self.open_cards = {}
        self.score = 0
        self.label_score1.setText('Score: 0')
        self.label_score2.setText('Score: 0')

        for index, bn in enumerate(button_list):
            self.reset_button(bn, index, is_start)

    def reset_button(self, button, card, is_start):
        if is_start:
           button.setEnabled(True)
        button.setIcon(QtGui.QIcon(card_list[card]))

        # size image to whole button
        button.setIconSize(QSize(100, 100))
        #button.setStyleSheet('QPushButton {background-color: #716799; color: #FFF352;}')
        QTimer().singleShot(3000, lambda: self.update_text(button))


    @staticmethod
    def update_text(button):
        button.setIcon(QtGui.QIcon('static\\background\\back_side.png'))
        button.setText('')


def exit_app():
    app.exit()


if __name__ == "__main__":
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
