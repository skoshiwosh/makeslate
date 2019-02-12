# makeslate
Generate a slate image file for visual effects dailies. Consider this project to be an initial prototype.
Software was developed on a Mac but is basically platform independent.

Files:

slater.py
- python script that generates slate image file
- uses Python 2.7 and PySide2, python wrapper around Qt5
- consists of 2 QtWidget classes, Slater and SlaterWin 
- user inputs slate data and thumbnail either directly within Slater widget or from SlaterWin or using environment settings 
- Slater widget is converted to QPixMap using grab method and saved to designated image file

slater.sh
- bash script to launch slater.py
- Autodesk’s Maya’s mayapy is used for convenience because PySide2 is already installed
- contains commented out environment variables: SHOW, SHOT and ARTIST
- if uncommented, these will initialize corresponding slate entries within slater.py classes

slaterUI_init.png
- screen shot of Slater and SlaterWin as displayed when slater.py is initially launched

slaterUI_final.png
- screen shot once slate data has been entered and saved to designated image file

testslate_09.jpg
- sample output slate that corresponds to above slaterUI_final.png
- TBD: resolve color noise issue in saved image
