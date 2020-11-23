import pandas
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers, models

DATA = f'{os.getcwd()}\\Training\\Training_Data'
CATAGORIES = ['match', 'nomatch']

def createTrainData():
    trainingData = []
    for catagory in CATAGORIES:
        path = os.path.join(DATA, catagory)
        catNum = CATAGORIES.index(catagory)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                trainingData.append([img_array, catNum])
            except Exception as e:
                raise e

    return trainingData
trainingData = createTrainData()
np.random.shuffle(trainingData)

X = []
y = []

for feature, label in trainingData:
    X.append(feature)
    y.append(label)

X = np.array(X).reshape(-1, 100, 200, 1)
y = np.array(y)

X = X/255.0

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 200, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, batch_size=32, validation_split=0.1, epochs=1)

