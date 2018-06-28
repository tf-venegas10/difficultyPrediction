import json
from pygments.lexers import guess_lexer

# Feature id 14

transcriptFile = open('../InitialData/video_caption_text.json', 'r', encoding="utf8")
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("videoPLanguage.sql", "a")

for trans in transcript:
    text = trans['text']
    print(text)
    try:
        value = guess_lexer(text)
        #file.write(
            #"INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (14, " + str(trans['id']) + ", " + str(
                #value) + " );\n")
    except(UnicodeDecodeError):
        print ("not read at id: " + str(trans['id']))
        # print row[1]

file.close()
transcriptFile.close()