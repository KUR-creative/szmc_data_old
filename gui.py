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
    resize_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.display_full = True

        self.showMaximized()
        self.resize_signal.connect(self.change_img_size)

    def resizeEvent(self, event):
        self.resize_signal.emit()
        return super(type(self), self).resizeEvent(event)

    def change_img_size(self):
        viewer_w = self.img_viewer.width()
        viewer_h = self.img_viewer.height()
        #print('img viewer',viewer_w,viewer_h)

        pixmap = QPixmap('./2706002.jpg')
        #pixmap = QPixmap('./670984.gif')
        origin_w = pixmap.width()
        origin_h = pixmap.height()
        #print('pixmap',origin_h,origin_w)

        if self.display_full:
            smaller = pixmap.scaled(viewer_w, viewer_h, QtCore.Qt.KeepAspectRatio)
        else:
            smaller = pixmap.scaled(viewer_w, origin_h, QtCore.Qt.KeepAspectRatio)
        self.img_label.setPixmap(smaller)
        self.img_label.adjustSize()

    def init_ui(self):
        #self.setGeometry(200, 200, 850, 750)
        #self.setWindowTitle('Sick Zil Machine  ver 0.0.0')    
        #self.statusBar().showMessage('Ready')
        self.init_main_widget()


    def init_main_widget(self):
        self.img_label = QLabel()
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
            #https://doc.qt.io/qt-5.9/qt.html#Key-enum
            # o a h n ? !
            viewer_h = self.img_viewer.height()
            if e.key() == QtCore.Qt.Key_Up:
                y = self.img_viewer.verticalScrollBar().value()
                print('y',self.img_viewer.verticalScrollBar().value())
                print('up')
                self.img_viewer.verticalScrollBar().setValue(y - viewer_h)
            elif e.key() == QtCore.Qt.Key_Down:
                y = self.img_viewer.verticalScrollBar().value()
                self.img_viewer.verticalScrollBar().setValue(y + viewer_h)
                print('y',self.img_viewer.verticalScrollBar().value())
                print('down')
            elif e.key() == QtCore.Qt.Key_Left:
                print('left')
            elif e.key() == QtCore.Qt.Key_Right:
                print('right')
            elif e.key() == QtCore.Qt.Key_F:
                self.display_full = (not self.display_full)
                self.change_img_size()
        self.img_viewer.keyPressEvent = keyPressEvent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
