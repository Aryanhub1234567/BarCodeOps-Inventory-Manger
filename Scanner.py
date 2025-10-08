import cv2
import numpy as np
from pyzbar.pyzbar import decode

#cap = cv2.VideoCapture(1)
#cap.set(3,640)
#cap.set(4,480)
def scan_barcode() :
    cap = cv2.VideoCapture(1)
    myData = None

    while True:
        success, img = cap.read()
        if not success:
            break
        
        for barcode in decode(img) :
            #print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print (myData)
            pts = np. array([barcode. polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img, [pts], True, (255,0,0),2)
            pts2=barcode.rect
            cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
            #return myData
        
        img = cv2.resize(img, (540,480)) 
        cv2.imshow('Result',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return myData
