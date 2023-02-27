from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from datetime import datetime
from threading import Timer
import json
import time
import sys
import os

ID = None
PW = None
login_data_path = None
login_data_available = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Main_UI_path = resource_path("main.ui")
Main_UI_class = uic.loadUiType(Main_UI_path)[0]

Warning_UI_path = resource_path("warning_not_time.ui")
Warning_UI_class = uic.loadUiType(Warning_UI_path)[0]

class Main_Window(QMainWindow, Main_UI_class):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("수강신청을 자동으로 해보자")
        self.setupUi(self)
        self.load_id_pw()
        self.START.clicked.connect(self.get_id_pw)
        self.show_time()

    def load_id_pw(self):
        global ID
        global PW
        global login_data_available
        global login_data_path
        login_data_path = ("./id_pw.json")
        try:
            with open(login_data_path, "r") as f:
                data = json.load(f)
                ID = data["ID"]
                self.ID.setText(ID)
                PW = data["PW"]
                self.PW.setText(PW)
            login_data_available = True
        except FileNotFoundError:
            login_data_available = False

    def get_id_pw(self):
        global ID
        global PW
        global login_data_available
        ID = self.ID.text()
        PW = self.PW.text()
        data = {"ID" : ID,
                "PW" : PW}
        with open(login_data_path, "w") as f:
            json.dump(data, f, indent = 2)
        time.sleep(0.5)
        self.close()

    def show_time(self):
        time_now = datetime.now().strftime("%H : %M : %S")
        self.HOUR.display(time_now)

        timer = Timer(0.1, self.show_time)
        timer.start()

    def not_sugang_time(self):
        re = QMessageBox.warning(self, "수강신청 가능 기간이 아닙니다.",
                                  "Press OK to exit...",
                                  QMessageBox.Ok)

        if re == QMessageBox.Ok:
            print("close")
            self.close()

class Not_Sugang_Time(QDialog, Warning_UI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("수강신청 기간이 아닙니다")

    def exit_im(self):
        self.close()
        sys.exit()

def warning_not_sugang_time():
    app = QApplication(sys.argv)

    window = Not_Sugang_Time()
    window.show()

    app.exec_()

def login_gui():
    app = QApplication(sys.argv)

    window = Main_Window()
    window.show()
    
    app.exec_()

if __name__ == "__main__":
    login_gui()