from textblob import TextBlob
import json
import time
import datetime

# Feature id 9

transcriptFile = open('../InitialData/video_caption_text.json', 'r')
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("Video_Noun_Phrases.sql", "a")
file.write("-- Feature update: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))+"\n")

for trans in transcript:
    text = trans['text']
    # print(text)
    try:
        blob = TextBlob(text)
        noun_phrases = blob.noun_phrases
        value = len(noun_phrases)
        print("NOUN_PHRASES: "+str(value))
    except(UnicodeDecodeError):
        print "not read at id: " + str(trans['id'])
        # print row[1]
        value = 0
    file.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (14, " + str(trans['id']) + ", " + str(
            value) + " );\n")

file.close()
transcriptFile.close()
