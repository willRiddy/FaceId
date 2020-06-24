import os

path = 'C:/Users/willi/OneDrive/Desktop/FaceId/resizeImage/'

for i, file_ in enumerate(os.listdir(path)):
    os.rename(f'{path}{file_}', f'{path}willRiddy!{i}.jpg')