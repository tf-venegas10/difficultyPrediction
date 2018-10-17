from random import random

import MySQLdb
import numpy as np
def  getDataSet():
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="tomasmarica",  # your password
                         # port="3306",
                         db="dajee")
    cur = db.cursor()
    cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT>2;")
    videos = {}
    for row in cur.fetchall():
        videos[row[0]] = {}
        videos[row[0]]["VIDEOID"] = row[0]

        videos[row[0]]["qualification"] = row[1]

    cur.execute("SELECT FV.video_id, name, value, qualification " +
                "FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID " +
                "JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID " +
                "WHERE QUALIFICATION_AMOUNT>2 AND FEATURE_ID<100;")

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
    X = np.array(xFeatures)
    Y = np.array(yScore)
    X_test = np.array(xTestFeatures)
    Y_test = np.array(yTestScore)
    return (X,Y, X_test,Y_test)
