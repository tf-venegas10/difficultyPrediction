from PIL import Image
from pytesseract import image_to_string
import cv2
import os
import jellyfish
import sys
import json
import MySQLdb

dbcomplete = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                             # your host, usually localhost
                             user="znrmxn5ahxiedok5",  # your username
                             passwd="r8lkor9pav5ag5uz",  # your password
                             # port="3306",
                             db="uzzonr2rx4qx8zu4")

db = MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # your host, usually localhost
                     user="gh7u6wguchfrkxo1",  # your username
                     passwd="lqgvsrxvaeyb8uql",  # your password
                     # port="3306",
                     db="n501u8qclhvj0mdv")

curcomplete = dbcomplete.cursor()
cur = db.cursor()

ids = {}

curcomplete.execute("SELECT * FROM learning_resources;")
for row in curcomplete.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/", "")
    name = path.split(".")[0] + ".mp4"
    ids[str(row[0])] = name

dbcomplete.close()

vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION  WHERE QUALIFICATION_AMOUNT>0")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

print(vids)
db.close()

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def similitude(val1, val2):
    return jellyfish.jaro_distance(unicode(val1), unicode(val2)) > 0.60


ospath = os.path.dirname(__file__)
ospath = ospath.replace("\\featureCalculation", "")
rootdir = "E:\Coursera"
export = open(ospath + '\InitialData\\video_caption_text.json', 'w')
img_path = (ospath + "/InitialData/image.jpg")  # .replace("/", "\\")
texts = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        vid_path = os.path.join(subdir, file)
        print(vid_path)
        # vid_path = (ospath + "/InitialData/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")

        # print(img_path)
        # print(vid_path)
        if file.endswith(".mp4"):
            route = os.path.join(subdir, file)
            name = route.replace("E:\Coursera\\", "").replace("\\", "/")
            print(name)
            if name in vids:
                text = [""]
                cap = cv2.VideoCapture(vid_path)
                interval = 120
                counti = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        if counti % interval == 0:
                            try:
                                # cv2.imshow('frame', frame)
                                cv2.imwrite(img_path, frame)
                                img = Image.open(img_path)
                                # print(img)
                                frame_text = image_to_string(img)
                                # print(frame_text)
                                comp_text = text.pop()
                                if not similitude(frame_text, comp_text) and frame_text != "":
                                    text.append(comp_text)
                                    text.append(frame_text)
                                elif similitude(frame_text, comp_text) and frame_text != "":
                                    text.append(frame_text)
                                else:
                                    text.append(comp_text)
                                # print(image_to_string(img, lang='eng'))
                            except OSError:
                                print("FILE NOT FOUND")
                            # time.sleep(5)
                        counti = counti + 1
                    else:
                        # print(counti)
                        break
                cap.release()
                cv2.destroyAllWindows()
                # print(text)
                texts.append({'id': vids[name], 'path': name, 'text': " ".join(text)})
conversion = json.dumps(texts, ensure_ascii=False)
export.write(conversion)
export.close()
print(texts)
