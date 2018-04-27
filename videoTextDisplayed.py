from PIL import Image
from pytesseract import image_to_string
import cv2
import time
import os

ospath = os.path.dirname(__file__)
img_path = (ospath + "/image.jpg")#.replace("/", "\\")
vid_path = (ospath + "/01_how-can-i-succeed-in-this-course.mp4")#.replace("/", "\\")

print(img_path)
print(vid_path)

cap = cv2.VideoCapture(vid_path)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        try:
            cv2.imshow('frame', frame)
            cv2.imwrite(img_path, frame)
            img = Image.open(img_path)
            #print(img)
            #print(image_to_string(img))
            print(image_to_string(img, lang='eng'))
        except FileNotFoundError:
            print("FILE NOT FOUND")
        #time.sleep(5)
cap.release()
cv2.destroyAllWindows()
