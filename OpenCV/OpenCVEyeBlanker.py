#Cascade file source: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#Uses cv2
#Finds and blanks out human eyes

import cv2
import os

image_path = ''
cascade_file = 'haarcascade_eye.xml'
cascade = cv2.CascadeClassifier(cascade_file)

try:
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(grey_image, minSize=(20,20))
    if (len(eyes) == 0):
        print("No eyes found.")
    else:
        for (x, y, w, h) in eyes:
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), -1)
            cv2.imshow('image', image)

except Exception as e:
    print(e)
  
