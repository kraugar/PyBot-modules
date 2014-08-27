Very simple bot modules, written in python.

Stealers
========
#### Simple info stealers. Includes:
###### -  Pidgin accounts(plain text)
###### -  Pidgin logs
###### -  Skype username and hash
###### -  Skype messages
###### -  Mozilla hashed credentials
###### -  Filezilla server credentials(plain text)
###### -  Chrome browsing history
###### -  Chrome passwords

sysinfo
=======

#### Simple info gathering. Includes:
###### - Basic info (Ip address, Windows version, Current User)
###### - Running Processes (pid and name)
###### - Drive detection (Selects interesting drives: Removable, Local and Network)
###### - Simple port scanning 
###### - Simple directory lister (recursive)
###### - Execute javascript in windows

Screenshot pidgin
=================

###### Take screenshot of pidgin if it is on the foreground.

Microphone record
=================

#### PoC record from microphone. Very early!

###### Needs to be run from commandline, because of the use of multiprocessing.

#### dependencies:
###### - Pyaudio

####TODO:
###### - List all microphones.
###### - Error catching.

Webcam view
=================

#### PoC view webcam feed. Very early!

###### - client & server: A very(!) simple reverse webcam connection. The client takes shots and sends them to the server, the server starts a webserver and shows the shots in a browser that refreshes.
###### - Viewer: Simple video feed, takes snapshots and shows them in a GUI.

#### Dependencies:
###### - opencv2
###### - numpy
###### - flask
###### - requests

####TODO:
###### - List all webcams
###### - Error catching