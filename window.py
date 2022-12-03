import socket
import threading

from PyQt6.QtWidgets import QMainWindow, QApplication

import main_window


# пишем своё MainWindow, основанное на Ui_MainWindow (которое мы ранее сгенерировали)
class Game(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        # в методе инициализации мы вызываем родительскую инициализацию (устанавливаем элементы интерфейса)
        super(Game, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    # при запуске клиента мы создаем инстанс приложения, созданного нами главного окна, и все запускаем
    app = QApplication([])
    window = Game()
    window.show()
    app.exec()
