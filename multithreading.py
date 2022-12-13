import traceback
import sys

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot


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
            except_type, value = sys.exc_info()[:2]
            self.signals.error.emit((except_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit()  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done