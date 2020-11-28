import urllib.request
from bs4 import BeautifulSoup
import re
import os
import cv2
import shutil
import matplotlib.pyplot as plt
import requests

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
dim = (100, 100) # Dimensions for face

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def resizeImage(img):
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA) # make all the faces the same size
    resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) # Turning image gray
    return resized_gray

opener = AppURLopener()

celebs = open('Training/celebs2.txt', 'r')
celebs_lines = celebs.readlines()
total = len(celebs_lines)
origTotal = total

safe = True
numLeft = total
total = numLeft

for celeb in celebs_lines[(origTotal - numLeft):]:
    print(total, '/', origTotal)
    celeb = celeb.replace('\n', '')
    query = celeb.replace(' ', '+')# + signs needed for query in google
    query = celeb.replace('"', '')
    try:
        html = opener.open(f'https://www.google.com/search?q={query}+actor+portrait&safe=strict&sxsrf=ALeKk02RtmPshF5zmoEUYqnx1pH2NjJ_gg:1606508885399&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjU8sT7x6PtAhXUX8AKHQUIDGoQ_AUoAnoECCsQBA&biw=1920&bih=1')
    except UnicodeError:
        safe = False
        query = query.replace('+', '_')
        print(f'Deleted {query} Unicode Error')
        try:
            shutil.rmtree(f'Training/Training_Faces/{query}/')
            pass
        except FileNotFoundError:
            pass
    
    if safe:
        bs = BeautifulSoup(html, 'html.parser')
        images = bs.find_all('img', {'src':re.compile('.jpg')})
        print(images)
        query = query.replace('+', '_')
        limit = 10
        for i, image in enumerate(images):
            if i < limit and i <= 15:
                try:
                    urllib.request.urlretrieve(image['src'], f'Training/Training_Faces/{query}/{query}!{i}.jpg')
                    img_file = f'Training/Training_Faces/{query}/{query}!{i}.jpg'
                    img = cv2.imread(img_file)
                    print(img)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                except FileNotFoundError:
                    break
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
            elif i > 15:
                print(f'Deleted {query} too many unkown faces')
                shutil.rmtree(f'Training/Training_Faces/{query}/')
                break
                
            else:
                break
    safe = True
    total -= 1