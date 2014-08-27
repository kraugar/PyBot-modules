import numpy as np
import cv2 as opencv2

cam = opencv2.VideoCapture(0)

opencv2.imwrite('snapshot.jpg', cam.read()[1])

while True:
    shot = cam.read()[1]

    opencv2.imshow('Webcam',shot)
     
    if opencv2.waitKey(1) == 27:
    	break

cam.release()
opencv2.destroyAllWindows()
