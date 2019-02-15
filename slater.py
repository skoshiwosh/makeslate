#!/usr/bin/env python
"""
    Create a slate for visual effects dailies
    
    File name: slater.py
    Author: Suzanne Berger
    Email: zanefx7@gmail.com
    Date created: 02/07/2019
    Python Version: 2.7
"""

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

# use as default for artist entry
if sys.platform == "win32":
    USERNAME = os.getenv("USERNAME")
else:
    USERNAME = os.getenv("USER")

# replace with appropriate to facilities packaging/release system
PROGPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
BGSLATE = os.path.join(PROGPATH,"bgslate.png")

#########################################################
# Slater
#########################################################

class Slater(QtWidgets.QWidget):
    """This widget displays slate show/shot data along with thumbnail image and can be saved as an image file."""
    
    def __init__(self, parent=None, movie=None, shot=None, artist=None):
        super(Slater, self).__init__(parent)
        
        self.movie = movie
        if not self.movie:      # remind the user to enter show title
            self.movie = "!!! Enter Movie Title  !!!"
        self.shot = shot
        self.artist = artist

        self.initUI()
        self.show()

    def initUI(self):
        """Create and initialize widgets and layouts for this object."""
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

        # thumbnail image will be contained in this QLabel
        self.thumbnail_label = QtWidgets.QLabel("LOAD THUMBNAIL")
        self.thumbnail_label.setFixedSize(500, 280)
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail_label.setFont(QtGui.QFont("Times", 36, QtGui.QFont.Bold))
        self.thumbnail_label.setStyleSheet('QLabel {background-color: gray; color: darkRed;}')
        
        thumbnail_layout = QtWidgets.QHBoxLayout()
        thumbnail_layout.addSpacing(500)
        thumbnail_layout.addWidget(self.thumbnail_label)

        self.movie_label = QtWidgets.QLabel(self.movie)
        self.movie_label.setFixedSize(400,51)
        self.movie_label.setFont(QtGui.QFont("Times", 36, QtGui.QFont.Bold))
        self.movie_label.setStyleSheet('QLabel { color: blue }')
        self.movie_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        # these lineEdits allow user input although some can also be input or initialized from SlateWin object
        self.shot_lineEdit, shot_layout = self.mk_lineEdit(QtWidgets.QLabel('shot: '))
        self.filename_lineEdit, filename_layout = self.mk_lineEdit(QtWidgets.QLabel('filename: '))
        self.artist_lineEdit, artist_layout = self.mk_lineEdit(QtWidgets.QLabel('artist: '))
        self.framerange_lineEdit, framerange_layout = self.mk_lineEdit(QtWidgets.QLabel('frame range: '))
        self.date_lineEdit, date_layout = self.mk_lineEdit(QtWidgets.QLabel('date: '))
        self.notes_lineEdit, notes_layout = self.mk_lineEdit(QtWidgets.QLabel('notes:   '), 175, 600, 520)

        if self.artist:
            self.artist_lineEdit.setText(self.artist)
        if self.shot:
            self.shot_lineEdit.setText(self.shot)
        self.date_lineEdit.setText(str(date.today()))

        # set overall layout to make a nice slate image when grabbed as a QPixmap
        slateboxLayout = QtWidgets.QVBoxLayout()
        slateboxLayout.addSpacing(10)
        slateboxLayout.addLayout(thumbnail_layout)
        slateboxLayout.addStretch()
        slateboxLayout.addWidget(self.movie_label)
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
        """Make labels, lineEdits and layouts for slate entry fields."""
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
        """Load thumbnail image file into a QPixMap and set the corresponding QLabel."""
        self.thumbnail = QtGui.QPixmap(thumb_file).scaled(500, 280)
        self.thumbnail_label.setPixmap(self.thumbnail)


############################################################
# SlaterWin
############################################################

