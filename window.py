from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import QtGui

from random import shuffle
from collections import defaultdict
import os

import start_window
import main_window

# collecting names of cards' images in card_list
PATH_TO_DIR = 'static/img/cards'
card_list = os.listdir(PATH_TO_DIR)
card_list = [(PATH_TO_DIR + '/' + card) for card in card_list]

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
        timer_update.timeout.connect(lambda: self.countdown(timer_update))
        timer_update.start(1000)

        # creating a timer for collapsing pictures
        timer = QTimer()
        timer.singleShot(4000, lambda: self.main_window.reset(is_start=True))

        window.hide()

    def countdown(self, timer):
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

        # dictionary holds button objects
        self.open_buttons = {}

        self.score = 0

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

    @staticmethod
    def turn_over_card(card):
        card.setIcon(QtGui.QIcon())
        card.setStyleSheet("background-color: #464258;")

    def get_rid_of_card(self, bn):

        bn.setStyleSheet("QPushButton{background-color: #E37936;}")
        QTimer().singleShot(1000, lambda: self.turn_over_card(bn))

    def check_pair(self, bn, path_to_image, check_state):
        if not check_state:

            card_image = path_to_image.replace(PATH_TO_DIR + '/', '').rsplit('_', 1)[0]
            card_number = path_to_image.replace(PATH_TO_DIR + '/', '').rsplit('_', 1)[1]
            print(card_number, card_image)

            if (card_image in self.open_buttons.keys()) and (self.open_buttons != None):
                if (self.open_cards[card_image] != None) and (self.open_cards[card_image] != None):
                    if (card_number not in self.open_cards[card_image]):
                        print(self.open_cards[card_image])
                        self.score += 1
                        self.label_score1.setText(f'Score: {self.score}')

                        self.get_rid_of_card(self.open_buttons[card_image])
                        self.get_rid_of_card(bn)

            self.open_buttons[card_image] = bn
            self.open_cards[card_image].append(card_number)

        else:
            pass


    # SLOT
    def clicker(self, bn, path_to_image):

        def open_icons(path, button):
            icon = QtGui.QIcon(path_to_image)
            icon.path_to_image = path_to_image
            button.setIcon(icon)

        def button_was_released(self, button):
            self.is_checked = button.isChecked()
            return self.is_checked

        bn.setCheckable(True)
        self.is_checked = False
        self.check_pair(bn, icon.path_to_image, button_was_released(self,bn))
        bn.setCheckable(False)


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
        self.open_buttons = {}
        self.open_cards = defaultdict(list)
        self.score = 0
        self.label_score1.setText('Score: 0')
        self.label_score2.setText('Score: 0')

        for index, bn in enumerate(button_list):
            self.reset_button(bn, index, is_start)


    def reset_button(self, button, card, is_start):
        if is_start:
           button.setEnabled(True)

        button.setIcon(QtGui.QIcon(card_list[card]))

        button.setIconSize(QSize(100, 100))
        QTimer().singleShot(1000, lambda: self.cover_buttons(button))


    @staticmethod
    def cover_buttons(button):
         button.setIcon(QtGui.QIcon('static\\background\\back_side.png'))


def exit_app():
    app.exit()


if __name__ == "__main__":
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
