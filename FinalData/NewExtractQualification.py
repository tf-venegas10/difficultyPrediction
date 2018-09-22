from __future__ import division

#CREATE TABLE VIDEO_QUALIFICATION (VIDEO_ID int(11) NOT NULL ,QUALIFICATION REAL(8,3),QUALIFICATION_AMOUNT int(11),  PRIMARY KEY (VIDEO_ID) )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#for i in xrange(1,5841):
#    write.write("INSERT INTO VIDEO_QUALIFICATION (VIDEO_ID, QUALIFICATION, QUALIFICATION_AMOUNT) VALUES ("+str(i)+",0,0);\n")

#write.close()
import json
write=open("NewQualification.sql","w+")
read=open("./../initialData/evaluations_new.json","r")



videosQual={}
videosNumber={}
#cur.execute("SELECT * FROM VIDEO_QUALIFICATION;");
#for row in cur.fetchall():
#    videosQual[row[0]]=row[1]
#    videosNumber[row[0]]=row[2]

for i in xrange(1,5841):
    videosQual[i] = 0
    videosNumber[i]= 0


text=read.read()
users=json.loads(text)
total=0
for user in users:
    for eval in user['evaluations']:
        videosNumber[eval['videoId']]+=1
        dif=-1
        if eval['difficulty']=="Easy":
            dif=5
        elif eval['difficulty']=="VeryEasy":
            dif=4
        elif eval['difficulty']=="Intermediate":
            dif=3
        elif eval['difficulty']=="Difficult":
            dif=2
        elif eval['difficulty']=="VeryDifficult":
            dif=1
        videosQual[eval['videoId']]= (videosQual[eval['videoId']]*(videosNumber[eval['videoId']]-1)+ dif)/videosNumber[eval['videoId']]
        total+=1
print("json processing done")

for i in xrange(1,5841):
    if(videosQual[i]!=0):
        write.write("UPDATE VIDEO_QUALIFICATION SET QUALIFICATION="+str(videosQual[i])+", QUALIFICATION_AMOUNT="+str(videosNumber[i])+" WHERE VIDEO_ID="+str(i)+";\n")



write.close()
read.close()
print("The total number of evaluations acquired was: "+str(total))
