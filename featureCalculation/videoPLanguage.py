import json
from pygments.lexers import guess_lexer


# Feature id 14
def compose(words, init, end):
    comp = ""
    for i in range(init, end):
        comp += words[i]
    return comp


transcriptFile = open('../InitialData/video_caption_text.json', 'r', encoding="utf8")
lines = transcriptFile.read()
transcript = json.loads(lines)

file = open("videoPLanguage.sql", "a")
window = 1

for trans in transcript:
    text = trans['text']
    print(text)
    words = text.split(" ")
    while window < len(words):
        for i in range(len(words) + 1 - window):
            comp = compose(words, i, i + window)
            print(comp)
            try:
                value = guess_lexer(comp)
                # print(value)
                # file.write(
                # "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (14, " + str(trans['id']) + ", " + str(
                # value) + " );\n")
            except(UnicodeDecodeError):
                print ("not read at id: " + str(trans['id']))
                # print row[1]
        window = window + 1

file.close()
transcriptFile.close()
