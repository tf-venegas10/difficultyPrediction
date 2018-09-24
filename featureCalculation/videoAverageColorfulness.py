import numpy as np
import imutils
import cv2
import os
import sys
import MySQLdb
import re
import subprocess
import math


def getVideoDurationSecs(path_to_video):
    result = subprocess.Popen(["C:/ffmpeg/bin/ffprobe.exe", path_to_video],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time = ([x for x in result.stdout.readlines() if "Duration" in x])[0].split(",")[0].strip().replace("Duration: ",
                                                                                                        "").split(":")
    print(time)
    mult = 3600
    duration = 0
    for i in range(3):
        duration += int(float(time[i])) * mult
        mult /= 60
    return duration


def image_colorfulness(image):
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))

    # compute rg = R - G
    rg = np.absolute(R - G)

    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)

    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))

    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

    # derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)


# DB connection with our dataset server
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

cur = db.cursor()

ids = {}

cur.execute("SELECT * FROM learning_resources;")
for row in cur.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "C:/Tesis ISIS/videosLu/frontend/public/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "C:/Tesis ISIS/videosLu/frontend/public/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[str(row[0])] = name

vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION  WHERE QUALIFICATION_AMOUNT>0")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

vids_amount = len(vids)
db.close()

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

ospath = os.path.dirname(__file__)
ospath = ospath.replace("/featureCalculation", "")
rootdir = "C:/Tesis ISIS/videosLu/frontend/public/Coursera"
export = open(ospath + '/InitialData/video_caption_text.json', 'w')
img_path = (ospath + "/InitialData/image4.jpg")  # .replace("/", "\\")
processed = 0

output = open("Video_Average_Colorfulness.sql", "a")

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        vid_path = os.path.join(subdir, file)
        # vid_path = (ospath + "/InitialData/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")
        # print(img_path)
        # print(vid_path)
        if file.endswith(".mp4"):
            route = os.path.join(subdir, file)
            name = route.replace("\\", "/")
            print(name)
            for key in vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                if name.startswith(key):
                    cap = cv2.VideoCapture(vid_path)
                    counti = 0
                    duration = getVideoDurationSecs(vid_path)
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    print("Duration [s]: " + str(duration))
                    interval = int(math.floor((frame_count / duration) * 1))
                    print("Interval: " + str(interval))
                    colorful = 0.0
                    amount = 0

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            if counti % interval == 0:
                                try:
                                    # cv2.imshow('frame', frame)
                                    cv2.imwrite(img_path, frame)
                                    img = cv2.imread(img_path)
                                    img = imutils.resize(img, width=250)
                                    colorful += image_colorfulness(img)
                                    amount += 1
                                except OSError:
                                    print("FILE NOT FOUND")
                        else:
                            break
                        counti = counti + 1
                    average = colorful/float(amount)
                    print("AVERAGE: "+str(average))
                    output.write(
                        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (36, " + str(
                            vids[key]) + ", " + str(average) + " );\n")
                    processed = processed + 1
                    print("Processed: " + str(processed) + "/" + str(vids_amount))
                    cap.release()
                    cv2.destroyAllWindows()
