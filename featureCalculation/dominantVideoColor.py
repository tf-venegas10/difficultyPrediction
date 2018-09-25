from PIL import Image
import cv2
import os
import sys
import MySQLdb
import re
import subprocess
import math
import time
import datetime


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


def getMainColors(colors, image):
    cols = image.getcolors(maxcolors=2000000)
    for col in cols:
        count = col[0]
        key = '#%02x%02x%02x' % col[1]
        if not key in colors:
            colors[key] = count
        else:
            colors[key] += count


def getDominantColor(colors):
    dominant = 0
    k_dominant = ''
    for key in colors.keys():
        if colors[key] > dominant:
            dominant = colors[key]
            k_dominant = key
    k_dominant = k_dominant.replace('#', "0x")
    return float.fromhex(k_dominant)

# DB connection with our dataset server
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

cur = db.cursor()

ids = {}

# Path search
cur.execute("SELECT * FROM learning_resources;")
for row in cur.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "C:/Tesis ISIS/videosLu/frontend/public/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "C:/Tesis ISIS/videosLu/frontend/public/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[str(row[0])] = name

vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION VQ WHERE QUALIFICATION_AMOUNT>0 AND VQ.VIDEO_ID NOT IN "
            "(SELECT VIDEO_ID FROM FEATURES_PER_VIDEO WHERE FEATURE_ID=35);")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

vids_amount = len(vids)
db.close()

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

ospath = os.path.dirname(__file__).replace("/featureCalculation", "")
rootdir = "C:/Tesis ISIS/videosLu/frontend/public/Coursera"
img_path = (ospath + "/InitialData/image2.jpg")  # .replace("/", "\\")
processed = 0

output = open("Dominant_Video_Color.sql", "a")
output.write("-- Feature update: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))+"\n")

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
                    cols = {}

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            if counti % interval == 0:
                                try:
                                    cv2.imwrite(img_path, frame)
                                    img = Image.open(img_path)
                                    getMainColors(cols, img)
                                except OSError:
                                    print("FILE NOT FOUND")
                        else:
                            break
                        counti = counti + 1
                    dominant = getDominantColor(cols)/10000
                    print("DOMINANT: " + str(dominant))
                    processed = processed + 1
                    print("Processed: " + str(processed) + "/" + str(vids_amount))
                    cap.release()
                    cv2.destroyAllWindows()
                    output.write(
                        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (35, " + str(
                            vids[key]) + ", " + str(dominant) + " );\n")
