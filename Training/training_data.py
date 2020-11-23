'''
Turns the images into training data
'''
import os
import numpy as np
import cv2
import sys

class Dataset():

    def __init__(self, fileLoc):
        self.path_in = f'{os.getcwd()}/Training/Training_Faces/'
        self.path_out = f'{os.getcwd()}/Training/{fileLoc}/'
        self.celebList = os.listdir(self.path_in)

    def connect(self, img1, img2):
        connect = np.concatenate((img1, img2), axis=1)
        return connect

    def makePic(self, celeb):
        images_target = []
        images_notTarget = []
        input_array = []

        for i, image in enumerate(os.listdir(f'{self.path_in}{celeb}')):
            img = cv2.imread(f'{self.path_in}{celeb}/{image}') # the path of the picture
            if i != 1:
                images_target.append(img)
            else:
                target_image = img

        # make random selections for photos up to 90 of wrong people
        for i in range(10):
            folder = np.random.choice(os.listdir(f'{self.path_in}'))
            if folder != celeb:
                # Get image from folder and convert into binary
                image = np.random.choice(os.listdir(f'{self.path_in}{folder}'))
                img = cv2.imread(f'{self.path_in}{folder}/{image}') # the path of the picture
                images_notTarget.append(img)
        
        # check if celebs name = file name
        for i, image in enumerate(images_target):
            try:
                img = self.connect(target_image, image)
                cv2.imwrite(f'{self.path_out}match/{celeb}_match_{i}.jpg', img)
            except UnboundLocalError:
                pass

        for i, image in enumerate(images_notTarget):
            try:
                img = self.connect(target_image, image)
                cv2.imwrite(f'{self.path_out}nomatch/{celeb}_nomatch_{i}.jpg', img)
            except UnboundLocalError:
                pass


    def main(self, numTimes=None):
        for i, celeb in enumerate(self.celebList):
            if not numTimes:  
                self.makePic(celeb)
            else:
                if i <= numTimes:
                    self.makePic(celeb)
                else:
                    break
                
Dataset('Training_Data').main()
