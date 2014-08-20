from PIL import *
import time
import win32gui
import win32process, win32pdhutil
from screenshot import *

try:
    pidginpid = win32pdhutil.GetPerformanceAttributes('Process','ID Process',"Pidgin")
except: # Meed to find the appropriate error 
    print "[!]Error! Pidgin is not running."
    exit()

while True:
    foregroundhwnd = win32gui.GetForegroundWindow()
    foregroundpid =  win32process.GetWindowThreadProcessId(foregroundhwnd)[1]
    
    if foregroundpid == pidginpid:
        coordinates = win32gui.GetWindowRect(foregroundhwnd)
        hCaptureBitmap = get_screen_buffer(bounds = coordinates)
        pimage = make_image_from_buffer(hCaptureBitmap).save("pidgin.png","PNG")
        print "[+]Found pidgin!"

    time.sleep(1)


