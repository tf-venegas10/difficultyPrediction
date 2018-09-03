import MySQLdb
import re
import os

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="tomasmarica",  # your password
                     # port="3306",
                     db="dajee")

ids = {}

curcomplete = db.cursor()
curcomplete.execute("SELECT * FROM learning_resources;")
for row in curcomplete.fetchall():
    path = row[2].replace(
        "/Users/rubenmanrique/Dropbox/DoctoradoAndes/Investigacion/Course Sequences Dataset/CourseraTexto/",
        "C:/Tesis ISIS/videosLu/Coursera/").replace("/Users/rubenmanrique/Downloads/CourseraTexto/",
                                                    "C:/Tesis ISIS/videosLu/Coursera/")
    name = re.sub(r'\.((t(x(t)?)?)|(e(n)?)|(s(r(t)?)?))(\.(t(x(t)?)?)?)?', '.mp4', path)
    ids[name] = str(int(row[0]))

ospath = os.path.dirname(__file__)
rootdir = "C:/Tesis ISIS/videosLu/Coursera"
export = open(ospath + 'path_updates.sql', 'w')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        vid_path = os.path.join(subdir, file)
        # vid_path = (ospath + "/InitialData/01_how-can-i-succeed-in-this-course.mp4")  # .replace("/", "\\")
        # print(img_path)
        # print(vid_path)
        if file.endswith(".mp4"):
            route = os.path.join(subdir, file)
            name = route.replace("\\", "/")#.replace("'", "\'")
            print(name)
            for key in ids.keys():
                if name.startswith(key):
                    export.write('UPDATE learning_resources SET path="' + name + '"WHERE id=' + ids[key] + ';\n')
                    print("INSERTED " + name)

db.close()
