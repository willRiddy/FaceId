import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
Not completely my code
'''

path = 'captureFrames/'

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml') #haarcascade to recognise faces

class faceRecognition():

    def __init__(self, face_cascade):
        self.cap = cv2.VideoCapture(0) # captures from default camera
        self.face_cascade = face_cascade
        self.dim = (100, 100)

    def draw_rect(self, obj): # drawing a rectangle around each face
        for (x, y, w, h) in obj:
            cv2.rectangle(self.img, (x,y), (x+w, y+h), (255, 0, 0), 2)
            self.roi_gray = self.gray[y:y+h, x:x+w]
            self.roi_colour = self.img[y:y+h, x:x+w]
        return len(obj)

    def save_face(self, face, i, j, pThrough):
        x = face[0] # getting coords from image
        y = face[1]
        h = face[3]
        crop_img = self.img[y:y+h, x:x+h] # cropping the image in those coords
        cv2.imwrite('{0}{1}frame{2}{3}.jpg'.format(path, pThrough, i, j), crop_img) # writes to a folder so I can run another program at the same time which checks this folder for faces

    def main(self):
        i = 0
        pThrough = 0
        while True:
            if i > 100000:
                i = 0
                pThrough += 1
            if i % 2 == 0: # Skips out every other frame
                ret, self.img = self.cap.read()
                self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 4) # captures all the faces in that frame.
                if self.draw_rect(faces) > 0: # returns then len of the array, so how many faces their are
                    for j, face in enumerate(faces):
                        self.save_face(face, i, j, pThrough)

            cv2.imshow('webcam',self.img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            i += 1

        self.cap.release()
        cv2.destroyAllWindows()

faceRecognition(face_cascade).main()