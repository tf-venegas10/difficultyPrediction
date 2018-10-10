from __future__ import division

#CREATE TABLE VIDEO_QUALIFICATION (VIDEO_ID int(11) NOT NULL ,QUALIFICATION REAL(8,3),QUALIFICATION_AMOUNT int(11),  PRIMARY KEY (VIDEO_ID) )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#for i in xrange(1,5841):
#    write.write("INSERT INTO VIDEO_QUALIFICATION (VIDEO_ID, QUALIFICATION, QUALIFICATION_AMOUNT) VALUES ("+str(i)+",0,0);\n")

#write.close()
import json
write=open("Qualification_majority_vote.sql","w")
read=open("./../initialData/evaluations_new.json","r")
read1=open("./../initialData/evaluations.json","r")
read2=open("./../initialData/evaluations_phase2.json","r")



videosQual={}
videosNumber={}
#cur.execute("SELECT * FROM VIDEO_QUALIFICATION;");
#for row in cur.fetchall():
#    videosQual[row[0]]=row[1]
#    videosNumber[row[0]]=row[2]

for i in xrange(1,5841):
    videosQual[i] = {"Easy":0,"VeryEasy":0,"Intermediate":0,"Difficult":0,"VeryDifficult":0}
    videosNumber[i]= 0


text=read.read()
users=json.loads(text)
total=0
for user in users:
    for eval in user['evaluations']:
        videosNumber[eval['videoId']]+=1
        if eval['difficulty']=="Easy":
            videosQual[eval['videoId']]["Easy"]+=1
        elif eval['difficulty']=="VeryEasy":
            videosQual[eval['videoId']]["VeryEasy"] += 1
        elif eval['difficulty']=="Intermediate":
            videosQual[eval['videoId']]["Intermediate"] += 1
        elif eval['difficulty']=="Difficult":
            videosQual[eval['videoId']]["Difficult"] += 1
        elif eval['difficulty']=="VeryDifficult":
            videosQual[eval['videoId']]["VeryDifficult"] += 1
        total+=1

# reading the original data-set
text=read1.read()
users=json.loads(text)

for user in users:
    for eval in user['evaluations']:
        if int(eval['resource']['evaluation'][0]['answer']['value'])<1 or int(eval['resource']['evaluation'][0]['answer']['value'])>5 :
            print(int(eval['resource']['evaluation'][0]['answer']['value']))
        videosNumber[eval['resource']['id']]+=1
        if int(eval['resource']['evaluation'][0]['answer']['value'])==5:
            videosQual[eval['resource']['id']]["Easy"]+=1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==4:
            videosQual[eval['resource']['id']]["VeryEasy"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==3:
            videosQual[eval['resource']['id']]["Intermediate"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==2:
            videosQual[eval['resource']['id']]["Difficult"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==1:
            videosQual[eval['resource']['id']]["VeryDifficult"] += 1
        total+=1
text=read2.read()
users=json.loads(text)

for user in users:
    for eval in user['evaluations']:
        if int(eval['resource']['evaluation'][0]['answer']['value'])<1 or int(eval['resource']['evaluation'][0]['answer']['value'])>5 :
            print(int(eval['resource']['evaluation'][0]['answer']['value']))
        videosNumber[eval['resource']['id']]+=1
        if int(eval['resource']['evaluation'][0]['answer']['value'])==5:
            videosQual[eval['resource']['id']]["Easy"]+=1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==4:
            videosQual[eval['resource']['id']]["VeryEasy"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==3:
            videosQual[eval['resource']['id']]["Intermediate"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==2:
            videosQual[eval['resource']['id']]["Difficult"] += 1
        elif int(eval['resource']['evaluation'][0]['answer']['value'])==1:
            videosQual[eval['resource']['id']]["VeryDifficult"] += 1
        total+=1

print("json processing done")

for video in videosQual:
    major="VeryDifficult"
    num = 0
    if videosQual[video]!={"Easy":0,"VeryEasy":0,"Intermediate":0,"Difficult":0,"VeryDifficult":0}:
        for diff in videosQual[video].keys():
            if(videosQual[video][diff]>=num):
                num=videosQual[video][diff]
                major=diff
        videosQual[video]["vote"]=major
print("json processing done")

for i in xrange(1,5841):
    if videosQual[i]!={"Easy":0,"VeryEasy":0,"Intermediate":0,"Difficult":0,"VeryDifficult":0}:
        write.write("UPDATE VIDEO_QUALIFICATION SET QUALIFICATION='"+str(videosQual[i]["vote"])+"', QUALIFICATION_AMOUNT="+str(videosNumber[i])+" WHERE VIDEO_ID="+str(i)+";\n")



write.close()
read.close()
print("The total number of evaluations acquired was: "+str(total))
