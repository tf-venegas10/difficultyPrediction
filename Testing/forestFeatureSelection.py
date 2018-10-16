from sklearn.ensemble import RandomForestRegressor
import MySQLdb


db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="tomasmarica",  # your password
                         # port="3306",
                         db="dajee")
cur = db.cursor()
cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT<>0;")
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
results = []
test = []
i = 1
toDo = True
features = []
xFeatures = []
yScore = []

for key in videos.keys():
    print(i)
    if toDo:
        toDo = False
        for feature in videos[key].keys():
            if feature != "qualification":
                features.append(feature)
    theseFeatures = []

    for feature in features:
        theseFeatures.append(videos[key][feature])
    xFeatures.append(theseFeatures)
    yScore.append(videos[key]["qualification"])
    i += 1
X = xFeatures
Y = yScore
names = features
rf = RandomForestRegressor()
rf.fit(X, Y)
print "Features sorted by their score:"
print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
             reverse=True)
