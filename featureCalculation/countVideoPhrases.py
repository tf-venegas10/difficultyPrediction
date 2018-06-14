import json
from textstat.textstat import textstat
import MySQLdb
import sys

# Feature id 8

db = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # your host, usually localhost
                     user="znrmxn5ahxiedok5",  # your username
                     passwd="r8lkor9pav5ag5uz",  # your password
                     # port="3306",
                     db="uzzonr2rx4qx8zu4")

transcriptFile = open('../InitialData/video_caption_text.json', 'r')
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("Video_Phrases_Count.sql", "a")

for trans in transcript:
    text = trans['text']
    print(text)
    try:
        value = textstat.sentence_count(text)
    except(UnicodeDecodeError):
        print "not read at id: " + str(trans['id'])
        # print row[1]
        value = 0
    file.write("INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (8, " + str(trans['id']) + ", " + str(
        value) + " );\n")

file.close()
transcriptFile.close()