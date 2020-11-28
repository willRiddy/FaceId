import pandas
import os
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import TensorBoard

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
      for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)


path = 'C:/Users/willi/OneDrive/Desktop/FaceId/Training'

DATA = f'{path}/Training_Data/'
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

dense_layers = [1]
layer_sizes = [256]
conv_layers = [3]

for denseLayer in dense_layers:
    for layerSize in layer_sizes:
        for convLayer in conv_layers:
            NAME = f'{convLayer}-conv-{layerSize}-nodes-{denseLayer}-dense-{time.time()}'
            tensorboard = TensorBoard(log_dir=f'logs/{NAME}')

            model = models.Sequential()
            model.add(layers.Conv2D(layerSize, (3, 3), activation='relu', input_shape=(100, 200, 1)))
            model.add(layers.MaxPooling2D((2, 2)))

            for l in range(convLayer - 1):
                model.add(layers.Conv2D(layerSize, (3, 3), activation='relu'))
                model.add(layers.MaxPooling2D((2, 2)))

            model.add(layers.Flatten())
            for i in range(denseLayer):
                model.add(layers.Dense(layerSize, activation='relu'))

            model.add(layers.Dense(1, activation='sigmoid'))

            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            model.fit(X, y, batch_size=32, validation_split=0.1, epochs=10, callbacks=[tensorboard])


model.save('recognitionCNN.model')