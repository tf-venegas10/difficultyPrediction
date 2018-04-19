from __future__ import division

#CREATE TABLE VIDEO_QUALIFICATION (VIDEO_ID int(11) NOT NULL ,QUALIFICATION REAL(8,3),QUALIFICATION_AMOUNT int(11),  PRIMARY KEY (VIDEO_ID) )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#for i in xrange(1,5841):
#    write.write("INSERT INTO VIDEO_QUALIFICATION (VIDEO_ID, QUALIFICATION, QUALIFICATION_AMOUNT) VALUES ("+str(i)+",0,0);\n")

#write.close()
import json
write=open("Qualification.sql","a")
read=open("evaluations22-03-2018.json","r")
import MySQLdb


db= MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="gh7u6wguchfrkxo1",         # your username
                     passwd="lqgvsrxvaeyb8uql", # your password
                    # port="3306",
                     db="n501u8qclhvj0mdv")
cur = db.cursor()
videosQual={}
videosNumber={}
#cur.execute("SELECT * FROM VIDEO_QUALIFICATION;");
#for row in cur.fetchall():
#    videosQual[row[0]]=row[1]
#    videosNumber[row[0]]=row[2]

for i in xrange(1,5841):
    videosQual[i] = 0
    videosNumber[i]= 0

print("db read completed")
text=read.read()
users=json.loads(text)

for user in users:
    for eval in user['evaluations']:
        videosNumber[eval['resource']['id']]+=1
        videosQual[eval['resource']['id']]= (videosQual[eval['resource']['id']]+ int(eval['resource']['evaluation'][0]['answer']['value']))/videosNumber[eval['resource']['id']]
print("json processing done")

for i in xrange(1,5841):
    if(videosQual[i]!=0):
        write.write("UPDATE VIDEO_QUALIFICATION SET QUALIFICATION="+str(videosQual[i])+", QUALIFICATION_AMOUNT="+str(videosNumber[i])+" WHERE VIDEO_ID="+str(i)+";\n")



write.close()
read.close()
cur.close()
