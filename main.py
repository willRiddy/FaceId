'''
Main program - Compares unidentified photos with know photos
'''
import os
import cv2
import numpy as np
import face_recognition
import mysql.connector
# import tensorflow as tf
import time

class DB():

    def __init__(self, host='localhost', user='will', password='toor', database='faceRegistration'):
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def query(self, data, table, condition=None):
        if condition is not None:
            sql = f"SELECT {data} FROM {table} WHERE {condition}"
        else:
            sql = f"SELECT {data} FROM {table}"

        return sql

class CheckUnkown():

    def __init__(self):

        self.db = DB()
    # Path to captures from face recognition program
        self.pathUnkown = f'captureFrames'
        self.pathKnown = f'knownFaces'
        #self.model_path = f'Training/TensorFlow/recognitionCNN.model'
        #self.model = tf.keras.models.load_model(self.model_path)
        self.name = None
        self.currentPhotoPath = None

        self.limit = 0.5 # constant
        self.highestPrev = 1

        # all known faces
        self.known = []
        self.knownID = []
        self.knownNames = []

    def encodeKnown(self):
        sql = self.db.query('pupilID, name, photo', 'pupils')
        self.db.cursor.execute(sql)
        results = self.db.cursor.fetchall()
        for ID, name, photo in results:
            img = face_recognition.load_image_file(photo)
            encoding = face_recognition.face_encodings(img)[0]
            self.known.append(encoding)
            self.knownID.append(ID)
            self.knownNames.append(name)

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

    def update(self, ID):
        sql = f"UPDATE pupils SET time = now(), cameraID = 2 WHERE pupilID={ID}"
        self.db.cursor.execute(sql)
        self.db.db.commit()

    def loopThroughUnknowns(self):
        for photo in os.listdir(self.pathUnkown):
            photoPath = os.path.join(self.pathUnkown, photo)
            if photoPath is None: # bug where there is an image file but no image in it
                break
            prediction = self.useFR(photoPath)
            self.ID = prediction
            if self.ID is not None:
                print('Update', self.ID)
                self.update(self.ID)
            os.remove(photoPath)
        time.sleep(0.1) # Going through images too fast, had to slow down.

    def useFR(self, unknown):
        unknown_image = face_recognition.load_image_file(unknown)
        try:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            return None

        results = face_recognition.face_distance(self.known, unknown_encoding)
        result = self.knownID[np.argmin(results)]

        return result

    def main(self):
        self.encodeKnown()
        while True:
            self.loopThroughUnknowns()

CheckUnkown().main()
