import MySQLdb
from textblob import TextBlob
import sys
import unicodedata

reload(sys)
sys.setdefaultencoding('utf8')

db = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="znrmxn5ahxiedok5",         # your username
                     passwd="r8lkor9pav5ag5uz", # your password
                    # port="3306",
                     db="uzzonr2rx4qx8zu4")
dbWrite= MySQLdb.connect(host="l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="gh7u6wguchfrkxo1",         # your username
                     passwd="lqgvsrxvaeyb8uql", # your password
                    # port="3306",
                     db="n501u8qclhvj0mdv")
curRead = db.cursor()
curWrite= dbWrite.cursor()
# Use all the SQL you like
#curWrite.execute("CREATE TABLE FEATURES_PER_VIDEO ( id int(11) NOT NULL AUTO_INCREMENT, feature_id int(11), video_id int(11), value REAL(8,3), PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  ")
#curWrite.execute("CREATE TABLE FEATURES( id int(11) NOT NULL AUTO_INCREMENT, name VARCHAR(255), PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  ")

#cur.execute("DELETE FROM FEATURES WHERE name='numeroPalabras'")
#curWrite.execute("INSERT INTO FEATURES (name) VALUES('numeroPalabras');")
#curWrite.execute("INSERT INTO FEATURES (name) VALUES('nounPhrases');")
#curWrite.execute("INSERT INTO FEATURES (name) VALUES('numeroFrases');")
#file= open("3-21-18-coursesequences.sql", "r")
#dbQuery=file.read()
#queries=dbQuery.split(";")
#for q in queries:
#    cur.execute(q+ ";")
#cur.execute("SELECT * from INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE '%wild%';")


# i=1
file=open("nounPhrases.sql","a")
curRead.execute("SELECT * FROM resource_content")
for row in curRead.fetchall():
    text= unicode(row[1],"utf-8",errors='ignore')
    try:
        blob = TextBlob(text)
        value=len(blob.noun_phrases)
    except(UnicodeDecodeError):
         print "not read at id: "+str(row[0])
         #print row[1]
         value=0
    #curWrite.execute\
    file.write("INSERT INTO FEATURES_PER_VIDEO (feature_id, video_id, value) VALUES (3, "+str(row[0])+", "+str(value)+" );\n")

file.close()
# curWrite.execute("SELECT * FROM FEATURES;")
# for row in curWrite.fetchall():
#     print(row)
# db.close()
dbWrite.close()
