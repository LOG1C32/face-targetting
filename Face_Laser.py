#Face tracker using OpenCV and Arduino

import cv2
import math
import serial,time
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
ArduinoSerial=serial.Serial('com5',9600,timeout=0.1)
time.sleep(5)

while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #mirror the image
    #print(frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face
    for x,y,w,h in faces:
        #sending coordinates to Arduino
        xx = math.floor((x+w//2)/(640/180))
        yy = math.floor((y+h//2)/(480/180))
        string='X{0:d}Y{1:d}'.format(xx,yy)
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))
        #plot the center of the face
        cv2.circle(frame,(x+w//2,y+h//2),2,(0,0,255),2)
        #plot the roi
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    #plot the squared region in the center of the screen
    #out.write(frame)
    cv2.imshow('img',frame)
    #cv2.imwrite('output_img.jpg',frame)
    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()