import xml.etree.ElementTree as ET, urllib, gzip, io
import glob
import difflib
import html

class Sys(object):
    def __init__(self,pn,n,lu):
        self.pn = pn
        self.n = n
        self.lu = lu

class Cat(object):
    def __init__(self,path):
        self.path = path
        self.planets = {}
        self.systems = []
        self.lastupdate = {}
        for f in glob.glob(path+"/*.xml"):
            c = ET.parse(f)
            for planet in c.findall(".//planet"):
                names = planet.findall("name")
                names_text = []
                for name in names:
                    self.planets[name.text] = names[0].text
            names = c.findall("./name")
            names_text = []
            try:
                lu = c.find(".//lastupdate").text
            except:
                lu = ""
            for name in names:
                self.systems.append(Sys(names[0].text,name.text,lu))
    def findnews(self,other):
        usnames = list(set([s.pn for s in self.systems]))
        othernames = [s.n for s in other.systems]
        snew = []
        for usname in usnames:
            if usname not in othernames:
                snew.append([usname,difflib.get_close_matches(usname,othernames)])

        return snew
    def getsystem(self,systemname):
        with open(self.path+"/"+systemname+".xml","r") as f:
            return f.read()



oec = Cat("systems_open_exoplanet_catalogue")
eeu = Cat("systems_exoplaneteu")

news = eeu.findnews(oec)

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    o = "<html><body>"
    o += """ <form action="./update"  method="post">   <input type="submit" value="Submit"> """
    for i,n in enumerate(news):
        pn, ons = n
        o+="<h2>%03d/%03d &nbsp;&nbsp;&nbsp; "%(i+1,len(news))+pn+"</h2>"
        o+="<input type='radio' name='s%05d' value='ignore' checked>ignore<br/>\n" %i
        for j,on in enumerate(ons):
            o+="<input type='radio' name='s%05d' value='on%02d'>add name to oec:  %s<br/>\n" %(i,j,on)

        o+="<input type='radio' name='s%05d' value='addsystem'>add system to oec<br/>\n" %i
        o+="<pre style='margin-left: 3em;'>"+html.escape(eeu.getsystem(pn))+"</pre>\n"
    o += "</form></body></html>"
    return o


@app.route('/update', methods=['POST'])
def login():
    o = ""
    for i,n in enumerate(news):
        o+= "%d  "%i + request.form['s%05d'%i] + "<br/>"
    return o

if __name__ == "__main__":
    app.run()
