from textstat.textstat import textstat
import json
import MySQLdb

# Feature id 9
db = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # your host, usually localhost
                     user="znrmxn5ahxiedok5",  # your username
                     passwd="r8lkor9pav5ag5uz",  # your password
                     # port="3306",
                     db="uzzonr2rx4qx8zu4")

curRead = db.cursor()
curRead.execute("SELECT * FROM resource_content")
transcriptFile = open('../InitialData/video_caption_text.json', 'r')
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("Speech_Display_Words_Ratio.sql", "a")
speech = {}

for row in curRead.fetchall():
    text = unicode(row[1], "utf-8", errors='ignore')
    try:
        value = textstat.lexicon_count(text)
    except(UnicodeDecodeError):
        print "not read at id: " + str(row[0])
        # print row[1]
        value = 0
    # curWrite.execute\
    speech[row[0]] = value
db.close()

for trans in transcript:
    text = trans['text']
    ratio = 0.0
    print(text)
    try:
        value = textstat.lexicon_count(text)
        speech_val = speech[trans['id']]
        if not speech_val == 0:
            ratio = float(value)/float(speech_val)
    except(UnicodeDecodeError):
        print "not read at id: " + str(trans['id'])
        # print row[1]
        value = 0
    file.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (34, " + str(trans['id']) + ", " + str(
            ratio) + " );\n")

file.close()
transcriptFile.close()
