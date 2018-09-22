import pymysql
import re
import os
from pycaption import *

db = pymysql.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

ids = {}

curcomplete = db.cursor()
curcomplete.execute("SELECT * FROM learning_resources;")
converter = CaptionConverter()
for row in curcomplete.fetchall():
    path = row[2]
    if ("ruben" not in path):

        path=path.replace(".mp4", ".en.srt")
        try:
            try:
                f=open(path, "r")
                file =f.read()
            except:
                path=path.replace(".en.srt", ".srt")
                f = open(path, "r")
                file = f.read()
        except:
            print("not found at: "+str(row[0]))
        try:
            converter.read(file.replace("1\r","1").replace("\n1\n","1\n"),SRTReader())
            writeFile=open(path.replace(".en.srt",".vtt").replace(".srt",".vtt"),"w+")
            writeFile.write(converter.write(WebVTTWriter()))
        except:
            #print(file.replace("1\r","1").replace("\n1\n","1\n"))
            print("Aqui si ni idea : "+str(row[0]))


        #print(converter.write(WebVTTWriter()))
        f.close()
        writeFile.close()


