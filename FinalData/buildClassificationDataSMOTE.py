import MySQLdb
import json
import random
from imblearn.over_sampling import SMOTE

# db = MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # your host, usually localhost
#                      user="gh7u6wguchfrkxo1",  # your username
#                      passwd="lqgvsrxvaeyb8uql",  # your password
#                      # port="3306",
#                      db="n501u8qclhvj0mdv")
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")
cur = db.cursor()
# file=open("classificationData.json","w")
# testSet=open("testSetClassification.json","w")
csvTraining = open("classificationData_SMOTE.csv", "w")
csvTestSet = open("testSetClassification_SMOTE.csv", "w")

cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION<>0");
videos = {}
for row in cur.fetchall():
    videos[row[0]] = {}
    videos[row[0]]["VIDEOID"] = row[0]
    # if (float(row[1]) <= 1.5):
    #     videos[row[0]]["qualification"] = "very difficult"
    # elif(float(row[1])<2.5):
    #     videos[row[0]]["qualification"] = "difficult"
    # elif(float(row[1])<=3.5):
    #     videos[row[0]]["qualification"] = "neutral"
    # elif(float(row[1])<4.5):
    #     videos[row[0]]["qualification"] = "easy"
    # else:
    #     videos[row[0]]["qualification"] = "very easy"

    if (float(row[1]) < 2.34):
        videos[row[0]]["qualification"] = "difficult"
    elif (float(row[1]) < 3.67):
        videos[row[0]]["qualification"] = "intermediate"
    else:
        videos[row[0]]["qualification"] = "easy"

cur.execute("SELECT FV.video_id, name, value, qualification " +
            "FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID " +
            "JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID " +
            "WHERE (QUALIFICATION<>0 );")

for row in cur.fetchall():
    videos[row[0]][row[1]] = row[2]

results = []
test = []
i = 1
toDo = True
features = []
xFeatures = []
yScore = []
xTestFeatures = []
yTestScore = []
for key in videos.keys():
    print(i)
    if toDo:
        toDo = False
        for feature in videos[key].keys():
            if feature != "qualification":
                features.append(feature)
    theseFeatures = []
    if (random.random() < 0.3):
        for feature in features:
            theseFeatures.append(videos[key][feature])
        xTestFeatures.append(theseFeatures)
        yTestScore.append(videos[key]["qualification"])
    else:
        for feature in features:
            theseFeatures.append(videos[key][feature])
        xFeatures.append(theseFeatures)
        yScore.append(videos[key]["qualification"])
    i += 1

sm = SMOTE()
x_Features_res, y_Score_res = sm.fit_sample(xFeatures, yScore)
print("total lenght after SMOTE: " + str(len(y_Score_res)))

for feature in features:
    csvTraining.write(feature + ";")
    csvTestSet.write(feature + ";")
csvTraining.write("score\n")
csvTestSet.write("score\n")

i = 0
for video in x_Features_res:
    for feature in video:
        csvTraining.write(str(feature) + ";")
    csvTraining.write(str(y_Score_res[i]) + "\n")
    i += 1
print("There are " + str(i) + " videos on the training set (SMOTE was applied)")

i = 0
for video in xTestFeatures:
    for feature in video:
        csvTestSet.write(str(feature) + ";")
    csvTestSet.write(str(y_Score_res[i]) + "\n")
    i += 1
print("There are " + str(i) + " videos on the testing set (no SMOTE- original videos)")

object = json.dumps(results)
# file.write(object)
object = json.dumps(test)
# testSet.write(object)
# file.close()
# testSet.close()
cur.close()
csvTestSet.close()
csvTraining.close()