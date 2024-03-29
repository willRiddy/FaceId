import os
import json

path = os.getcwd() # Path to directory
path = f'Training_Faces/'

# Getting celebs name from file
celebs = open('celebs2.txt', 'r')
celebs_lines = celebs.readlines()
# Making folder for each celeb
for celeb in celebs_lines:
    celeb = celeb.replace('\n', '')
    celeb = celeb.replace(' ', '_')# Replacing all spaces with underscores
    try:
        os.makedirs(f'{path}{celeb}')# Makes folder in current directory with celebs name
    except OSError:
        print(f'Error Making directory to {path}')
    else:
        print (f'Directory made in: {path}')


