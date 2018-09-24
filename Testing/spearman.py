import MySQLdb
import json
import scipy.stats  as sy
import math
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
file=open("regressionData.json","w")
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
    #print(str(row[1])+": "+str(row[2]))

for key in features.keys():

    try:
        #print(key)
        spe=(sy.spearmanr(features[key],features['qualification']))
        spearman[key]=spe[0]
        spearmanPval[key]=spe[1]
        pea=(sy.pearsonr(features[key],features['qualification']))
        pearson[key]=pea[0]
        pearsonPval[key]=pea[1]


    except Exception :
        print ("*******************************************"+key+" FAILED **************")
        print(len(features[key]))
        print(len(features['qualification']))

i=0
for key,value in sorted(spearman.iteritems(), key=lambda (k,v): (math.fabs(v),k)):
    i+=1
    print(i)

    if key!="qualification":
        print(key)
        print("Spearman's index: "+ str(spearman[key])+" pValue: "+str(spearmanPval[key]))
        print("Pearson's index: "+ str(pearson[key])+" pValue: "+str(pearsonPval[key]))
