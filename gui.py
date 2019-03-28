#-*- coding: utf-8 -*-
from access_db import img_pathseq

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, 
    QMainWindow, QAction, QFileDialog, 
    QLabel, QScrollArea, QHBoxLayout, QSizePolicy, 
)
from PyQt5.QtWidgets import qApp
from PyQt5.QtGui import QIcon, QPixmap, QImage

class MainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.show()

        self.showMaximized()

        self.resized.connect(self.someFunction)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(type(self), self).resizeEvent(event)
    def someFunction(self):
        print("someFunction")
 
        ih = self.img_viewer.height()
        iw = self.img_viewer.width()
        print('img viewer',ih,iw)

        h = self.img_label.height()
        w = self.img_label.width()
        print('img label',h,w)

        pixmap = QPixmap('./2706002.jpg')
        h = pixmap.height()
        w = pixmap.width()
        print('pixmap',h,w)
        #self.img_label.setPixmap(pixmap)
        smaller = pixmap.scaled(iw, h, QtCore.Qt.KeepAspectRatio)
        #smaller = pixmap.scaled(iw, ih, QtCore.Qt.KeepAspectRatio)
        self.img_label.setPixmap(smaller)
        self.img_label.adjustSize()

        h = smaller.height()
        w = smaller.width()
        print('smaller pixmap',h,w)

        h = self.img_label.height()
        w = self.img_label.width()
        print('img label after adjust size',h,w)
        #self.img_label.setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio))

    def init_ui(self):
        #self.setGeometry(200, 200, 850, 750)
        #self.setWindowTitle('Sick Zil Machine  ver 0.0.0')    
        #self.statusBar().showMessage('Ready')
        self.init_main_widget()


    def init_main_widget(self):
        #pixmap = QPixmap('./2706002.jpg')

        self.img_label = QLabel()
        #self.img_label.setPixmap(pixmap.scaled(w,h,PyQt5.QtCore.Qt.KeepAspectRatio))
        #pixmap = QPixmap('./2706002.jpg')
        #self.img_label.setPixmap(pixmap)
        self.img_label.setScaledContents(True)
        self.img_viewer = QScrollArea() 
        h = self.img_label.height()
        w = self.img_label.width()
        print(h,w)
        #TODO: 이미지 확대/추가, 마우스 휠 눌러서 옮기기 구현하기.      
        self.img_viewer.setWidget(self.img_label)

        self.choice_viwer = QLabel()
        self.choice_viwer.setStyleSheet('font:70pt;')
        self.choice_viwer.setText('T')
        self.choice_viwer.resize(200,100)

        self.choice_viwer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)

        hbox = QHBoxLayout()#Horizontal, 수평으로 배치.
        hbox.addWidget(self.img_viewer)
        hbox.addWidget(self.choice_viwer)

        self.main_widget = QWidget()
        self.main_widget.setLayout(hbox)
        self.setCentralWidget(self.main_widget)

        def keyPressEvent(e):
            if e.key() == QtCore.Qt.Key_Up:
                print('up')
            elif e.key() == QtCore.Qt.Key_Down:
                print('down')
            elif e.key() == QtCore.Qt.Key_Left:
                print('left')
            elif e.key() == QtCore.Qt.Key_Right:
                print('right')
        self.img_viewer.keyPressEvent = keyPressEvent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
