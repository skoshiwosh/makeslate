#!/bin/sh

#  slater.sh
#
#  Platform is Mac OS X Yosemite
#
#  Created by Suzanne Berger on 2/07/19.
#
#  Launch slater.py and possibly set environment variables as inputs
#  Note: mayapy is used because PySide2 already installed for mayapy
#
MAYAPY=/Applications/Autodesk/maya2017/Maya.app/Contents/bin/mayapy
SLATERPY=/Users/suzanneberger/Documents/dev/slater/slater.py
#
# If any of these environemnt variables are set, then corresponding
# input fields in slater.py will be initialized to set values
#
#export SHOW="Facing The Beast"
#export SHOT="abc01"
#export ARTIST="picasso"

$MAYAPY $SLATERPY $*
