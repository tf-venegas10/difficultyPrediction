import json

# Feature id 8

transcriptFile = open('../InitialData/evaluations_new.json', 'r')
lines = transcriptFile.read()
evaluations = json.loads(lines)

file_pauses = open("Video_Pauses.sql", "w")
file_ = open("Video_Pauses.sql", "w")