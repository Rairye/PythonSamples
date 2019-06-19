#Cascade file source: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_alt.xml
#Casecade file source: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_fullbody.xml
#Casecade file source: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_lowerbody.xml
#Uses cv2
#Creates list of the following three types of profile pictures: face pictures, full body pictures, faceless pictures


import cv2
import os

image_dir = './photos'

cascade_file1 = 'haarcascade_frontalface_alt.xml'
cascade1 = cv2.CascadeClassifier(cascade_file1)

cascade_file2 = 'haarcascade_fullbody.xml'
cascade2 = cv2.CascadeClassifier(cascade_file2)

cascade_file3 = 'haarcascade_fullbody.xml'
cascade3 = cv2.CascadeClassifier(cascade_file3)


face_pictures = []
full_body_pictures = []
faceless_pictures = []


for file in os.listdir(image_dir):
    if file.endswith(".jpg"):
        try:
            joined_path = os.path.join(image_dir, file)
            image = cv2.imread(joined_path)
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = cascade1.detectMultiScale(grey_image, minSize=(10,10))
            full_bodies = cascade2.detectMultiScale(grey_image)
            faceless_bodies = cascade3.detectMultiScale(grey_image)
            if (len(faces) > 0 and (len(full_bodies) == 0 and len(faceless_bodies) == 0)):
                 face_pictures.append(joined_path)
            elif (len(full_bodies) > 1):
                  full_body_pictures.append(joined_path)
            elif (len(faceless_bodies) > 0 and len(faces) == 0):
                  faceless_pictures.append(joined_path)

        except Exception as e:
            print(e)
    else:
        continue

print("face_pictures", face_pictures)
print("full_body pictures", full_body_pictures)
print("faceless_pictures", faceless_pictures)

