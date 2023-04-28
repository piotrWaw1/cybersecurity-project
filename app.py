from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QWidget, QStackedWidget
import sys

# to open designer
# qt5-tools designer

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("ui/app_ui.ui", self)
        self.setWindowTitle("app")

        # pages
        self.stack = self.findChild(QStackedWidget, "stackedWidget")
        # menu buttons
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

        # ransomware
        self.r_stack = self.findChild(QStackedWidget, "ransom_stack")
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_1"))  # set to first page
        self.r_1 = self.findChild(QPushButton, "ransom_bt__1").clicked.connect(self.ransom_start)
        self.r_2 = self.findChild(QPushButton, "ransom_bt__2").clicked.connect(self.ransom_keys)
        self.r_3 = self.findChild(QPushButton, "ransom_bt__3").clicked.connect(self.ransom_send)
        self.r_4 = self.findChild(QPushButton, "ransom_bt__4").clicked.connect(self.ransom_run)
        self.r_5 = self.findChild(QPushButton, "ransom_bt__5").clicked.connect(self.ransom_decrypt)
        self.r_6 = self.findChild(QPushButton, "ransom_bt__6").clicked.connect(self.ransom_return)

        self.show()

    def ransom_start(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_2"))

    def ransom_keys(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_3"))

    def ransom_send(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_4"))

    def ransom_run(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_5"))

    def ransom_decrypt(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_6"))

    def ransom_return(self):
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_1"))

app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())