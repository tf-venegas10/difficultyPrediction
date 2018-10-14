import json
import MySQLdb

# VIDEO_PAUSES : ID = 46
# VIDEO_BACK_SEEKS : ID = 47
# VIDEO_FORWARD_SEEKS : ID = 48
# VIDEO_TIME_SPENT : ID = 49
# VIDEO_DURATION_OBSERVED_RATIO : ID = 50

# Evaluations load from json file, generated from MongoDB export
transcriptFile = open('../InitialData/evaluations_new.json', 'r')
lines = transcriptFile.read()
data = json.loads(lines)

# This section defines files to export the sql queries
file_pauses = open("Video_Pauses.sql", "w")
file_back_seeks = open("Video_Back_Seeks.sql", "w")
file_forward_seeks = open("Video_Forward_Seeks.sql", "w")
file_time_spent = open("Video_Time_Spent.sql", "w")
file_duration_observed_ratio = open("Video_Duration_Observed_Ratio.sql", "w")

# Variable to store average results for every video
results = {}

# Iteration meant to explore all user data
for user in data:
    evaluations = user['evaluations']
    for ev in evaluations:
        id = ev['videoId']
        # If there is no existent information about the video specified by id, a default data structure is made,
        # the information is added otherwise

        print 'ID: ' + str(id)
        print 'START TIME: ' + str(ev['startTime'])
        print 'END TIME: ' + str(ev['endTime'])
        print '\n'
        if id not in results:
            results[id] = {
                'amount': 1,
                'pauses': ev['numberOfPauses'],
                'backseeks': ev['numberOfBackSeeks'],
                'forwardseeks': ev['numberOfForwardSeeks'],
                'timespent': ev['endTime'] - ev['startTime']
            }
        else:
            results[id]['amount'] += 1
            results[id]['pauses'] += ev['numberOfPauses']
            results[id]['backseeks'] += ev['numberOfBackSeeks']
            results[id]['forwardseeks'] += ev['numberOfForwardSeeks']
            results[id]['timespent'] += ev['endTime'] - ev['startTime']

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

cur = db.cursor()

durations = {}
cur.execute("SELECT * FROM VIDEO_DURATION")
for row in cur.fetchall():
    durations[row[0]] = row[1]

cur.close()
db.close()

# From the extracted interactions the queries are built to insert in the database
length = len(results.keys())
iter = 0
for key in results.keys():
    pauses = float(results[key]['pauses']) / float(results[key]['amount'])
    backseeks = float(results[key]['backseeks']) / float(results[key]['amount'])
    forwardseeks = float(results[key]['forwardseeks']) / float(results[key]['amount'])
    timespent = (float(results[key]['timespent']) / float(results[key]['amount'])) / 60000.0
    ratio = timespent/durations[key]

    file_pauses.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (46, " + str(key) + ", " + str(
            pauses) + " );\n")
    file_back_seeks.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (47, " + str(key) + ", " + str(
            backseeks) + " );\n")
    file_forward_seeks.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (48, " + str(key) + ", " + str(
            forwardseeks) + " );\n")
    file_time_spent.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (49, " + str(key) + ", " + str(
            timespent) + " );\n")
    file_duration_observed_ratio.write(
        "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (50, " + str(key) + ", " + str(
            ratio) + " );\n")
    iter += 1
    print 'PROCESSED: ' + str(iter) + '/' + str(length)

file_pauses.close()
file_back_seeks.close()
file_forward_seeks.close()
file_time_spent.close()
