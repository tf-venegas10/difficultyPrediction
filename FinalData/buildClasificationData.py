import MySQLdb
import json
import random

db= MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="gh7u6wguchfrkxo1",         # your username
                     passwd="lqgvsrxvaeyb8uql", # your password
                    # port="3306",
                     db="n501u8qclhvj0mdv")
cur = db.cursor()
file=open("classificationData.json","w")
testSet=open("testSetClassification.json","w")
cur.execute("SELECT * FROM VIDEO_QUALIFICATION WHERE QUALIFICATION<>0");
videos={}
for row in cur.fetchall():
    videos[row[0]]={}
    videos[row[0]]["VIDEOID"] = row[0]
    if(float(row[1])<3):
        videos[row[0]]["qualification"] = "difficult"
    elif (float(row[1]) < 4):
        videos[row[0]]["qualification"] = "intermediate"
    else:
        videos[row[0]]["qualification"] = "easy"

cur.execute("SELECT FV.video_id, name, value, qualification "+
"FROM FEATURES F JOIN FEATURES_PER_VIDEO FV ON F.ID=FV.FEATURE_ID "+
"JOIN VIDEO_QUALIFICATION VQ ON FV.VIDEO_ID=VQ.VIDEO_ID "+
 "WHERE QUALIFICATION<>0;")


for row in cur.fetchall():
    videos[row[0]][row[1]]=row[2]

results=[]
test=[]
i=1
for key in videos.keys():
    print(i)
    i+=1
    if(random.random()<0.3):
        test.append(videos[key])
    else:
        results.append(videos[key])

object=json.dumps(results)
file.write(object)
object=json.dumps(test)
testSet.write(object)
file.close()
testSet.close()
cur.close()
