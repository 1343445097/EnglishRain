
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from threading import Thread
import time

class MainGui(QMainWindow):
    closesignal = pyqtSignal(str)
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.setGeometry(0,0,1000,1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        fonta = QFont()
        fonta.setPointSize(30)
        label = QLabel(text='123',parent=self)
        self.style = "background-color:rgba(100,100,100,10);color:rgb(200,0,0)"
        label.setStyleSheet(self.style)
        label.setFont(fonta)
        label.setParent(self)

        label2 = QLabel(text='aaa',parent=self)
        self.style = "background-color:rgba(100,100,100,10);color:rgb(200,0,0)"
        label2.setStyleSheet(self.style)
        label2.setFont(fonta)


    def labelleaveEvent(self,event):
        self.speed = self.before_speed
        print('label 离开')
    def labelenterEvent(self,event):
        print('label 进入')
        self.before_speed = self.speed
        self.speed = 0
        
    def move(self):
        self.label2.move(700,600)
        geo = self.label2.geometry()
        print(geo.x(),geo.y())
        # print(dir(self.label2.geometry()))

    
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key()==Qt.Key_Escape:

            self.wordsman.all_Stop()
            time.sleep(0.1)
            self.close()

        else:
            return super().keyPressEvent(a0)

        

if __name__=='__main__':
    app = QApplication(sys.argv)

    s = MainGui(None)
    s.show()
    print("exit")
    sys.exit(app.exec())