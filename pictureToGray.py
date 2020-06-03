import cv2
import os

path = 'targets/'
# path to the test photos
dim = (50, 50)

def resizeImage(img):
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA) # make all the faces the same size
    resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) # changes the faces to black and white
    return resized_gray # returns the image

for i, picture in enumerate(os.listdir(path)):
    img = cv2.imread('{0}{1}'.format(path,picture))
    resized_img = resizeImage(img)
    cv2.imwrite('{}{}'.format(path, picture), resized_img)