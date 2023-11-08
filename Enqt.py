import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from threading import Thread
import time
from utils import RandomChose,SpideWords
import random

Equency = 1 #多久下一次
Numbers = 4 #每次下几个
ALLWORDS = []

class Thea_(QThread):
    moving_signal = QtCore.pyqtSignal(int,int)
    def __init__(self, parent=None,func=None,pos=()) -> None:
        super().__init__(parent)
        self.parent = parent
        self.func = func
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        
        self.speed=1
        self.switch = True
        self.first = True
    def run(self):
        self.fallint()

    def fallint(self):

        self.movingy = self.y
        # print(self.parent.parent.get_size().height())
        while True and self.switch:
            if self.first:
                time.sleep(random.randrange(4))
                self.first = False
            time.sleep(1/120)

            self.y = self.y+self.speed
            
                
            self.moving_signal.emit(self.x,self.y)
            self.movingy = self.y
            if self.y>self.parent.parent.get_size().height()-100:
                print('达到底部')
                change_flag = False
                self.change_word()
    def change_word(self):
        global ALLWORDS
        # print(self.parent.text(),self.parent.explain)
        ALLWORDS.insert(0,(self.parent.text(),self.parent.explain))
        word = ALLWORDS.pop()
        self.parent.setText(word[0])
        self.parent.explain = word[1]
        self.parent.adjustSize()
        self.y = -self.parent.height()
        self.moving_signal.emit(self.x,self.y)

class Word(QLabel):
    """下降的单词"""
    def __init__(self,text,parent=None,speed=0,explain=''):
        # super().__init__(text,parent)
        super().__init__(text)
        
        self.explain = explain
        self.parent = parent
        self.speed = speed
        self.switch = True
        self.defaultx = 0
        self.th = None

    def show_explain(self,create=True):
        if create:
            print('explain')
            print(self.parent)
            self.a=QLabel(text=self.explain,parent=self.parent)
            fonta = QFont()
            fonta.setPointSize(16)
            style = "background-color:rgba(0,0,0,100);color:rgb(200,200,200)"
            self.a.setFont(fonta)
            self.a.setStyleSheet(style)
            # self.a.setGeometry(pos[0],pos[1],300,50)
            self.a.adjustSize()
            pos = self.geometry().right(),self.geometry().top()
            if pos[0]+self.a.geometry().width()>self.parent.get_size().right():
                print("超了")
                pos = self.geometry().left()-self.a.geometry().width(),self.geometry().top()
                # self.a.move(pos[0],pos[1])
            self.a.move(pos[0],pos[1])
            self.a.show()
            # self.a.destroy()
        else:
            self.a.deleteLater()
        

    def set_parent(self):
        self.setParent(self.parent)

    def enterEvent(self, a0: QEvent) -> None:
        if self.th:
            self.last_speed = self.th.speed
            self.th.speed = 0
            
            # r,t = self.geometry().right(),self.geometry().top()
            self.show_explain()

    
    def leaveEvent(self, a0: QEvent) -> None:
        if self.th:
            self.th.speed = self.last_speed 
            self.show_explain(create=False)
    def moving(self):
        self.speed = 2
        i = 0
        geo = self.geometry()
        self.x = geo.x()
        self.y = geo.y()
        self.movingy = self.y
        while i < 7000 and self.switch:
            i+=1
            time.sleep(1/60)
            # geo = self.geometry()
            # self.move(geo.x(),geo.y()+self.speed)
            self.y = self.y+self.speed
            # print('x:',self.x,"y:",self.y)
            if self.y-self.movingy>1:
                self.move(self.x,self.y)
                self.movingy = self.y
        # print("final")

    def stop(self):
        self.th.switch = False

    def thread_move(self):
        # self.set_parent()
        self.th = Thea_(parent=self,func=self.moving,pos=(self.geometry().x(),self.geometry().y()))
        self.th.moving_signal.connect(lambda x,y:self.move(x,y))
        self.th.start()


