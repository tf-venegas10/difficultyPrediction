import MySQLdb
import json
import scipy.stats  as sy

db= MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="gh7u6wguchfrkxo1",         # your username
                     passwd="lqgvsrxvaeyb8uql", # your password
                    # port="3306",
                     db="n501u8qclhvj0mdv")
cur = db.cursor()
file=open("regressionData.json","w")
cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION<>0");
features={}
features["qualification"]=[]
for row in cur.fetchall():
    features["qualification"].append(row[1])

cur.execute("SELECT FV.video_id, name, value, qualification "+
"FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID "+
"JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID "+
 "WHERE QUALIFICATION<>0;")

for row in cur.fetchall():
    if row[1] in features.keys():
        features[row[1]].append(row[2])
    else:
        features[row[1]]=[row[2]]

for key in features.keys():

    try:
        print(key)
        print(sy.spearmanr(features[key],features['qualification']))
        print(sy.pearsonr(features[key],features['qualification']))
    except Exception :
        print ("*******************************************"+key+" FAILED **************")
