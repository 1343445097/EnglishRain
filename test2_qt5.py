import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from threading import Thread
import time
# 一、应用程序对象，只能有一个
# 1、该类管理GUI应用程序控制流和主要设置，专门用于QWidget所需的一些功能
# 2、不使用命令行或提示符程序（cmd），则为空列表 []
# 3、如果使用命令行或提示符程序(cmd)，则为sys.argv
class test_Label(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        fonta = QFont()
        fonta.setPointSize(16)
        style = "background-color:rgba(0,100,0,100);color:rgb(0,0,0)"
        self.text = '1234'
        self.setFont(fonta)
        self.setStyleSheet(style)
        self.setGeometry(100,100,200,200)
        # self.test()

    def test(self):
        a=QLabel(text="AAAAAAAA",parent=self.parent)
        fonta = QFont()
        fonta.setPointSize(16)
        style = "background-color:rgba(0,100,0,100);color:rgb(0,0,0)"
        a.setFont(fonta)
        a.setStyleSheet(style)
        a.setGeometry(300,0,100,100)
    def enterEvent(self, a0: QEvent) -> None:
        # return super().enterEvent(a0)
        print("enter")
        self.test()

class MainGui(QMainWindow):
    def __init__(self, argv) -> None:
        super().__init__(argv)
        self.setGeometry(0,0,1000,1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font = QFont()
        font.setPointSize(30)
        # font.set
        a=QLabel(text="explain",parent=self)
        fonta = QFont()
        fonta.setPointSize(16)
        style = "background-color:rgba(0,100,0,100);color:rgb(0,0,0)"
        a.setFont(fonta)
        a.setStyleSheet(style)
        a.setGeometry(0,0,100,100)
        # self.test()
        a=test_Label(self)
        # self.label = QLabel(text="1234",parent=self)
        # self.label.setFont(font)
        # self.label.setStyleSheet("color:blue")
        # self.label.setGeometry(0,0,200,200)

        # self.label2 = QLabel(text="1234",parent=self)
        # self.label2.setFont(font)
        # self.label2.setStyleSheet("background-color:rgba(10,10,10,80);color:blue")
        # self.label2.setGeometry(200,100,200,200)
        # self.label2.leaveEvent=self.labelleaveEvent
        # self.label2.enterEvent = self.labelenterEvent
        # self.thread_move()
        # self.label2.
    def test(self):
        a=QLabel(text="AAAAAAAA",parent=self)
        fonta = QFont()
        fonta.setPointSize(16)
        style = "background-color:rgba(0,100,0,100);color:rgb(0,0,0)"
        a.setFont(fonta)
        a.setStyleSheet(style)
        a.setGeometry(0,0,100,100)
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
    
    def moving(self):
        self.speed = 1
        for i in range(1600):
            time.sleep(1/120)
            geo = self.label2.geometry()
            self.label2.move(geo.x(),geo.y()+self.speed)

    def thread_move(self):
        th = Thread(target=self.moving)
        th.daemon=True
        th.start()

        

if __name__=='__main__':
    app = QApplication(sys.argv)

    s = MainGui(None)
    s.show()
    sys.exit(app.exec())