'''
Main program - Compares unidentified photos with know photos
'''
import os
import cv2
import numpy as np
import face_recognition
import matplotlib.pyplot as plt
# import tensorflow as tf
import time

class CheckUnkown():

    def __init__(self):
    # Path to captures from face recognition program
        self.pathUnkown = f'captureFrames'
        self.pathKnown = f'knownFaces'
        #self.model_path = f'Training/TensorFlow/recognitionCNN.model'
        #self.model = tf.keras.models.load_model(self.model_path)
        self.name = None
        self.currentPhotoPath = None

        self.limit = 0.4 # constant
        self.highestPrev = 1

    # Makes two photos into single concatenated photo
    def conPhotos(self, img1, img2):
        connected = np.concatenate((img1, img2), axis=1)
        return connected.reshape(-1, 100, 200, 1)

    # query model to check if face is match
    def query(self, faces):
        prediction = self.model.predict([faces])
        return prediction[0]

    # reading photo
    def read(self, img):
        img_array = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        return img_array

    # check for match
    def check_match(self, prediction):
        if prediction is not None:
            if prediction[0] <= self.limit:
                if prediction[0] < self.highestPrev:
                    self.highestPrev = prediction[0]
                    _, tail = os.path.split(self.currentPhotoPath)
                    self.name = tail.partition('.')[0]

    def loopThroughUnknowns(self):
        for photo in os.listdir(self.pathUnkown):
            photoPath = os.path.join(self.pathUnkown, photo)
            #img = self.read(photoPath)
            if photoPath is None: # bug where there is an image file but no image in it
                break
            self.loopThroughKnowns(photoPath)
            os.remove(photoPath)

    def useFR(self, known, unknown):
        known_image = face_recognition.load_image_file(known)
        unknown_image = face_recognition.load_image_file(unknown)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        try:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            return None

        results = face_recognition.face_distance([known_encoding], unknown_encoding)
        return results


    # loop though all known faces
    def loopThroughKnowns(self, unimg):
        for i, face in enumerate(os.listdir(self.pathKnown)): # Don't have any known faces yet
            facePath = os.path.join(self.pathKnown, face)
            self.currentPhotoPath = facePath
            #knimg = self.read(facePath)
            knimg = facePath
            #connected = self.conPhotos(knimg, unimg)
            #prediction = self.query(connected)
            prediction = self.useFR(knimg, unimg)
            #print(prediction)
            #print(i, prediction)
            self.check_match(prediction)

        if self.name is not None:
            self.highestPrev = 1
            # Update times
            currentTime = time.time()
            print(self.name, currentTime)
            self.name = None

    def main(self):
        while True:
            self.loopThroughUnknowns()

CheckUnkown().main()
