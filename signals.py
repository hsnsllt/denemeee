from PyQt5.QtCore import QObject, pyqtSignal

class AppSignals(QObject):
    member_added = pyqtSignal()
    payment_added = pyqtSignal()
