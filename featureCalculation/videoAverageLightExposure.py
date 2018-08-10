from PIL import Image
import cv2
import os
import sys
import MySQLdb
import re
import subprocess
import math
import numpy as np


def getVideoDurationSecs(path_to_video):
    result = subprocess.Popen(["C:/Users/juanm/Downloads/ffmpeg/bin/ffprobe.exe", path_to_video],
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


def calculateAverageLightExposure(image):
    pixels = image.reshape((image.shape[0] * image.shape[1], 3))
    H, S, V = pixels.T
    count = np.bincount(V)
    amount = 0.0
    weight = 0.0
    hue = 0.0
    for val in count:
        amount += val
        hue += weight * val
        weight += 1
    hue /= amount
    return hue


# DB connection with our dataset server
dbcomplete = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                             # your host, usually localhost
                             user="znrmxn5ahxiedok5",  # your username
                             passwd="r8lkor9pav5ag5uz",  # your password
                             # port="3306",
                             db="uzzonr2rx4qx8zu4")

# DB connection with our data server
db = MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # your host, usually localhost
                     user="gh7u6wguchfrkxo1",  # your username
                     passwd="lqgvsrxvaeyb8uql",  # your password
                     # port="3306",
                     db="n501u8qclhvj0mdv")

curcomplete = dbcomplete.cursor()
cur = db.cursor()

ids = {}

# Path search
curcomplete.execute("SELECT * FROM learning_resources;")
for row in curcomplete.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "E:/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "E:/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[str(row[0])] = name

dbcomplete.close()

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

ospath = os.path.dirname(__file__).replace("/featureCalculation", "")
rootdir = "E:/Coursera"
img_path = (ospath + "/InitialData/image.jpg")  # .replace("/", "\\")
processed = 0

output = open("Video_Average_Light_Exposure.sql", "a")

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
                    counti = 0
                    cap = cv2.VideoCapture(vid_path)
                    duration = getVideoDurationSecs(vid_path)
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    print("Duration [s]: " + str(duration))
                    interval = int(math.floor((frame_count / duration) * 1))
                    print("Interval: " + str(interval))
                    average = 0.0
                    amount = 0.0

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            if counti % interval == 0:
                                try:
                                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                                    average += calculateAverageLightExposure(hsv)
                                    amount += 1
                                except OSError:
                                    print("FILE NOT FOUND")
                        else:
                            break
                        counti = counti + 1
                    if not amount == 0:
                        average /= amount
                    else:
                        average = 0.0
                    print("AVERAGE LIGHT EXPOSURE: " + str(average))
                    processed = processed + 1
                    print("Processed: " + str(processed) + "/" + str(vids_amount))
                    cap.release()
                    cv2.destroyAllWindows()
                    output.write(
                        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (41, " + str(
                            vids[key]) + ", " + str(average) + " );\n")
