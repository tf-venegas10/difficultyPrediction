import MySQLdb
import json
import random
import sys

testingEasy = []
testingNotEasy = []
trainingEasy = []
trainingNotEasy = []

for k in xrange(1000):
    arg = sys.argv[1]
    exclusive = False
    if arg == 'true':
        exclusive = True

    # db= MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
    #                      user="gh7u6wguchfrkxo1",         # your username
    #                      passwd="lqgvsrxvaeyb8uql", # your password
    #                     # port="3306",
    #                      db="n501u8qclhvj0mdv")
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="tomasmarica",  # your password
                         # port="3306",
                         db="dajee")
    cur = db.cursor()
    # file=open("classificationData.json","w")
    # testSet=open("testSetClassification.json","w")

    csvTraining = None
    csvTestSet = None
    if exclusive:
        csvTraining = open("../FinalData/classificationDataExclusive.csv", "w")
        csvTestSet = open("../FinalData/testSetClassificationExclusive.csv", "w")
    else:
        csvTraining = open("../FinalData/classificationData.csv", "w")
        csvTestSet = open("../FinalData/testSetClassification.csv", "w")

    cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT<>0");
    temp = {}
    videos = {}
    for row in cur.fetchall():
        temp[row[0]] = {}
        temp[row[0]]["VIDEOID"] = row[0]

        # if (float(row[1]) < 2.34):
        #     temp[row[0]]["qualification"] = "difficult"
        # elif (float(row[1]) < 3.67):
        #     temp[row[0]]["qualification"] = "intermediate"
        # else:
        #     temp[row[0]]["qualification"] = "easy"
        temp[row[0]]["qualification"] = row[1]

    cur.execute("SELECT FV.video_id, name, value, qualification " +
                "FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID " +
                "JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID " +
                "WHERE QUALIFICATION_AMOUNT<>0;")

    for row in cur.fetchall():
        temp[row[0]][row[1]] = row[2]

    if exclusive:
        dbcomplete = MySQLdb.connect(host="localhost",
                                     # your host, usually localhost
                                     user="root",  # your username
                                     passwd="tomasmarica",  # your password
                                     # port="3306",
                                     db="cloud_backup")
        curcomplete = dbcomplete.cursor()
        curcomplete.execute("SELECT VIDEO_ID FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT>0;")

        ids = []
        for row in curcomplete.fetchall():
            ids.append(row[0])

        print "PREV SCEMA LENGTH: " + str(len(ids))

        for key in temp.keys():
            if key not in ids:
                videos[key] = temp[key]
    else:
        videos = temp

    results = []
    test = []
    i = 1
    toDo = True
    features = []
    xFeatures = []
    yScore = []
    xTestFeatures = []
    yTestScore = []
    # for key in videos.keys():
    #     print(i)
    #     if toDo:
    #         toDo = False
    #         for feature in videos[key].keys():
    #             if feature != "qualification":
    #                 features.append(feature)
    #     theseFeatures = []
    #     if (random.random() < 0.3):
    #         for feature in features:
    #             theseFeatures.append(videos[key][feature])
    #         xTestFeatures.append(theseFeatures)
    #         yTestScore.append(videos[key]["qualification"])
    #     else:
    #         for feature in features:
    #             theseFeatures.append(videos[key][feature])
    #         xFeatures.append(theseFeatures)
    #         yScore.append(videos[key]["qualification"])
    #     i += 1
    keys_used = []
    is_test = True
    while len(keys_used) != len(videos.keys()):
        index = random.randint(1, 6000)
        if index in videos.keys() and index not in keys_used:
            if toDo:
                toDo = False
                for feature in videos[index].keys():
                    if feature != "qualification":
                        features.append(feature)
            theseFeatures = []
            if is_test and len(xTestFeatures) < len(videos.keys())*0.3:
                is_test = False
                for feature in features:
                    theseFeatures.append(videos[index][feature])
                xTestFeatures.append(theseFeatures)
                yTestScore.append(videos[index]["qualification"])
            else:
                is_test = True
                for feature in features:
                    theseFeatures.append(videos[index][feature])
                xFeatures.append(theseFeatures)
                yScore.append(videos[index]["qualification"])
            keys_used.append(index)

    x_Features_res, y_Score_res = (xFeatures, yScore)
    print("total lenght: " + str(len(y_Score_res)))

    for feature in features:
        csvTraining.write(feature + ";")
        csvTestSet.write(feature + ";")
    csvTraining.write("score\n")
    csvTestSet.write("score\n")

    numberOfEasy = 0
    i = 0
    for video in x_Features_res:
        for feature in video:
            csvTraining.write(str(feature) + ";")
        csvTraining.write(str(y_Score_res[i]) + "\n")
        if (y_Score_res[i] == "Easy"):
            numberOfEasy += 1
        i += 1
    print("There are " + str(i) + " videos on the training set (no-SMOTE was applied)")
    trainingEasy.append(numberOfEasy)
    trainingNotEasy.append(i - numberOfEasy)
    numberOfEasy = 0
    i = 0
    for video in xTestFeatures:
        for feature in video:
            csvTestSet.write(str(feature) + ";")
        csvTestSet.write(str(y_Score_res[i]) + "\n")
        if (y_Score_res[i] == "Easy"):
            numberOfEasy += 1
        i += 1
    print("There are " + str(i) + " videos on the testing set (no SMOTE- original videos)")
    testingEasy.append(numberOfEasy)
    testingNotEasy.append(i - numberOfEasy)

    object = json.dumps(results)
    # file.write(object)
    object = json.dumps(test)
    # testSet.write(object)
    # file.close()
    # testSet.close()
    cur.close()
    csvTestSet.close()
    csvTraining.close()
    print str(k)+"/1000"

experiment = open("../Testing/reparticion.csv", "w+")
experiment.write("Experiment#;Easy_Training; NotEasy_Training; Easy_Testing; NotEasy_Testing\n")
for i in xrange(len(testingNotEasy)):
    experiment.write(
        str(i) + ";" + str(trainingEasy[i]) + ";" + str(trainingNotEasy[i]) + ";" + str(testingEasy[i]) + ";" + str(
            testingNotEasy[i]) + "\n")

experiment.close()
