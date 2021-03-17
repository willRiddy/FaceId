import subprocess

subprocess.run('python app.py & python faceRecognition.py & python main.py', shell=True)