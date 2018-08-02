import MySQLdb
import re
import sys
import os
from textstat.textstat import textstat


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
alt_ids = {}

curcomplete.execute("SELECT * FROM learning_resources;")
for row in curcomplete.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "E:/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "E:/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.en.srt', path)
    alt_name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.srt', path)
    ids[str(row[0])] = name
    alt_ids[str(row[0])] = alt_name

dbcomplete.close()

vids = {}
alt_vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION")
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
rootdir = "E:/Coursera"
output = open("wordsPerMinute.sql", "a")
processed = 0
vids_processed = {}

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
                key_suffix = key.replace(".en.srt", "")
                if name.startswith(key) and key_suffix not in vids_processed:
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
                    vids_processed[key_suffix] = 1
        elif file.endswith(".srt"):
            route = os.path.join(subdir, file)
            name = route.replace("\\", "/")
            print(name)
            for key in alt_vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                key_suffix = key.replace(".srt", "")
                if name.startswith(key) and key_suffix not in vids_processed:
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
                    vids_processed[key_suffix] = 1
output.close()
