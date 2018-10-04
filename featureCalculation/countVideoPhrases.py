import json
from textstat.textstat import textstat

# Feature id 8

transcriptFile = open('../InitialData/video_caption_text.json', 'r')
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("Video_Phrases_Count.sql", "w")

for trans in transcript:
    text = trans['text']
    print(text)
    try:
        value = textstat.sentence_count(text)
    except(UnicodeDecodeError):
        print "not read at id: " + str(trans['id'])
        # print row[1]
        value = 0
    file.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (8, " + str(trans['id']) + ", " + str(
            value) + " );\n")

file.close()
transcriptFile.close()
