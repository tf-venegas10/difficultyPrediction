import json
import MySQLdb

write=open("Concepts.sql","w")
read=open("./../initialData/evaluations.json","r")
read2=open("./../initialData/evaluations_phase2.json","r")
read3=open("./../initialData/evaluations_new.json","r")
concepts=[]
allExsiting={}


for i in xrange(0,5841):
    concepts.append({})

text=read.read()
users=json.loads(text)
for user in users:
    for eval in user['evaluations']:
        for concept in eval['concepts']:
            concepts[eval['resource']['id']][concept['uri']]=1
            allExsiting[concept['uri']]=1

text=read2.read()
users=json.loads(text)
for user in users:
    for eval in user['evaluations']:
        for concept in eval['concepts']:
            concepts[eval['resource']['id']][concept['uri']]=1
            allExsiting[concept['uri']]=1
text=read3.read()
users=json.loads(text)
for user in users:
    for eval in user['evaluations']:
        for concept in eval['topics']:
            concepts[eval['videoId']][concept['value']]=1
            allExsiting[concept['value']]=1
i=100
for key in allExsiting.keys():
    write.write("INSERT INTO FEATURES (ID,NAME) VALUES ("+str(i)+",'"+key+"');\n")
    allExsiting[key]=i
    i+=1
v=0
real=0
print(len(concepts))
for video in concepts:
    if v==0 or video=={}:
        pass
    else:
        real+=1
        print(real)
        for key in allExsiting.keys():
            if (key in video):
                write.write(  "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES ("+str(allExsiting[key])+", " + str(v) + ",1 );\n")
            else:
                write.write(  "INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES ("+str(allExsiting[key])+", " + str(v) + ",0 );\n")
        print(len(allExsiting.keys()))
    v+=1


write.close()
read.close()


