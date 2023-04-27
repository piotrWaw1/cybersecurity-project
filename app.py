from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QWidget, QStackedWidget
import sys


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("ui/app_ui.ui", self)
        self.setWindowTitle("app")

        # pages
        self.stack = self.findChild(QStackedWidget, "stackedWidget")
        # menu buttons
        self.init_pages()

        self.show()

    def init_pages(self):
        self.home = self.findChild(QPushButton, "home_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_1")))
        self.keylogger = self.findChild(QPushButton, "keylogger_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_2")))
        self.ransomware = self.findChild(QPushButton, "ransomware_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_3")))
        self.worm = self.findChild(QPushButton, "worm_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_4")))
        self.wifi = self.findChild(QPushButton, "wifi_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_5")))
        self.zip = self.findChild(QPushButton, "zip_button").clicked.connect(
            lambda: self.stack.setCurrentWidget(self.findChild(QWidget, "page_6")))

app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())