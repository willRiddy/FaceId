'''
Saves the images in a text file for training data
'''
import os
import cv2
import numpy as np
import neuralNetworks as nN

network = nN.Supervised(5000, 3000, 1, 1.3)
pictures = 'C:/Users/willi/OneDrive/Documents/Python/FaceRecognition/recogOpenCV/captureFrames' # path to the photos
targets = 'C:/Users/willi/OneDrive/Documents/Python/FaceRecognition/recogOpenCV/targets'

def compareNames(picture, target):
    if picture == target:
        return 1
    else:
        return 0

with open('training_data.txt', 'a') as trainingData:
    for picture, target in zip(os.listdir(pictures), os.listdir(targets)):
        img = cv2.imread('{0}{1}'.format(pictures,picture), cv2.IMREAD_GRAYSCALE) # the path of the picture
        image_array = np.true_divide(img, 255) # converting the array to decimals for input in the neural network
        picture_array = image_array.flatten().tolist() # flatten the array for learning

        img = cv2.imread('{0}{1}'.format(targets,target), cv2.IMREAD_GRAYSCALE) # the path of the picture
        image_array = np.true_divide(img, 255) # converting the array to decimals for input in the neural network
        target_array = image_array.flatten().tolist()

        isTarget = [compareNames(picture.partition('!')[0], target.partition('!')[0])]
        final_array = isTarget + picture_array + target_array
        trainingData.write('{}\n'.format(final_array))   

    