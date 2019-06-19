#Cascade file source: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_alt.xml
#Uses cv2
#Creates a list of images which contain human faces

import cv2
import os

image_dir = './photos'
cascade_file = 'haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_file)

files_with_faces = []

for file in os.listdir(image_dir):
    if file.endswith(".jpg"):
        try:
            joined_path = os.path.join(image_dir, file)
            image = cv2.imread(joined_path)
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(grey_image, minSize=(20,20))
            if (len(faces) > 0):
                files_with_faces.append(joined_path)
        except Exception as e:
            print(e)
    else:
        continue
