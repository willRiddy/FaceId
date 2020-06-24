'''
Saves the images in a text file for training data
'''
import os
import cv2
import numpy as np
import neuralNetworks_2 as nN

network_structure = [5000, 3000, 500, 1]
lr = 0.3

network = nN.Supervised(network_structure, 1)
pictures = 'captureFrames' # path to the photos
targets = 'targets'
weights = 'weights/'

class Train:

    def __init__(self, data):
        self.data = data
        self.network_data = None

    def convert(self, farray): # converts the data into 'network' data
        return np.asfarray(farray[1:])

    def getTarget(self, target):
        return np.asfarray(target[0])

    def train(self):
        for data in self.data:
            target = self.getTarget(data)
            inputs = self.convert(data)
            network.train(inputs, target)

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

#np.save(f'{weights}weights.npy', network.weights)