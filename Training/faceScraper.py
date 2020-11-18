import urllib.request
from bs4 import BeautifulSoup
import re
import os
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
dim = (50, 50) # Dimensions for face

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def resizeImage(img):
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA) # make all the faces the same size
    resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) # Turning image gray
    return resized_gray

opener = AppURLopener()

celebs = open('Training/celebs.txt', 'r')
celebs_lines = celebs.readlines()

for celeb in celebs_lines:
    celeb = celeb.replace('\n', '')
    query = celeb.replace(' ', '+')# + signs needed for query in google
    html = opener.open(f'https://www.google.com/search?q={query}+portrait&safe=active&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjAjr-A2ovtAhWhoFwKHUpqBuIQ_AUoAXoECAQQAw&biw=1280&bih=619&surl=1')

    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    query = query.replace('+', '_')
    limit = 10
    for i, image in enumerate(images):
        if i < limit: 
            print(f'{celeb} {i}')
            urllib.request.urlretrieve(image['src'], f'Training/Training_Faces/{query}/{query}!{i}.jpg')
            img_file = f'Training/Training_Faces/{query}/{query}!{i}.jpg'
            img = cv2.imread(img_file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            try:
                x = faces[0][0]
                y = faces[0][1]
                h = faces[0][3]
                crop_img = img[y:y+h, x:x+h]
                resized_img = resizeImage(crop_img)
                cv2.imwrite(f'Training/Training_Faces/{query}/{query}!{i}.jpg', resized_img)
            except  IndexError:
                limit += 1
                os.remove(f'Training/Training_Faces/{query}/{query}!{i}.jpg')
            
        else:
            break