# makeslate
Generate a slate image file for visual effects dailies. Consider this project to be an initial prototype.
Software was developed on a Mac but is basically platform independent.

Files:

slater.py
- python script that generates slate image file
- uses Python 2.7 and PySide2, python wrapper around Qt5
- consists of 2 QtWidget classes, Slater and SlaterWin 
- user inputs data and thumbnail either directly within Slater or from SlaterWin or using environment settings 
- Slater widget is converted to QPixMap using grab method and saved to designated image file

slater.sh
- bash script to launch slater.py
- Autodesk’s Maya’s mayapy is used for convenience because PySide2 is already installed
- contains commented out environment variables: SHOW, SHOT and ARTIST
- if uncommented, these will initialize corresponding slate entries within slater.py classes

bgslate.png
- background image used by slater (that I modified from Billy Brook's original post)
- if you use this for production then replace studio logo with yours

slate_thumbnail.jpg
- this is a stand-in thumbnail image I used for development 
- I cropped this from image attached to Billy's post 

running_slater.pdf
- instructions on how to run slater.py

slaterUI_init.png
- screen shot of Slater and SlaterWin as displayed when slater.py is initially launched

slaterUI_final.png
- screen shot once slate data has been entered and saved to designated image file

testslate_10.jpg
- sample output slate that corresponds to above slaterUI_final.png
- TBD: resolve color noise issue in saved image

Disclaimers:

Inconsistencies and redundancies in code was partly intentional for demonstration and iterative development process.
Currently image resolutions and aspect ratios are hard-coded but software should accommodate show specifications.
Qt Designer that outputs *.ui files could have been used instead of manually coding widgets and layouts.

How it works:

The entire Slater widget is converted to a Pixmap using QWidget grab method and then saved to designated slate image file. Currently this runs standalone but might be incorporated as a plugin into CG apps that use Python2.7 with PySide2.
 
User enters slate data both from SlateWin and Slater widgets. I did this intentionally although future versions should either have all data input into Slater widget directly or entered externally from a separate object which accesses Slater widget object. If the latter, then Slater can be created entirely using QPainter and saved as QImage. Slate generator could then run either as batch process or GUI. Studio environment configuration that is used for other applications should definitely be incorporated to further automate and/or enforce filesystem standards and naming conventions. 

User can press "Update Slate" button in SlaterWin to send all entries from SlaterWin to Slater. Alternatively, user can send individual entries to Slater widget by pressing "Return" key on any field entered from SalterWin. Entries made within main Slater do not require user to press "Return" (because no signal needs to be emitted). The "Movie Title" needs to be set from either the Show field within SlaterWin or using SHOW environment variable that is presumably set externally. User sets Thumbnail image in Slater widget using "Load Thumbnail" button from SlateWin. Other fields in Slater can be entered directly. Shot and Artist fields might also be initialized with respective environment variables.

