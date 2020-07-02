import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request

#cap = cv2.VideoCapture(0)

url='http://192.168.1.3:8080/shot.jpg'

font = cv2.FONT_HERSHEY_PLAIN

while True:
    #_, frame = cap.read()
    
    imgResp =  urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)

    decodedObjects = pyzbar.decode(img)
    for obj in decodedObjects:
        print("Data", obj.data)
        cv2.putText(img, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)

    cv2.imshow("Frame", img)

    key = cv2.waitKey(1)
    if key == 27:
        break