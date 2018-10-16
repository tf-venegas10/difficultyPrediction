from sklearn.ensemble import RandomForestRegressor
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt


db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="tomasmarica",  # your password
                         # port="3306",
                         db="dajee")
cur = db.cursor()
cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION_AMOUNT<>0;")
videos = {}
for row in cur.fetchall():
    videos[row[0]] = {}
    videos[row[0]]["VIDEOID"] = row[0]

    if ((row[1]) == "Easy"):
        videos[row[0]]["qualification"] = 0
    else:
        videos[row[0]]["qualification"] = 1

cur.execute("SELECT FV.video_id, name, value, qualification " +
            "FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID " +
            "JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID " +
            "WHERE QUALIFICATION_AMOUNT<>0;")

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
            if feature != "qualification" and feature!="VIDEOID":
                features.append(feature)
    theseFeatures = []

    for feature in features:
        theseFeatures.append(videos[key][feature])
    xFeatures.append(np.array(theseFeatures))
    yScore.append(videos[key]["qualification"])
    i += 1
X = np.array(xFeatures)
Y = np.array(yScore)


names = features
rf = RandomForestRegressor()
rf.fit(X, Y)
print "Features sorted by their score:"
sortedList= sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
             reverse=True)

print(sortedList)

x=[]
y=[]
csv= open("forestFeaturesSelectionResults.csv","w+")
csv.write("Feature;Dispersion index\n")
for i in xrange(len(sortedList)):
   x.append(sortedList[i][1])
   y.append(sortedList[i][0])
   csv.write(str(sortedList[i][1])+";"+str(sortedList[i][0])+"\n")

csv.close()
plt.bar(x,y)
plt.show()
