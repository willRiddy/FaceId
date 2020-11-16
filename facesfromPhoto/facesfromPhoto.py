'''
This code looks at a phot and saves all the photos in it in a folder
'''

import cv2
import numpy as np

path = 'faces/'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

img_file = 'facesfromPhoto/groupPhoto.jpg'
img = cv2.imread(img_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 4)
print(face_cascade)
for i, face in enumerate(faces):
    print(i, face)
    x = face[0]
    y = face[1]
    h = face[3]
    crop_img = img[y:y+h, x:x+h]
    cv2.imwrite('{0}frame{1}.jpg'.format(path, i), crop_img)

cv2.imshow('img', img)
cv2.waitKey(0)