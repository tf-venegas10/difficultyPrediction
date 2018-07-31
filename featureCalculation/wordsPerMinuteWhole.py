import MySQLdb
import re
import subprocess
import os
import sys
from textstat.textstat import textstat


def getVideoDurationMins(path_to_video):
    result = subprocess.Popen(["C:/Users/juanm/Downloads/ffmpeg/bin/ffprobe.exe", path_to_video],
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
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "E:/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/", "E:/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[str(row[0])] = name

dbcomplete.close()

vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION ")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

print("Amount: " + str(len(vids)))
total_vids = len(vids)
db.close()

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

rootdir = "E:/Coursera"
texts = {}
processed = 0
output = open("wordsPerMinuteWhole.sql", "a")

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
                    print("Processed: " + str(processed/2)+"/"+str(total_vids))
                    # print(text)
                    if vids[key] not in texts:
                        texts[vids[key]] = {'duration': duration}
                    else:
                        texts[vids[key]]['duration'] = duration
                    break
        elif file.endswith(".txt") or file.endswith(".en.txt"):
            for key in vids.keys():
                # if not key.endswith(".mp4"):
                # print("THIS IS KEY: " + key)
                if name.startswith(key.replace(".mp4",".txt")) or name.startswith(key.replace(".mp4",".en.txt")):
                    transcript = open(name, 'r')
                    words = textstat.lexicon_count(transcript)
                    processed = processed + 1
                    print("Processed: " + str(processed/2)+"/"+str(total_vids))
                    # print(text)
                    if vids[key] not in texts:
                        texts[vids[key]] = {'words': words}
                    else:
                        texts[vids[key]]['words'] = words
                    break
for key in texts.keys():
    data = texts[key]
    if 'words' in data and 'duration' in data:
        average = float(data['words'])/data['duration']
        output.write("INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (32, " + str(
                            key) + ", " + str(average) + " );\n")

print(texts)