class WordsManager:
    """单词管理"""
    def __init__(self,area:QRect,parent) -> None:
        self.rect = area
        self.parent = parent
        
        # self.loc = [self.rect.left(),self.rect.right()] #范围
        self.left_loc = RandomChose(self.rect.left(),self.rect.right())
        self.words = []
        self.falling = []  #正在下降的单词

        self.assign_Words = []
        self.switch = True  #线程开关
    
    def add_word(self,word:Word):
        self.words.append(word)

    def add_words(self,words:[Word]):
        self.words.extend(words)

    def assign_location(self):
        i = 0
        while i <len(self.words):
            # print(i)
            word = self.words[i]
            location = random.choice(self.left_loc.range_) #随机选择一个剩余位置
            if location[1]-location[0]>word.width():
                new_left = location[0]+int(random.random()*(location[1]-location[0]-word.width()))
                self.left_loc.divide(new_left,new_left+word.width())

                word.move(new_left,-word.height())   #移动到计算后的坐标处
                word.defaultx = new_left
                word.set_parent()
                print(i,'-------------------------------------')
                word.thread_move()      #开始下落
                self.assign_Words.append(word)
            i+=1
        #一起移动，减少线程数量
        # self.th = Thea_(func=self.move_all)
        # self.th.start()

    def move_all(self):
        location =  {}
        i=0
        while i < 9000 and self.switch:
            for word in self.assign_Words:
                if word not in location:
                    location[word] = [word.defaultx,0]
                    x,y = [word.defaultx,0]
                else:
                    x,y = location.get(word,[word.defaultx,0])
                    # print(f'x{x} y{y}')
                    print(i)
                i+=1
                time.sleep(1/1500000)
                # geo = self.geometry()
                # self.move(geo.x(),geo.y()+self.speed)
                # self.y = self.y+self.speed
                word.move(x,y+word.speed-1)
                location[word][1]+=word.speed-1


    def all_Stop(self):
        for word in self.assign_Words:
            word.stop()
        # self.switch=False

class CreateWords:
    def __init__(self,master) -> None:
        self.master = master
        self.native_words = []
        self.fonta = QFont()
        self.fonta.setPointSize(16)

        self.style = "background-color:rgba(100,100,100,10);color:rgb(200,200,200)"

        self.words_obj = []

    def add(self,native_word:tuple):
        self.native_words.append(native_word)
    
    def adds(self,native_words:[tuple]):
        self.native_words.extend(native_words)
    
    def creatWords_obj(self):
        words_list = []
        for word in self.native_words:
            word_obj = Word(text=word[0],parent=self.master,speed=2,explain=word[1])
            word_obj.setFont(self.fonta)
            word_obj.setStyleSheet(self.style)
            # word_obj.resize(word_obj.width(),int(word_obj.height()*1.3))
            word_obj.adjustSize() #自适应大小
            words_list.append(word_obj)
        self.words_obj.extend(words_list)
    
    def getWords_obj(self):
        return self.words_obj

class MainGui(QMainWindow):
    closesignal = pyqtSignal(str)
    def __init__(self, argv) -> None:
        super().__init__(argv)
        
        self.setGeometry(0,0,QDesktopWidget().screenGeometry().width(),QDesktopWidget().screenGeometry().height())
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint|
                            QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                         QtCore.Qt.WindowCloseButtonHint |  # 使能关闭按钮
                         QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端
        fonta = QFont()
        fonta.setPointSize(30)

        words = self.find_words()
        creator = CreateWords(self)     #批量创建Word对象
        # creator.adds(["A","B","C"])
        spide = SpideWords(r"E:\code\2_tkinter\English-pyqt\words.txt")
        global ALLWORDS
        ALLWORDS = spide.re_match()
        creator.adds(ALLWORDS)
        creator.creatWords_obj()

        self.wordsman = WordsManager(self.rect(),self)   #单词管理器，在一定范围内下单词雨
        self.wordsman.add_words(creator.getWords_obj())
        self.wordsman.assign_location()
        # self.wordsman.randomly_fall()

    def get_size(self):
        return self.geometry()
    def find_words(self):
        spide = SpideWords(r"E:\code\2_tkinter\English-pyqt\words.txt")
        words = spide.re_match()
        return words

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
        print('what')
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