#!/usr/bin/env python
'''
    Create a slate for vfx
    File name: slater.py
    Author: Suzanne Berger
    Date created: 02/07/2019
    Python Version: 2.7
    '''

import sys
import os
import logging
from datetime import date
from pprint import pprint

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2 import QtUiTools

#########################################################
# globals
#########################################################

VERSION = "V01"

logging.basicConfig(level=logging.INFO)
logging.info( " %s Version %s" % (sys.argv[0], VERSION))

TESTSHOW = "FACING THE BEAST"

PROGPATH = "/Users/suzanneberger/Documents/dev/slater"
BGSLATE = os.path.join(PROGPATH,"bgslate.png")
THUMBNAIL = os.path.join(PROGPATH, "slate_thumbnail.jpg")
TESTSLATE = os.path.join(PROGPATH, "testSlate_02.jpg")

#########################################################
# Slater
#########################################################

class Slater(QtWidgets.QWidget):

    def __init__(self, parent=None, movie=None, artist=None):
        
        super(Slater, self).__init__(parent)
        
        self.thumb_file = None
        
        self.movie = movie
        if not self.movie:
            self.movie = os.getenv("SHOW")
            if not self.movie:
                self.movie = "!!! Enter Movie Title  !!!"

        self.artist = artist
        if not self.artist:
            self.artist = os.getenv("LOGNAME")      # this env depends on platform

        self.initUI()
        #self.connectSignals()
        self.show()

    def initUI(self):
        self.setGeometry(100, 80, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Slater')
        
        self.slatebox = QtWidgets.QGroupBox()
        self.slatebox.setStyleSheet('QGroupBox {border: none;}')

        # load slate background image and resize to slate size
        oImage = QtGui.QImage(BGSLATE)
        sImage = QtGui.QPixmap(oImage.scaled(QtCore.QSize(1280,720)))
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, sImage)
        self.setPalette(palette)

        self.thumbnail_label = QtWidgets.QLabel("LOAD THUMBNAIL")
        self.thumbnail_label.setFixedSize(500, 280)
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail_label.setFont(QtGui.QFont("Times", 36, QtGui.QFont.Bold))
        self.thumbnail_label.setStyleSheet('QLabel {background-color: gray; color: darkRed;}')
        
        thumbnail_layout = QtWidgets.QHBoxLayout()
        thumbnail_layout.addSpacing(500)
        thumbnail_layout.addWidget(self.thumbnail_label)

        self.title_label = QtWidgets.QLabel(self.movie)
        self.title_label.setFixedSize(400,51)
        self.title_label.setFont(QtGui.QFont("Times", 36, QtGui.QFont.Bold))
        self.title_label.setStyleSheet('QLabel { color: blue }')
        self.title_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.shot_lineEdit, shot_layout = self.mk_lineEdit(QtWidgets.QLabel('shot: '))
        self.filename_lineEdit, filename_layout = self.mk_lineEdit(QtWidgets.QLabel('filename: '))
        self.artist_lineEdit, artist_layout = self.mk_lineEdit(QtWidgets.QLabel('artist: '))
        self.framerange_lineEdit, framerange_layout = self.mk_lineEdit(QtWidgets.QLabel('frame range: '))
        self.date_lineEdit, date_layout = self.mk_lineEdit(QtWidgets.QLabel('date: '))
        self.notes_lineEdit, notes_layout = self.mk_lineEdit(QtWidgets.QLabel('notes:   '), 175, 600, 520)

        self.artist_lineEdit.setText(self.artist)
        self.date_lineEdit.setText(str(date.today()))

        slateboxLayout = QtWidgets.QVBoxLayout()
        slateboxLayout.addSpacing(10)
        slateboxLayout.addLayout(thumbnail_layout)
        slateboxLayout.addStretch()
        slateboxLayout.addWidget(self.title_label)
        slateboxLayout.addSpacing(10)
        slateboxLayout.addLayout(shot_layout)
        slateboxLayout.addLayout(filename_layout)
        slateboxLayout.addLayout(artist_layout)
        slateboxLayout.addLayout(framerange_layout)
        slateboxLayout.addLayout(date_layout)
        slateboxLayout.addLayout(notes_layout)
        slateboxLayout.addSpacing(150)
        self.slatebox.setLayout(slateboxLayout)
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.slatebox)
        self.setLayout(mainLayout)


    def closeEvent(self, event):
        event.accept()

    def mk_lineEdit(self, this_label, label_width=140, line_width=200, layout_rightspace=850):
        this_label.setFixedSize(label_width, 27)
        this_label.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Normal))
        this_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        this_label.setStyleSheet('QLabel { color: lightGray }')
        this_lineEdit = QtWidgets.QLineEdit()
        this_lineEdit.setFixedSize(line_width, 27)
        this_lineEdit.setFont(QtGui.QFont("Helvetica", 18, QtGui.QFont.Medium))
        col = QtGui.QColor(180, 180, 180)
        this_lineEdit.setStyleSheet("QWidget {background-color: %s; border: 1px transparent}" % col.name())
        
        this_layout = QtWidgets.QHBoxLayout()
        this_layout.addWidget(this_label)
        this_layout.addWidget(this_lineEdit)
        this_layout.addSpacing(layout_rightspace)

        return this_lineEdit, this_layout

    def set_thumbnail(self, thumb_file):
        self.thumbnail = QtGui.QPixmap(thumb_file).scaled(500, 280)
        self.thumbnail_label.setPixmap(self.thumbnail)

