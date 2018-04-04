
from textstat.textstat import textstat
import MySQLdb
import sys


db = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="znrmxn5ahxiedok5",         # your username
                     passwd="r8lkor9pav5ag5uz", # your password
                    # port="3306",
                     db="uzzonr2rx4qx8zu4")

curRead = db.cursor()
file=open("Automated_readability_index.sql","a")
curRead.execute("SELECT * FROM resource_content")
for row in curRead.fetchall():
    text= unicode(row[1],"utf-8",errors='ignore')
    try:
        value=textstat.automated_readability_index(text)
    except(UnicodeDecodeError):
         print "not read at id: "+str(row[0])
         #print row[1]
         value=0
    #curWrite.execute\
    file.write("INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (5, "+str(row[0])+", "+str(value)+" );\n")

file.close()

db.close()
