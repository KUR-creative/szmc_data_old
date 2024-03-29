'''
Simple gui for selecting text state of image
select O / A / H / N !
'''
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

def unzip(zipped):
    return zip(*zipped)

class Session:
    def __init__(self, id_path_list, now_id=None):
        self.ids,_ = unzip(id_path_list)
        self.path_dic = {id:path for id,path in id_path_list}
        self._idx = self.ids.index(now_id) if now_id else 0
    
    def id_path(self):
        now_id = self.ids[self._idx]
        return now_id, self.path_dic[now_id]

    def id(self): 
        return self.ids[self._idx]

    def path(self):
        now_id = self.ids[self._idx]
        return self.path_dic[now_id]

    def next(self):
        last_idx = len(self.ids) - 1
        if self._idx < last_idx:
            self._idx += 1

    def prev(self):
        if self._idx > 0:
            self._idx -= 1

disp_mode = ['Full','Original Height','Original Width']
FULL = 0
ORIGIN_H = 1
ORIGIN_W = 2
class MainWindow(QMainWindow):
    resize_signal = QtCore.pyqtSignal()
    def resizeEvent(self, event):
        self.resize_signal.emit()
        return super(type(self), self).resizeEvent(event)

    def __init__(self, db, id_path_list):
        super().__init__()
        self.resize_signal.connect(self.display_image)

        # immutable references
        self.order = sys.argv[1]
        self.db = db

        # states
        self.init_session()
        self.disp_mode = FULL
        self.now_text = '?'
        self.img = QPixmap(self.session.path())

        # init gui
        self.init_main_widget()
        self.update_statusBar()
        self.showMaximized()

    def init_session(self):
        work_state = self.db.get_work_state()
        if work_state is None:
            self.session = Session(id_path_list)
            db.update_work_state(self.order, self.session.id())
        else:
            order,now_id = work_state
            assert order == self.order, "saved_order:'%s' != '%s':arg_order" % (order,self.order)
            self.session = Session(id_path_list, now_id)

    def update_statusBar(self):
        len_ids = len(self.session.ids) 
        now_idx = self.session._idx # incr
        percent = 100 * (now_idx / len_ids)
        msg = 'id: {} / mode: {} / {}/{}({:3.4f}%)'\
              .format(self.session.id(), disp_mode[self.disp_mode],
                      now_idx, len_ids, percent)
        self.statusBar().showMessage(msg)

    def display_image(self):
        viewer_w = self.img_viewer.width()
        viewer_h = self.img_viewer.height()
        origin_w = self.img.width()
        origin_h = self.img.height()

        if self.disp_mode == FULL:
            w,h = viewer_w, viewer_h
        elif self.disp_mode == ORIGIN_W:
            w,h = origin_w, viewer_h
        elif self.disp_mode == ORIGIN_H:
            w,h = viewer_w, origin_h
        smaller = self.img.scaled(w, h, QtCore.Qt.KeepAspectRatio)
        self.img_label.setPixmap(smaller)
        self.img_label.adjustSize()

    def confirm(self):   
        # save current selection
        self.db.update_data(self.session.id(), self.now_text)

        self.session.next()
        self.db.update_work_state(self.order, self.session.id())

        # initialize next selection
        self.img = QPixmap(self.session.path())
        self.display_image()
        self.now_text = '?'
        self.choice_viwer.setText(self.now_text)
        self.update_statusBar()
        # init position of scrollbars
        self.img_viewer.verticalScrollBar().setValue(0)
        self.img_viewer.horizontalScrollBar().setValue(0)

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
                self.disp_mode = (self.disp_mode + 1) % 3
                self.display_image()
                self.update_statusBar()

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
                x = self.img_viewer.horizontalScrollBar().value()
                self.img_viewer.horizontalScrollBar().setValue(x - viewer_w)
            elif e.key() == QtCore.Qt.Key_Right:
                x = self.img_viewer.horizontalScrollBar().value()
                self.img_viewer.horizontalScrollBar().setValue(x + viewer_w)

            # Selection 
            elif (e.key() == QtCore.Qt.Key_O or
                  e.key() == QtCore.Qt.Key_0):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:black;'
                )
                self.choice_viwer.setText('nO\ntext')
                self.now_text = 'O'

            elif (e.key() == QtCore.Qt.Key_A or
                  e.key() == QtCore.Qt.Key_1 or
                  e.key() == QtCore.Qt.Key_Space ):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:blue;'
                )
                self.choice_viwer.setText('All\neasy')
                self.now_text = 'A'

            elif (e.key() == QtCore.Qt.Key_H or
                  e.key() == QtCore.Qt.Key_2):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:magenta;'
                )
                self.choice_viwer.setText('Half\neasy')
                self.now_text = 'H'

            elif (e.key() == QtCore.Qt.Key_N or
                  e.key() == QtCore.Qt.Key_3):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:red;'
                )
                self.choice_viwer.setText('No\neasy')
                self.now_text = 'N'

            # confirm!
            elif e.key() == QtCore.Qt.Key_Return: # or Key_Enter
                if self.now_text != '?':
                    self.confirm()

            # Selection etc..
            elif (e.key() == QtCore.Qt.Key_Exclam or
                  e.key() == QtCore.Qt.Key_BracketLeft):
                self.choice_viwer.setStyleSheet(
                    'font:70pt; font-weight:bold; color:green;'
                )
                self.choice_viwer.setText('!')
                self.now_text = '!'
                
            #print('v:',self.img_viewer.verticalScrollBar().value())
            #print('h:',self.img_viewer.horizontalScrollBar().value())

        self.img_viewer.keyPressEvent = keyPressEvent

import unittest
class TestSession(unittest.TestCase):
    def test_ctor(self):
        sess = Session([(1,2),(3,4),(5,6)], 3)
        self.assertEqual(sess.path_dic, {1:2, 3:4, 5:6})
        self.assertEqual(sess.id_path(), (3,4))
        sess = Session([(1,2),(3,4),(5,6)])
        self.assertEqual(sess.path_dic, {1:2, 3:4, 5:6})
        self.assertEqual(sess.id_path(), (1,2))
    def test_id_path(self):
        sess = Session([(1,2),(3,4),(5,6)], 1)
        self.assertEqual(sess.id_path(), (1,2))
    def test_next(self):
        sess = Session([(1,2),(3,4),(5,6)], 1)
        self.assertEqual(sess.id_path(), (1,2)); sess.next()
        self.assertEqual(sess.id_path(), (3,4)); sess.next()
        self.assertEqual(sess.id_path(), (5,6)); sess.next()
        self.assertEqual(sess.id_path(), (5,6)); sess.next()
        self.assertEqual(sess.id_path(), (5,6))
    def test_prev(self):
        sess = Session([(1,2),(3,4),(5,6)], 1)
        sess.prev(); self.assertEqual(sess.id_path(), (1,2)) 
        sess.prev(); self.assertEqual(sess.id_path(), (1,2)) 
        sess.next(); self.assertEqual(sess.id_path(), (3,4)) 
        sess.next(); self.assertEqual(sess.id_path(), (5,6)) 

if __name__ == '__main__':
    #unittest.main()
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
