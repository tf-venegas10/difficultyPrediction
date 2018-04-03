import MySQLdb
db = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="znrmxn5ahxiedok5",         # your username
                     passwd="cxkd6uou53ov3vzm", # your password
                    # port="3306",
                     db="uzzonr2rx4qx8zu4")
cur = db.cursor()

# Use all the SQL you like
#cur.execute("CREATE TABLE FEATURES ( id int(11) NOT NULL AUTO_INCREMENT, name  varchar(250) DEFAULT NULL, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  ")
#cur.execute("INSERT INTO FEATURES (name) VALUES('numeroPalabras')")
#cur.execute("INSERT INTO FEATURES (name) VALUES('nounPhrases')")
#cur.execute("INSERT INTO FEATURES (name) VALUES('numeroFrases')")
file= open("3-21-18-coursesequences.sql", "r")
dbQuery=file.read()
queries=dbQuery.split(";")
for q in queries:
    cur.execute(q+ ";")
cur.execute("SELECT * FROM learning_resources")
for row in cur.fetchall():
    print row[0]

db.close()
