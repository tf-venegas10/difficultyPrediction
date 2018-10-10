from __future__ import division

#CREATE TABLE VIDEO_QUALIFICATION (VIDEO_ID int(11) NOT NULL ,QUALIFICATION REAL(8,3),QUALIFICATION_AMOUNT int(11),  PRIMARY KEY (VIDEO_ID) )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#for i in xrange(1,5841):
#    write.write("INSERT INTO VIDEO_QUALIFICATION (VIDEO_ID, QUALIFICATION, QUALIFICATION_AMOUNT) VALUES ("+str(i)+",0,0);\n")

#write.close()
import json
write=open("Qualification.sql","a")
read1=open("./../initialData/evaluations.json","r")
read2=open("./../initialData/evaluations_phase2.json","r")


videosQual={}
videosNumber={}
#cur.execute("SELECT * FROM VIDEO_QUALIFICATION;");
#for row in cur.fetchall():
#    videosQual[row[0]]=row[1]
#    videosNumber[row[0]]=row[2]

for i in xrange(1,5841):
    videosQual[i] = 0
    videosNumber[i]= 0


text=read1.read()
users=json.loads(text)

for user in users:
    for eval in user['evaluations']:
        if int(eval['resource']['evaluation'][0]['answer']['value'])<1 or int(eval['resource']['evaluation'][0]['answer']['value'])>5 :
            print(int(eval['resource']['evaluation'][0]['answer']['value']))

        videosNumber[eval['resource']['id']]+=1
        videosQual[eval['resource']['id']]= (videosQual[eval['resource']['id']]*(videosNumber[eval['resource']['id']]-1)+ int(eval['resource']['evaluation'][0]['answer']['value']))/videosNumber[eval['resource']['id']]

text=read2.read()
users=json.loads(text)

for user in users:
    for eval in user['evaluations']:
        if int(eval['resource']['evaluation'][0]['answer']['value'])<1 or int(eval['resource']['evaluation'][0]['answer']['value'])>5 :
            print(int(eval['resource']['evaluation'][0]['answer']['value']))
        videosNumber[eval['resource']['id']]+=1
        videosQual[eval['resource']['id']] = (videosQual[eval['resource']['id']] * (videosNumber[eval['resource']['id']] - 1) + int(eval['resource']['evaluation'][0]['answer']['value'])) / videosNumber[eval['resource']['id']]
print("json processing done")

for i in xrange(1,5841):
    if(videosQual[i]!=0):
        write.write("UPDATE VIDEO_QUALIFICATION SET QUALIFICATION="+str(videosQual[i])+", QUALIFICATION_AMOUNT="+str(videosNumber[i])+" WHERE VIDEO_ID="+str(i)+";\n")



write.close()
read1.close()
read2.close()
