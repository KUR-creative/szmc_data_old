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

FULL = 0
ORIGIN_H = 1
ORIGIN_W = 2
class MainWindow(QMainWindow):
    resize_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.display_full = FULL

        self.showMaximized()
        self.resize_signal.connect(self.change_img_size)

    def resizeEvent(self, event):
        self.resize_signal.emit()
        return super(type(self), self).resizeEvent(event)

    def change_img_size(self):
        viewer_w = self.img_viewer.width()
        viewer_h = self.img_viewer.height()
        #print('img viewer',viewer_w,viewer_h)

        pixmap = QPixmap('./big.jpg')
        pixmap = QPixmap('./2706002.jpg')
        #pixmap = QPixmap('./670984.gif')
        origin_w = pixmap.width()
        origin_h = pixmap.height()
        #print('pixmap',origin_h,origin_w)

        if self.display_full == FULL:
            smaller = pixmap.scaled(viewer_w, viewer_h, QtCore.Qt.KeepAspectRatio)
        elif self.display_full == ORIGIN_W:
            smaller = pixmap.scaled(origin_w, viewer_h, QtCore.Qt.KeepAspectRatio)
        elif self.display_full == ORIGIN_H:
            smaller = pixmap.scaled(viewer_w, origin_h, QtCore.Qt.KeepAspectRatio)
        self.img_label.setPixmap(smaller)
        self.img_label.adjustSize()

    def init_ui(self):
        #self.statusBar().showMessage('Ready')
        self.init_main_widget()


    def init_main_widget(self):
        self.img_label = QLabel()
        self.img_label.setScaledContents(True)
        self.img_viewer = QScrollArea() 
        self.img_viewer.setWidget(self.img_label)

        self.choice_viwer = QLabel()
        self.choice_viwer.setStyleSheet('font:70pt;')
        self.choice_viwer.setText('_')
        self.choice_viwer.resize(200,100)

        self.choice_viwer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)

        hbox = QHBoxLayout()
        hbox.addWidget(self.img_viewer)
        hbox.addWidget(self.choice_viwer)

        self.main_widget = QWidget()
        self.main_widget.setLayout(hbox)
        self.setCentralWidget(self.main_widget)

        def keyPressEvent(e):
            #TODO: refactor with dict, eval, yml init file....
            #https://doc.qt.io/qt-5.9/qt.html#Key-enum
            # o a h n ? !
            # 0 1 2 3

            viewer_h = self.img_viewer.height()
            viewer_w = self.img_viewer.width()

            # Toggle view mode 
            if e.key() == QtCore.Qt.Key_F:
                self.display_full = (self.display_full + 1) % 3
                self.change_img_size()

            # vertical mode
            elif (e.key() == QtCore.Qt.Key_Up or
                e.key() == QtCore.Qt.Key_K):
                y = self.img_viewer.verticalScrollBar().value()
                self.img_viewer.verticalScrollBar().setValue(y - viewer_h)
            elif (e.key() == QtCore.Qt.Key_Down or
                  e.key() == QtCore.Qt.Key_J):
                y = self.img_viewer.verticalScrollBar().value()
                self.img_viewer.verticalScrollBar().setValue(y + viewer_h)

            # horizontal mode
            elif e.key() == QtCore.Qt.Key_Left:
                x = self.img_viewer.verticalScrollBar().value()
                self.img_viewer.horizontalScrollBar().setValue(x - viewer_w)
            elif e.key() == QtCore.Qt.Key_Right:
                x = self.img_viewer.verticalScrollBar().value()
                self.img_viewer.horizontalScrollBar().setValue(x + viewer_w)

            # Selection 
            elif (e.key() == QtCore.Qt.Key_O or
                  e.key() == QtCore.Qt.Key_0):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:black;'
                )
                self.choice_viwer.setText('nO\ntext')

            elif (e.key() == QtCore.Qt.Key_A or
                  e.key() == QtCore.Qt.Key_1):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:blue;'
                )
                self.choice_viwer.setText('All\neasy')

            elif (e.key() == QtCore.Qt.Key_H or
                  e.key() == QtCore.Qt.Key_2):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:magenta;'
                )
                self.choice_viwer.setText('Half\neasy')

            elif (e.key() == QtCore.Qt.Key_N or
                  e.key() == QtCore.Qt.Key_3):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:red;'
                )
                self.choice_viwer.setText('No\neasy')

            # Selection etc..
            elif (e.key() == QtCore.Qt.Key_Exclam):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:green;'
                )
                self.choice_viwer.setText('!')
                
        self.img_viewer.keyPressEvent = keyPressEvent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
