from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from datetime import datetime
from threading import Timer
import time
import sys
import os

ID = None
PW = None
isTime = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Main_UI_path = resource_path("main.ui")
Main_UI_class = uic.loadUiType(Main_UI_path)[0]

class Main_Window(QMainWindow, Main_UI_class):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("수강신청을 자동으로 해보자")
        self.setupUi(self)
        self.START.clicked.connect(self.get_id_pw)
        self.show_time()

    def get_id_pw(self):
        global ID
        global PW
        ID = self.ID.text()
        PW = self.PW.text()
        time.sleep(0.5)
        if not isTime:
            self.not_sugang_time()
        self.close()

    def show_time(self):
        global isTime
        time_now = datetime.now().strftime("%H : %M : %S")
        if time_now >= "10 : 00 : 00" and time_now < "17 : 00 : 00":
            isTime = True
        self.HOUR.display(time_now)

        timer = Timer(0.1, self.show_time)
        timer.start()

    def not_sugang_time(self):
        re = QMessageBox.question(self, "수강신청 가능 시간(10:00 ~ 17:00)이 아닙니다.", 
                                  "진행 시 로그인 후 예비 수강신청 목록 확인까지는 진행됩니다.",
                                  QMessageBox.Yes | QMessageBox.No)
        
        if re == QMessageBox.Yes:
            pass
        else:
            self.close()
            os._exit(os.X_OK)

def login_gui():
    app = QApplication(sys.argv)

    window = Main_Window()
    window.show()
    
    app.exec_()
    print(f'id : {ID}')
    print(f'pw : {PW}')

if __name__ == "__main__":
    login_gui()