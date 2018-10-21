import MySQLdb
import numpy as np
from sklearn.model_selection import train_test_split


# Function that gets the dataset of evaluated videos
def getDataSet(maxFeatureId):
    # The SQL database reference is initialized
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="tomasmarica",  # your password
                         # port="3306",
                         db="dajee")
    cur = db.cursor()
    # Declaration of a statement that retrieves the videos with more than 2 qualifications
    cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT>2;")
    videos = {}

    # In this loop, the videos are assigned in a dictionary
    for row in cur.fetchall():
        videos[row[0]] = {}
        videos[row[0]]["VIDEOID"] = row[0]

        videos[row[0]]["qualification"] = row[1]

    # This query gets the joint information about the videos and their features
    cur.execute("SELECT FV.video_id, name, value, qualification " +
                "FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID " +
                "JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID " +
                "WHERE QUALIFICATION_AMOUNT>2 AND FEATURE_ID<%0.0f;" % maxFeatureId)

    # In this loop the features and their values are added to the video dictionary
    for row in cur.fetchall():
        videos[row[0]][row[1]] = row[2]
    results = []
    test = []
    i = 1
    toDo = True
    features = []
    xFeatures = []
    yScore = []

    # For each video the features and scores are separated into two arrays
    for key in videos.keys():
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

    # Split array of scores and features into random train and test subsets
    '''
    TO-DO: why is the test proportion 0.25 and not 0.3, meaning 30% of the dataset? Should this be changed?
    TO-DO: why is it better to propose a 42 seed rather than leaving the default?
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

    return (X_train, y_train, X_test, y_test)
