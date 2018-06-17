import MySQLdb
import os

dbcomplete = MySQLdb.connect(host="qbct6vwi8q648mrn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                             # your host, usually localhost
                             user="znrmxn5ahxiedok5",  # your username
                             passwd="r8lkor9pav5ag5uz",  # your password
                             # port="3306",
                             db="uzzonr2rx4qx8zu4")

curcomplete = dbcomplete.cursor()

curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (8,'VIDEO_PHRASES_COUNT')")
curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (9,'VIDEO_WORDS_COUNT')")
curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (10,'VIDEO_DIFFICULT_WORDS')")
curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (11,'EASY_VIDEO_READ')")
curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (12,'AUTOMATED_VIDEO_READABILITY_INDEX')")
curcomplete.execute("INSERT INTO FEATURES (ID,NAME) VALUES (13,'FLESCH_KINCAID_VIDEO_GRADE')")

ospath = os.path.dirname(__file__) + '/featureCalculation'

for subdir, dirs, files in os.walk(ospath):
    for file in files:
        if file.endswith(".sql") and file.lower().__contains__('video'):
            queries = open(ospath + '/' + file, 'r')
            lines = "".join(queries.readlines())
            print(lines)
            curcomplete.execute(lines)
            queries.close()

dbcomplete.close()
