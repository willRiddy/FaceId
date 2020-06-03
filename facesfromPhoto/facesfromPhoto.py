import cv2
import numpy as np

path = 'C:/Users/willi/Documents/A-Levels/Computing/Coursework/FaceRecognition/recogOpenCV/facesfromPhoto/faces/'

face_cascade = cv2.CascadeClassifier('C:/Users/willi/Documents/A-Levels/Computing/Coursework/FaceRecognition/recogOpenCV/haarcascade_frontalface_default.xml')

img_file = 'groupPhoto.jpg'
img = cv2.imread(img_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 4)
for i, face in enumerate(faces):
    print(i, face)
    x = face[0]
    y = face[1]
    h = face[3]
    crop_img = img[y:y+h, x:x+h]
    cv2.imwrite('{0}frame{1}.jpg'.format(path, i), crop_img)

cv2.imshow('img', img)
cv2.waitKey(0)