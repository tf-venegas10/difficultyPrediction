import MySQLdb
import numpy as np
from sklearn.model_selection import train_test_split
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
    print(videos.keys())
    for key in videos.keys():
        print(i)
        if toDo:
            toDo = False
            for feature in videos[key].keys():
                if feature != "qualification" and feature != "VIDEOID":
                    features.append(feature)
        theseFeatures = []

        for feature in features:
            theseFeatures.append(videos[key][feature])
        xFeatures.append(np.array(theseFeatures))
        yScore.append(videos[key]["qualification"])
        i += 1
    X = np.array(xFeatures)
    Y = np.array(yScore)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.25, random_state = 42)
    return (X_train, X_test, y_train, y_test)
