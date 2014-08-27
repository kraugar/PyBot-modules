import numpy as np
import cv2 as opencv2
import base64
import requests

cam = opencv2.VideoCapture(0)

while True:
    shot = cam.read()[1]

    cv2mat=opencv2.imencode(".jpeg",shot,(1,75))[1]
    JpegData=cv2mat.tostring()
    JpegData64 = base64.urlsafe_b64encode(JpegData)
    requests.get("http://192.168.178.36:5000/put?image=" + JpegData64)
    if opencv2.waitKey(50) == 27:
    	break
    
cam.release()
opencv2.destroyAllWindows()
