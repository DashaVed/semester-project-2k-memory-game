import time

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication
from random import shuffle

import main_window

card_list = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H', 'I', 'I']
shuffle(card_list)


# пишем своё MainWindow, основанное на Ui_MainWindow (которое мы ранее сгенерировали)
class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        # в методе инициализации мы вызываем родительскую инициализацию (устанавливаем элементы интерфейса)
        super(Game, self).__init__()
        self.setupUi(self)
        self.open_card = {}
        #
        # for index, button in enumerate(button_list):
        #     button.clicked.connect(lambda: self.clicker(self.button_1, card_list[index]))


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

    def check_pair(self, b):
        value = b.text()
        if value in self.open_card.keys():
            b.setStyleSheet('QPushButton {background-color: #5A5475; color: #FFB8CE;}')
            self.open_card[value].setStyleSheet('QPushButton {background-color: #5A5475; color: #FFB8CE;}')
            return
        self.open_card[b.text()] = b

    def clicker(self, b, card):
        b.setText(card)
        b.setEnabled(False)

        self.check_pair(b)

    def reset(self):
        button_list = [
            self.button_1, self.button_2, self.button_3,
            self.button_4, self.button_5, self.button_6,
            self.button_7, self.button_8, self.button_9,
            self.button_10, self.button_11, self.button_12,
            self.button_13, self.button_14, self.button_15,
            self.button_16, self.button_17, self.button_18,
        ]
        shuffle(card_list)
        self.button_1.setEnabled(True)
        self.button_1.setText(card_list[0])
        self.button_1.setStyleSheet('QPushButton {background-color: #716799; color: #FFF352;}')
        self.open_card = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        # for b in button_list:
        #     b.setEnabled(True)
        #     b.setText(card_list[0])
        #     b.setStyleSheet('QPushButton {background-color: #716799; color: #FFF352;}')
        #     self.open_card = {}
        #     self.timer = QTimer()
        #     self.timer.timeout.connect(self.update_text(b))
        #     self.timer.start(2000)

    def update(self):
        print(self.timer.isActive())
        self.button_1.setText('')
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication([])
    window = Game()
    window.show()
    app.exec()
