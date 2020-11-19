import os
import numpy as np
import cv2
import sys
sys.path.insert(1, os.getcwd())
import neuralNetworks_2

weights = np.load(f'{os.getcwd()}/weights/weights.npy', allow_pickle=True)
bias = np.load(f'{os.getcwd()}/weights/bias.npy', allow_pickle=True)
path = f'{os.getcwd()}/Training/Training_Faces/'
network = neuralNetworks_2.Supervised([5000, 2500, 1000, 1000, 2], 0.3, weights, bias)

def compareNames(picture, target):
    if picture == target:
        return 1
    else:
        return 0

def makeLearning(picture):
    image_array = np.true_divide(picture, 255) # converting the array to decimals for input in the neural network
    binary_picture = image_array.flatten().tolist() # flatten the array for learning
    return binary_picture

def training(picture_list):
    training_list = np.asfarray(picture_list[0])
    input_list = np.asfarray(picture_list[1:])
    network.train(input_list, training_list)

def test():
    # obtain data for testing the network accuracy
    outputs = []
    for i in range(100):
        photo_list = []
        final_list = []
        # Get Target Face
        target = np.random.choice(os.listdir(f'{path}'))
        target_face = np.random.choice(os.listdir(f'{path}{target}')) # Celebs Face
        target_img = cv2.imread(f'{path}{target}/{target_face}', cv2.IMREAD_GRAYSCALE)
        target_img = (makeLearning(target_img))

        for i in range(10):
            # Gets 1 face from celeb's folder
            if i == 0:
                random_face = np.random.choice(os.listdir(f'{path}{target}'))
                face = cv2.imread(f'{path}{target}/{random_face}', cv2.IMREAD_GRAYSCALE)
                photo_list.append(makeLearning(face))
            # Gets 9 other random faces
            else:
                random_person = np.random.choice(os.listdir(f'{path}'))
                random_face = np.random.choice(os.listdir(f'{path}{random_person}'))
                face = cv2.imread(f'{path}{random_person}/{random_face}', cv2.IMREAD_GRAYSCALE)
                photo_list.append(makeLearning(face))

        # collects photos in binary form for learning
        for image in photo_list:
            final_array = image + target_img
            final_list.append(final_array)

        # gets the outputs
        for picture in final_list:
            highest_output = 0
            output = network.query(picture)
            if output[0] > output[1] and output[0] > highest_output:
                highest_output = output[0]
                outputs.append(1)
            else:
                outputs.append(0)
        print('################')

    percentCorrect = (sum(outputs)/len(outputs)) * 100
    print(percentCorrect)

test()