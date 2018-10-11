import numpy as np
import MySQLdb


db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

cur = db.cursor()
#file=open("regressionData.json","w")
#cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION<>0 ORDER BY VIDEO_ID");
features={}
features["qualification"]=[]
spearman={}
pearson={}
spearmanPval={}
pearsonPval={}
#for row in cur.fetchall():
#    features["qualification"].append(row[1])

cur.execute("SELECT FV.video_id, name, value, qualification "+
"FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID "+
"JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID "+
 "WHERE QUALIFICATION<>0 ORDER BY VQ.VIDEO_ID;")

videoId=-1
for row in cur.fetchall():
    if(videoId!=row[0]):
        features["qualification"].append(row[3])
        videoId=row[0]
    if row[1] in features.keys():
        features[row[1]].append(row[2])
    else:
        features[row[1]]=[row[2]]

for key in features.keys():
    print(key+ " mean: "+str(np.mean(features[key])))
    print ("Variance: " + np.var(features[key]))
