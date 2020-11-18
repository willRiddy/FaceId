import os
import numpy as np
import cv2
import sys
sys.path.insert(1, os.getcwd())
import neuralNetworks_2

network = neuralNetworks_2.Supervised([5000, 2500, 1000, 1000, 2], 0.3)
path = f'{os.getcwd()}/Training/Training_Faces/'

def compareNames(picture, target):
    if picture == target:
        return [1, 0]
    else:
        return [0, 1]

def makeLearning(picture):
    image_array = np.true_divide(picture, 255) # converting the array to decimals for input in the neural network
    binary_picture = image_array.flatten().tolist() # flatten the array for learning
    return binary_picture

def training(picture_list):
    training_list = np.asfarray(picture_list[0: 1])
    input_list = np.asfarray(picture_list[2:])
    network.train(input_list, training_list)

def test():
    # obtain data for testing the network accuracy
    outputs = []
    for i in range(10):
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
            output = network.query(picture)
            if output[0] > output[1]:
                outputs.append(1)
            else:
                outputs.append(0)

    percentCorrect = (sum(outputs)/len(outputs)) * 100
    print(percentCorrect)
        
# Get photos from right person
for celeb in os.listdir(path):
    print(celeb)
    image_names = []
    isTargets = []
    images = []
    input_array = []

    for i, image in enumerate(os.listdir(f'{path}{celeb}')):
        img = cv2.imread(f'{path}{celeb}/{image}', cv2.IMREAD_GRAYSCALE) # the path of the picture
        binary_picture = makeLearning(img)
        if i != 1:
            image_names.append(image)
            images.append(binary_picture)
        else:
            target_image = binary_picture

    # make random selections for photos up to 90 of wrong people
    for i in range(20):
        current_folder_name = np.random.choice(os.listdir(f'{path}'))
        if current_folder_name != celeb:
            # Get image from folder and convert into binary
            image = np.random.choice(os.listdir(f'{path}{current_folder_name}'))
            image_names.append(image)
            img = cv2.imread(f'{path}{current_folder_name}/{image}', cv2.IMREAD_GRAYSCALE) # the path of the picture
            image_array = np.true_divide(img, 255) # converting the array to decimals for input in the neural network
            binary_picture = image_array.flatten().tolist() # flatten the array for learning
            images.append(binary_picture)
    
    # check if celebs name = file name
    for name in image_names:
        isTargets.append(compareNames(name.partition('!')[0], celeb))

    # make array for neural network training
    for image, isTarget in zip(images, isTargets):
        final_array = isTarget + image + target_image
        input_array.append(final_array)

    #print(input_array)
    # Training neural network
    for i, array in enumerate(input_array):
        training(array)
    
test()

np.save(f'weights/weights.npy', network.weights)
np.save(f'weights/bias.npy', network.bias)