class SlaterWin(QtWidgets.QWidget):
    """This widget creates a Slater widget object and it contains input fields and buttons for 
       initializing and saving a slate image file.
    """
    
    def __init__(self, parent=None):
        super(SlaterWin, self).__init__(parent)
        
        # optionally set these environment variables outside script to initialize corresponding widgets
        self.movie = os.getenv("SHOW")
        self.shot = os.getenv("SHOT")
        self.artist = os.getenv("ARTIST")
        if not self.artist:
            self.artist = USERNAME
        
        self.initUI()

    def initUI(self):
        """Create and initialize widgets and layouts for this object."""
        self.setGeometry(100, 840, 1280, 100)
        self.setWindowTitle('Make Slate')
    
        self.setStyleSheet("QPushButton {color: black; min-width: 100px; min-height: 35px;}")
        
        # create show title, shot and artist labels and lineEdits for input into Slater widget
        self.show_label = QtWidgets.QLabel("Show: ")
        self.show_lineEdit = QtWidgets.QLineEdit()
        if self.movie:
            self.show_lineEdit.setText(self.movie)
        
        self.shot_label = QtWidgets.QLabel("Shot: ")
        self.shot_lineEdit = QtWidgets.QLineEdit()
        if self.shot:
            self.shot_lineEdit.setText(self.shot)
        
        self.artist_label = QtWidgets.QLabel("Artist: ")
        self.artist_lineEdit = QtWidgets.QLineEdit(self.artist)
        
        
        self.thumbnail_button = QtWidgets.QPushButton("Load Thumbnail")
        self.save_button = QtWidgets.QPushButton("Save Slate")
        
        slate_input_layout = QtWidgets.QHBoxLayout()
        slate_input_layout.addWidget(self.show_label)
        slate_input_layout.addWidget(self.show_lineEdit)
        slate_input_layout.addWidget(self.shot_label)
        slate_input_layout.addWidget(self.shot_lineEdit)
        slate_input_layout.addWidget(self.artist_label)
        slate_input_layout.addWidget(self.artist_lineEdit)
        slate_input_layout.addSpacing(40)
        slate_input_layout.addWidget(self.thumbnail_button)
        slate_input_layout.addWidget(self.save_button)

        # create widgets and layout to be placed at bottom of window
        status_label = QtWidgets.QLabel("Status: ")
        self.status_lineEdit = QtWidgets.QLineEdit()
        self.status_lineEdit.setMinimumWidth(850)
        self.status_lineEdit.setReadOnly(True)
        self.close_button = QtWidgets.QPushButton("Close")
        
        slate_bottom_layout = QtWidgets.QHBoxLayout()
        slate_bottom_layout.addWidget(status_label)
        slate_bottom_layout.addWidget(self.status_lineEdit)
        slate_bottom_layout.addStretch()
        slate_bottom_layout.addWidget(self.close_button)

        # add layouts to overall window layout
        slatewin_layout = QtWidgets.QVBoxLayout()
        slatewin_layout.addLayout(slate_input_layout)
        slatewin_layout.addLayout(slate_bottom_layout)
        self.setLayout(slatewin_layout)
        
        # connect signal to slots for updating slate
        self.thumbnail_button.clicked.connect(self.loadthumb)
        self.save_button.clicked.connect(self.saveslate)
        self.close_button.clicked.connect(self.close)
        self.show_lineEdit.returnPressed.connect(self.on_showEdit)
        self.shot_lineEdit.returnPressed.connect(self.on_shotEdit)
        self.artist_lineEdit.returnPressed.connect(self.on_artistEdit)

        self.show()
        self.slateframe = Slater(movie=self.movie, shot=self.shot, artist=self.artist)

    def closeEvent(self, event):
        """Close this widget and Slater widget."""
        self.slateframe.close()
        event.accept()
    
    
############################################################
# slots
############################################################

    def loadthumb(self):
        thumbfile = QtWidgets.QFileDialog.getOpenFileName(self,'Load Thumbnail Image File',
                                                          PROGPATH,
                                                          "Image files (*.jpg *.png *.tif)")[0]
        self.slateframe.set_thumbnail(thumbfile)
        self.status_lineEdit.setText("Loaded Thumbnail Image from File: %s" % thumbfile)

    def saveslate(self):
        this_slate = self.slateframe.grab()
        slatefile = QtWidgets.QFileDialog.getSaveFileName(self, "Save Slate to File",
                                                   PROGPATH,
                                                   "Images (*.jpg *.png *.tif)")[0]
        this_slate.save(slatefile)
        self.status_lineEdit.setText("Saved Slate Image to File: %s" % slatefile)

    def on_showEdit(self):
        """Set new movie title in Slater widget's movie_label."""
        self.movie = self.show_lineEdit.text()
        self.slateframe.movie_label.setText(self.movie)

    def on_shotEdit(self):
        """Set new shot title in Slater widget's shot_lineEdit."""
        self.shot = self.shot_lineEdit.text()
        self.slateframe.shot_lineEdit.setText(self.shot)

    def on_artistEdit(self):
        """Set new artist name in Slater widget's artist_lineEdit."""
        self.artist = self.artist_lineEdit.text()
        self.slateframe.artist_lineEdit.setText(self.artist)


############################################################
# main
############################################################

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    slaterwin = SlaterWin()
    sys.exit(app.exec_())

