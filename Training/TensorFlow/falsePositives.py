import tensorflow as tf
import cv2
import os

class testModel():

    def __init__(self, folder, match, limit=0.25):
        
        self.path = f'C:/Users/willi/OneDrive/Desktop/FaceId/Training/Testing_Data/{folder}'
        self.model = tf.keras.models.load_model('recognitionCNN.model')
        self.match = match
        self.limit = limit

    def imgArray(self, picture):
        img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
        return img.reshape(-1, 100, 200, 1)

    def main(self):
        for name in os.listdir(self.path):
            testPic = os.path.join(self.path, name)
            
            prediction = self.model.predict([self.imgArray(testPic)])
            if self.match:
                self.correct(prediction, name)
            else:
                self.incorrect(prediction, name)

    def correct(self, prediction, name):
        if prediction[0] <= self.limit:
            print(f'{name}, is a match {prediction[0]}')
    
    def incorrect(self, prediction, name):
        if prediction[0] > self.limit:
            print(f'{name}, is not a match {prediction[0]}')

testModel('match', match=True).main()





