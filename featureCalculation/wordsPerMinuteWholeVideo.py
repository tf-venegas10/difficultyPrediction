import MySQLdb
import re
import subprocess
import os
import sys
from textstat.textstat import textstat
import json
import datetime
import time


def getVideoDurationMins(path_to_video):
    result = subprocess.Popen(["C:/ffmpeg/bin/ffprobe.exe", path_to_video],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time = ([x for x in result.stdout.readlines() if "Duration" in x])[0].split(",")[0].strip().replace("Duration: ",
                                                                                                        "").split(":")
    print(time)
    mult = 60.0
    duration = 0.0
    for i in range(3):
        duration += float(time[i]) * mult
        mult /= 60.0
    return duration


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
cur.execute("SELECT * FROM VIDEO_QUALIFICATION VQ WHERE QUALIFICATION_AMOUNT>0 AND VQ.VIDEO_ID NOT IN "
            "(SELECT VIDEO_ID FROM FEATURES_PER_VIDEO WHERE FEATURE_ID=33);")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

print("Amount: " + str(len(vids)))
total_vids = len(vids)
db.close()

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

transcriptFile = open('../InitialData/video_caption_text.json', 'r')
lines = transcriptFile.read()
transcript = json.loads(lines)

rootdir = "C:/Tesis ISIS/videosLu/frontend/public/Coursera"
processed = 0
output = open("wordsPerMinuteWholeVideo.sql", "a")
output.write("-- Feature update: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))+"\n")

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        vid_path = os.path.join(subdir, file)
        # vid_path = (ospath + "/InitialData/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")
        # print(img_path)
        # print(vid_path)
        route = os.path.join(subdir, file)
        name = route.replace("\\", "/")
        if file.endswith(".mp4"):
            print(name)
            for key in vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                if name.startswith(key):
                    duration = getVideoDurationMins(vid_path)
                    print("Duration [s]: " + str(duration))
                    processed = processed + 1
                    print("Processed: " + str(processed)+"/"+str(total_vids))
                    # print(text)
                    for val in transcript:
                        if val['id'] == vids[key]:
                            text = val['text']
                            print(text)
                            average = 0.0
                            try:
                                value = textstat.lexicon_count(text)
                                average = float(value)/float(duration)
                            except(UnicodeDecodeError):
                                print "not read at id: " + str(val['id'])
                                # print row[1]
                                value = 0
                            output.write("INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (33, " + str(
                                vids[key]) + ", " + str(average) + " );\n")
output.close()