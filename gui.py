#-*- coding: utf-8 -*-
from access_db import DB

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, 
    QMainWindow, QAction, QFileDialog, 
    QLabel, QScrollArea, QHBoxLayout, QSizePolicy, 
)
from PyQt5.QtWidgets import qApp
from PyQt5.QtGui import QIcon, QPixmap, QImage
from collections import OrderedDict

def unzip(zipped):
    return zip(*zipped)

FULL = 0
ORIGIN_H = 1
ORIGIN_W = 2
class MainWindow(QMainWindow):
    resize_signal = QtCore.pyqtSignal()
    def __init__(self, db, id_path_list):
        super().__init__()
        self.db = db

        self.img_paths = OrderedDict()
        for id_,path in id_path_list:
            self.img_paths[id_] = path
        #print(*self.img_paths.items(),sep='\n')

        #print(*self.ids, sep='\n')
        #print(*self.img_paths, sep='\n')
        work_state = self.db.get_work_state()
        if work_state is None:
            pass
        else:
            order,now_id = work_state
            assert order == sys.argv[1], "saved_order:'%s' != '%s':arg_order" % (order,sys.argv[1])
            print(order, now_id)
        self.img = QPixmap('./2706002.jpg')

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

        #pixmap = QPixmap('./670984.gif')
        origin_w = self.img.width()
        origin_h = self.img.height()
        #print('pixmap',origin_h,origin_w)

        if self.display_full == FULL:
            smaller = self.img.scaled(viewer_w, viewer_h, QtCore.Qt.KeepAspectRatio)
        elif self.display_full == ORIGIN_W:
            smaller = self.img.scaled(origin_w, viewer_h, QtCore.Qt.KeepAspectRatio)
        elif self.display_full == ORIGIN_H:
            smaller = self.img.scaled(viewer_w, origin_h, QtCore.Qt.KeepAspectRatio)
        self.img_label.setPixmap(smaller)
        self.img_label.adjustSize()

    #TODO: rearrange order of methods..
    def init_ui(self):
        #self.statusBar().showMessage('Ready')
        self.init_main_widget()

    def confirm(self):   
        print('confirmed!')

    def init_main_widget(self):
        self.img_label = QLabel()
        self.img_label.setScaledContents(True)
        self.img_viewer = QScrollArea() 
        self.img_viewer.setWidget(self.img_label)

        self.choice_viwer = QLabel()
        self.choice_viwer.setStyleSheet('font:70pt;')
        self.choice_viwer.setText('?')
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

            # confirm!
            elif e.key() == QtCore.Qt.Key_Return: # or Key_Enter
                self.confirm()

            # Selection etc..
            elif (e.key() == QtCore.Qt.Key_Exclam):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:green;'
                )
                self.choice_viwer.setText('!')
                
        self.img_viewer.keyPressEvent = keyPressEvent

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python gui.py desc')
        exit()

    order = sys.argv[1]
    with DB('szmc.db') as db:
        if order == 'incr':
            id_path_list = db.img_pathseq()
        elif order == 'desc':
            id_path_list = db.img_pathseq(incremental=False)
        else:
            print('Usage: python gui.py desc')
            exit()
        
        app = QApplication(sys.argv)
        ex = MainWindow(db, id_path_list)
        sys.exit(app.exec_())
