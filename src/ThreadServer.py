from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import socket

HOST = '127.0.0.1'
PORT = 50007

class ServerThread(QThread):
    somethingHappened = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))

        while 1:
            s.listen(1)
            conn, addr = s.accept()
            data = ''
            while 1:
                d = conn.recv(1024)
                if not d:
                    break
                data += d

            self.somethingHappened.emit(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.newThread = ServerThread()
        self.newThread.somethingHappened.connect(self.onSomethingHappened)
        # self.newThread.finished.connect(self.close)
        self.newThread.start()

        self.label = QLabel('')
        self.setCentralWidget(self.label)

    def onSomethingHappened(self, s):
        self.label.setText(self.label.text() + '\n' + s)

import sys
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

