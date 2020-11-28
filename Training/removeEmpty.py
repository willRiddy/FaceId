import os

root = 'Training_Faces'
folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        print('Remove', folder)
        os.rmdir(folder[0])