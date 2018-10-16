import subprocess
import os
import re
import MySQLdb
import sys
import numpy
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction


def convert_video_to_wav(path):
    if os.path.exists("../InitialData/audio.wav"):
        os.remove("../InitialData/audio.wav")
    command = "ffmpeg -i " + path + " -ab 160k -ac 1 -ar 44100 -vn ../InitialData/audio.wav"
    subprocess.call(command, shell=True)


def extract_audio_features():
    [Fs, x] = audioBasicIO.readAudioFile("../InitialData/audio.wav")
    data = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
    # Extract features values from analysis
    values = data[0]
    # Extract feature names from analysis
    names = data[1]

    features = {}
    for i in xrange(len(names)):
        features[names[i]] = numpy.mean(values[i])
    return features


convert_video_to_wav("")
feat = extract_audio_features()
print feat

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
        "C:/Tesis ISIS/videosLu/frontend/public/Coursera").replace("/Users/rubenmanrique/Downloads/CourseraTexto/",
                                                                   "C:/Tesis ISIS/videosLu/frontend/public/Coursera")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[str(row[0])] = name

vids = {}
cur.execute("SELECT * FROM VIDEO_QUALIFICATION VQ WHERE QUALIFICATION_AMOUNT>0")
for row in cur.fetchall():
    if str(row[0]) in ids:
        vids[ids[str(row[0])]] = row[0]

vids_amount = len(vids)
cur.close()
db.close()

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

ospath = os.path.dirname(__file__)
ospath = ospath.replace("/featureCalculation", "")
rootdir = "C:/Tesis ISIS/videosLu/frontend/public/Coursera"
processed = 0

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
                    text = [""]
                    counti = 0
                    convert_video_to_wav(vid_path)
                    features = extract_audio_features()
                    featID = 51
                    for fet in sorted(features.keys()):
                        output = open(fet + ".sql", 'a')
                        val = features[fet]
                        output.write(
                            "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES ("+featID+", " + str(
                                vids[key]) + ", " + str(val) + " );\n")
                        output.close()
                    processed = processed + 1
                    print("Processed: " + str(processed) + "/" + str(vids_amount))
