import numpy as np
import MySQLdb
import matplotlib.pyplot as plt

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
 "WHERE QUALIFICATION_AMOUNT<>0 ORDER BY VQ.VIDEO_ID;")

videoId=-1
for row in cur.fetchall():
    if(videoId!=row[0]):
        features["qualification"].append(row[3])
        videoId=row[0]
    if row[1] in features.keys():
        features[row[1]].append(row[2])
    else:
        features[row[1]]=[row[2]]

values=[]
for key in features.keys():
    if(key!="qualification"):
        print(key)
        mean=np.mean(features[key])
        var= np.var(features[key])
        values.append({"key":key, "mean": mean, "var" :var, "disp": var/mean})

values= sorted(values, key=lambda k: k['disp'])
vars=[]
means=[]
keys=[]
show=False
for i in xrange(len(values)):
    if(values[i]["key"]=="VIDEO_DURATION"):
        show= True
    if show:
        print(values[i])
    keys.append(values[i]["key"])
    vars.append(values[i]["disp"])
    means.append(values[i]["mean"])
width = 1/1.5
plt.bar(keys, vars,width, color="blue")
plt.show()


