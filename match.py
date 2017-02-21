import xml.etree.ElementTree as ET, urllib, gzip, io
import glob
import difflib
import html

class Cat(object):
    def __init__(self,path):
        self.path = path
        self.planets = {}
        self.systems = {}
        for f in glob.glob(path+"/*.xml"):
            c = ET.parse(f)
            for planet in c.findall(".//planet"):
                names = planet.findall("name")
                names_text = []
                for name in names:
                    self.planets[name.text] = names[0].text
            names = c.findall("./name")
            names_text = []
            for name in names:
                self.systems[name.text] = names[0].text
    def findnews(self,other):
        usnames = list(set(self.systems.values()))
        snew = []
        for usname in usnames:
            if usname not in other.systems:
                snew.append([usname,difflib.get_close_matches(usname,other.systems.keys())])
        return snew
    def findnew(self,other):
        unames = list(set(self.planets.values()))
        new = []
        for uname in unames:
            if uname not in other.planets:
                new.append([uname,difflib.get_close_matches(uname,other.planets.keys())])
        return new
    def getsystem(self,systemname):
        with open(self.path+"/"+systemname+".xml","r") as f:
            return f.read()



oec = Cat("systems_open_exoplanet_catalogue")
eeu = Cat("systems_exoplaneteu")

news = eeu.findnews(oec)


o = "<html><body>"
o += """ <form action=""> """
for i,n in enumerate(news):
    pn, ons = n
    o+="<h2>%03d/%03d &nbsp;&nbsp;&nbsp; "%(i+1,len(news))+pn+"</h2>"
    o+="<input type='radio' name='s%05d' value='ignore' checked>ignore<br/>\n" %i
    for j,on in enumerate(ons):
        o+="<input type='radio' name='s%05d' value='on%02d'>add name to oec:  %s<br/>\n" %(i,j,on)

    o+="<input type='radio' name='s%05d' value='addsystem'>add system to oec<br/>\n" %i
    o+="<pre style='margin-left: 3em;'>"+html.escape(eeu.getsystem(pn))+"</pre>\n"
o += "</form></body></html>"
    


print(o)
