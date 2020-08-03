

import cv2
import pandas as pd
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
#loading haarcascade
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

namex=pd.read_csv('Names.csv', index_col=0, squeeze=True)
x=namex.tail(1)
print (x)

face_id = input('\n enter user id end press <return> ==>  ')
face_name=input('\n enter the name of person and press enter ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

count = 0

import csv
with open(r'Names.csv', 'a') as f:
    writer = csv.writer(f, delimiter =',')
    writer.writerow([face_id, face_name])

while(True):

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff 
    if k == 27:
        break
    elif count >= 30: 
         break

# Releasing cam 
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

