from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("app_ui.ui", self)
        self.setWindowTitle("app")

        self.show()


app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())
