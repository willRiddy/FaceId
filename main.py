'''
Main program - Compares unidentified photos with know photos
'''
import os
import cv2
import numpy as np
import tensorflow as tf
import time

class CheckUnkown():

    def __init__(self):
    # Path to captures from face recognition program
        self.pathUnkown = f'{os.getcwd()}/captureFrames'
        self.pathKnown = f'{os.getcwd()}/knownFaces'
        self.model_path = f'{os.getcwd()}/Training/TensorFlow/recognitionCNN.model'
        self.model = tf.keras.models.load_model(self.model_path)
        self.name = None
        self.currentPhotoPath = None

        self.limit = 0.5 # constant
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
        if prediction <= self.limit:
            if prediction < self.highestPrev:
                self.highestPrev = prediction
                self.name = os.path.split(self.currentPhotoPath).partition('.')[0]

    def loopThroughUnknowns(self):
        for photo in os.listdir(self.pathUnkown):
            photoPath = os.path.join(self.pathUnkown, photo)
            img = self.read(photoPath)
            if img is None: # bug where there is an image file but no image in it
                break
            self.loopThroughKnowns(img)
            os.remove(photoPath)


    # loop though all known faces
    def loopThroughKnowns(self, unimg):
        for i, face in enumerate(os.listdir(self.pathKnown)): # Don't have any known faces yet
            facePath = os.path.join(self.pathKnown, face)
            knimg = self.read(facePath)
            connected = self.conPhotos(knimg, unimg)
            prediction = self.query(connected)
            print(i, prediction)
            self.check_match(prediction)

        if self.name is not None:
            # Update times
            currentTime = time.time()
            print(self.name)
            self.name = None

    def main(self):
        while True:
            self.loopThroughUnknowns()

CheckUnkown().main()
