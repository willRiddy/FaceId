'''
Program to compare the images and enter them into the neural network
'''
import os
import cv2
import numpy as np
import neuralnetworks as nN

network = nN.Supervised(5000, 3000, 1, 1.3)

targets = 'C:/Users/willi/Documents/A-Levels/Computing/Coursework/FaceRecognition/recogOpenCV/targets/'
pictures = 'C:/Users/willi/Documents/A-Levels/Computing/Coursework/FaceRecognition/recogOpenCV/captureFrames/' # path to the photos

while True:
    for picture in pictures:
        img = cv2.imread('{0}{1}'.format(pictures,picture), cv2.IMREAD_GRAYSCALE) # the path of the picture
        image_array = np.true_divide(img, 255) # converting the array to decimals for input in the neural network
        picture_array = image_array.flatten() # flatten the array for learning
        most_likely = [0, 'name']
        for target in targets:
            img = cv2.imread('{0}{1}'.format(targets,target), cv2.IMREAD_GRAYSCALE)
            image_array = np.true_divide(img, 255)
            target_array = image_array.flatten()
            final_array = [picture_array, target_array]
            final_array = final_array.flatten()
            prob_matching = network.query(final_array)
            if prob_matching > most_likely[0]:
                most_likely = [prob_matching, target]

        print('The face identy is most likely: {}'.format(most_likely[1]))