class SlaterWin(QtWidgets.QWidget):
    
    def __init__(self, parent=None, movie=None):
        super(SlaterWin, self).__init__(parent)
        
        self.movie = movie
        if not self.movie:
            self.movie = os.getenv("SHOW")
            if not self.movie:
                self.movie = " !!! Enter Movie Title  !!!"
        
        self.initUI()

    def initUI(self):
    
        self.setGeometry(100, 840, 1280, 100)
        self.setWindowTitle('Make Slate')
    
        self.thumbnail_button = QtWidgets.QPushButton("Load Thumbnail")
        self.status_lineEdit = QtWidgets.QLineEdit()
        self.status_lineEdit.setMinimumWidth(800)
        self.status_lineEdit.setText("Status:")
        self.status_lineEdit.setReadOnly(True)
        self.save_button = QtWidgets.QPushButton("Save Slate")
        self.close_button = QtWidgets.QPushButton("Close")


        slatebuttons_layout = QtWidgets.QHBoxLayout()
        slatebuttons_layout.addWidget(self.thumbnail_button)
        slatebuttons_layout.addWidget(self.status_lineEdit)
        slatebuttons_layout.addStretch()
        slatebuttons_layout.addWidget(self.save_button)
        slatebuttons_layout.addWidget(self.close_button)
        
        self.show_label = QtWidgets.QLabel("Show: ")
        self.show_lineEdit = QtWidgets.QLineEdit()
        if os.getenv("SHOW"):
            self.show_lineEdit.setText(os.getenv("SHOW"))
        self.shot_label = QtWidgets.QLabel("Shot: ")
        self.shot_lineEdit = QtWidgets.QLineEdit()
        self.artist_label = QtWidgets.QLabel("Artist: ")
        self.artist_lineEdit = QtWidgets.QLineEdit()
        self.artist_lineEdit.setText(os.getenv("LOGNAME"))      # this env depends on platform
        
        slatedata_layout = QtWidgets.QHBoxLayout()
        slatedata_layout.addWidget(self.show_label)
        slatedata_layout.addWidget(self.show_lineEdit)
        slatedata_layout.addWidget(self.shot_label)
        slatedata_layout.addWidget(self.shot_lineEdit)
        slatedata_layout.addWidget(self.artist_label)
        slatedata_layout.addWidget(self.artist_lineEdit)
       
        slatewin_layout = QtWidgets.QVBoxLayout()
        slatewin_layout.addLayout(slatedata_layout)
        slatewin_layout.addLayout(slatebuttons_layout)
        self.setLayout(slatewin_layout)
        
        self.thumbnail_button.clicked.connect(self.loadthumb)
        self.save_button.clicked.connect(self.saveslate)
        self.close_button.clicked.connect(self.close)
        self.show_lineEdit.returnPressed.connect(self.on_showEdit)
        self.shot_lineEdit.returnPressed.connect(self.on_shotEdit)
        self.artist_lineEdit.returnPressed.connect(self.on_artistEdit)

        self.show()
        self.slateframe = Slater()

    def closeEvent(self, event):
        self.slateframe.close()
        event.accept()

    def loadthumb(self):
        #self.slateframe.set_thumbnail(THUMBNAIL)
        thumbfile = QtWidgets.QFileDialog.getOpenFileName(self,'Load Thumbnail Image File',
                                                          PROGPATH,
                                                          "Image files (*.jpg *.png *.tif)")[0]
        self.slateframe.set_thumbnail(thumbfile)
        self.status_lineEdit.setText("Status: Loaded Thumbnail Image from File: %s" % thumbfile)

    def saveslate(self):
        this_slate = self.slateframe.grab()
        #slate_file = TESTSLATE
        slatefile = QtWidgets.QFileDialog.getSaveFileName(self, "Save Slate to File",
                                                   PROGPATH,
                                                   "Images (*.jpg *.png *.tif)")[0]
        this_slate.save(slatefile)
        self.status_lineEdit.setText("Status: Saved Slate Image to File: %s" % slatefile)

    def on_showEdit(self):
        show_title = self.show_lineEdit.text()
        self.slateframe.title_label.setText(show_title)

    def on_shotEdit(self):
        shot = self.shot_lineEdit.text()
        self.slateframe.shot_lineEdit.setText(shot)

    def on_artistEdit(self):
        artist = self.artist_lineEdit.text()
        self.slateframe.artist_lineEdit.setText(artist)


#########################################################
# main
#########################################################

if __name__ == '__main__':
    
    os.environ["SHOW"] = TESTSHOW     # test only env SHOW variable should be set outside
    
    app = QtWidgets.QApplication(sys.argv)
    slaterwin = SlaterWin()
    sys.exit(app.exec_())

