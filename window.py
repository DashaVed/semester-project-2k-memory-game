from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication
from random import shuffle

import start_window
import main_window

card_list = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H', 'I', 'I']
shuffle(card_list)


class Start(QMainWindow, start_window.Ui_StartWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.ui = None
        self.start_window = None
        self.setupUi(self)
        self.main_window = Game()

        self.start_button.clicked.connect(lambda: self.start())

    def start(self):
        duration = 5
        self.main_window.show()
        self.main_window.label.setText(f'Game started in {duration} sec')
        timer = QTimer()
        timer.singleShot(5000, self.main_window.reset)
        window.hide()


class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(Game, self).__init__()
        self.setupUi(self)
        self.open_card = {}
        self.score = 0

        QTimer.singleShot(1, self.reset)

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
            self.score += 1
            self.label_score1.setText(f'Score: {self.score}')
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
        self.open_card = {}

        self.score = 0
        self.label_score1.setText('Score: 0')
        self.label_score2.setText('Score: 0')
        self.label.setText('Observe the cards and memories them!')

        for index, b in enumerate(button_list):
            self.reset_button(b, index)

    def reset_button(self, button, card):
        button.setEnabled(True)
        button.setText(card_list[card])
        button.setStyleSheet('QPushButton {background-color: #716799; color: #FFF352;}')
        QTimer().singleShot(3000, lambda: self.update_text(button))

    @staticmethod
    def update_text(button):
        button.setText('')


if __name__ == "__main__":
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
