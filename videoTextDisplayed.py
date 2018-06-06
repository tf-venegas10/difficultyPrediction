from PIL import Image
from pytesseract import image_to_string
import cv2
import os
import jellyfish


def similitude(val1, val2):
    return jellyfish.jaro_distance(unicode(val1), unicode(val2)) > 0.9


ospath = os.path.dirname(__file__)
img_path = (ospath + "/image.jpg")  # .replace("/", "\\")
vid_path = (ospath + "/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")

print(img_path)
print(vid_path)

text = [""]
cap = cv2.VideoCapture(vid_path)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        try:
            # cv2.imshow('frame', frame)
            cv2.imwrite(img_path, frame)
            img = Image.open(img_path)
            # print(img)
            frame_text = image_to_string(img)
            print(frame_text)
            comp_text = text.pop()
            text.append(comp_text)
            if not similitude(frame_text, comp_text) and frame_text != "":
                text.append(frame_text)
            # print(image_to_string(img, lang='eng'))
        except OSError:
            print("FILE NOT FOUND")
        # time.sleep(5)
    else:
        break
cap.release()
cv2.destroyAllWindows()
print(text)
