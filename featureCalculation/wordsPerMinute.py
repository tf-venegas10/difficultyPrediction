import MySQLdb
import re
import sys
import os
from textstat.textstat import textstat
import time
import datetime


def getMinutes(start, end):
    print("Start: " + start)
    print("End: " + end)
    v_start = start.split(":")
    v_end = end.split(":")
    time_s = 0.0
    time_e = 0.0
    mult = 60.0
    for i in range(3):
        time_s += float(v_start[i].replace(",", ".")) * mult
        time_e += float(v_end[i].replace(",", ".")) * mult
        mult /= 60
    return time_e - time_s


# DB connection with our dataset server
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

cur = db.cursor()

ids = {}
alt_ids = {}

cur.execute("SELECT * FROM learning_resources;")
for row in cur.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "C:/Tesis ISIS/videosLu/frontend/public/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "C:/Tesis ISIS/videosLu/frontend/public/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?)|(m(p(4)?)?))(\.(t(x(t)?)?)?)?', '.en.srt', path)
    alt_name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?)|(m(p(4)?)?))(\.(t(x(t)?)?)?)?', '.srt', path)
    ids[str(row[0])] = name
    alt_ids[str(row[0])] = alt_name

vids = {}
alt_vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION VQ WHERE QUALIFICATION_AMOUNT>0 AND VQ.VIDEO_ID NOT IN "
            "(SELECT VIDEO_ID FROM FEATURES_PER_VIDEO WHERE FEATURE_ID=31);")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]
        alt_vids[alt_ids[str(row[0])]] = row[0]

print("Video Amount: " + str(len(vids)))
db.close()
vid_amount = str(len(vids))

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

ospath = os.path.dirname(__file__)
ospath = ospath.replace("/featureCalculation", "")
rootdir = "C:/Tesis ISIS/videosLu/frontend/public/Coursera"
output = open("wordsPerMinute.sql", "w+")
output.write("-- Feature update: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))+"\n")
processed = 0
vids_processed = {}

print vids

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        srt_path = os.path.join(subdir, file)
        # vid_path = (ospath + "/InitialData/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")
        # print(img_path)
        # print(vid_path)
        if file.endswith(".en.srt"):
            route = os.path.join(subdir, file)
            name = route.replace("\\", "/")
            print(name)
            for key in vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                if name.startswith(key) and (vids[key] not in vids_processed):
                    srt = open(srt_path, "r")
                    time = 0
                    words = 0
                    average = 0.0
                    line = srt.readline()
                    numeration = 1
                    while not (line == "" or line == None):
                        try:
                            if numeration == int(line):
                                line = srt.readline()
                                times = line.split(" --> ")
                                time += getMinutes(times[0], times[1])
                                line = srt.readline()
                                while not (line == "\n" or line == None or line == ""):
                                    words += textstat.lexicon_count(line)
                                    line = srt.readline()
                                numeration += 1
                        except ValueError:
                            print("Adjusting format")
                        line = srt.readline()
                    if not time == 0:
                        average = float(words) / float(time)
                    if average < 0:
                        average *= -1.0
                    print("Average: " + str(average))
                    srt.close()

                    output.write(
                        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (31, " + str(
                            vids[key]) + ", " + str(average) + " );\n")
                    processed += 1
                    print("Processed: " + str(processed) + "/" + vid_amount)
                    vids_processed[vids[key]] = 1
        elif file.endswith(".srt"):
            route = os.path.join(subdir, file)
            name = route.replace("\\", "/")
            print(name)
            for key in alt_vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                if name.startswith(key) and alt_vids[key] not in vids_processed:
                    srt = open(srt_path, "r")
                    time = 0
                    words = 0
                    average = 0.0
                    line = srt.readline()
                    numeration = 1
                    while not (line == "" or line == None):
                        try:
                            if numeration == int(line):
                                line = srt.readline()
                                times = line.split(" --> ")
                                time += getMinutes(times[0], times[1])
                                line = srt.readline()
                                while not (line == "\n" or line == None or line == ""):
                                    words += textstat.lexicon_count(line)
                                    line = srt.readline()
                                numeration += 1
                        except ValueError:
                            print("Adjusting format")
                        line = srt.readline()
                    if not time == 0:
                        average = float(words) / float(time)
                    if average < 0:
                        average *= -1.0
                    print("Average: " + str(average))
                    srt.close()

                    output.write(
                        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (31, " + str(
                            alt_vids[key]) + ", " + str(average) + " );\n")
                    processed += 1
                    print("Processed: " + str(processed) + "/" + vid_amount)
                    vids_processed[alt_vids[key]] = 1
for key in sorted(vids.keys()):
    if vids[key] not in vids_processed:
        print vids[key]
        print alt_vids[key]
        print key
output.close()
