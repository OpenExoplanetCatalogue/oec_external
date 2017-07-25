#!python 
import urllib.request
import os
import xml.etree.ElementTree as ET 
import xmltools
import csv
#####################
# Exoplanet.eu
#####################
url_exoplaneteu = "http://exoplanet.eu/catalog/csv/"

def get():
    xmltools.ensure_empty_dir("tmp_data")
    urllib.request.urlretrieve (url_exoplaneteu, "tmp_data/exoplanet.eu_catalog.csv")

def tofl(s):
    'convert str to nicer str'
    try:
        f = float(s)
        return "%.6f"%f
    except:
        return ""

def parse():
    # delete old data
    xmltools.ensure_empty_dir("systems_exoplaneteu")

    # parse data into default xml format
    f = open("tmp_data/exoplanet.eu_catalog.csv")
    header = [x.strip() for x in f.readline()[1:].replace("# ", "").split(",")]
    reader = csv.reader(f)
    for line in reader:
        p = dict(zip(header, line))
        outputfilename = "systems_exoplaneteu/"+p["star_name"].strip()+".xml"
        if p["planet_status"] != "Confirmed":
            continue
        if os.path.exists(outputfilename):
            system = ET.parse(outputfilename).getroot()
            star = system.find(".//star")
        else:
            system = ET.Element("system")
            ET.SubElement(system, "name").text = p["star_name"].strip()
          
            # convert the right ascension to hh mm ss
            tempra = ""
            ra = float(p['ra'])
            hours = ra / 360 * 24
            tempra += "%.2i" % (hours)
            minutes = hours % 1 * 60
            tempra += " %.2i" % (minutes)
            seconds = minutes % 1 * 60
            tempra += " %.2i" % (round(seconds))
            ET.SubElement(system, "rightascension").text = tempra

            # convert declination to deg mm ss
            tempdec = ""
            dec = float(p['dec'])
            tempdec += "%+.2i" %(dec) 
            minutes = dec % 1 * 60
            tempdec += " %.2i" % (minutes)
            seconds = round(minutes % 1 * 60)
            tempdec+= " %.2i" % (seconds)
            ET.SubElement(system, "declination").text = tempdec

            ET.SubElement(system, "distance").text = p["star_distance"]
            star = ET.SubElement(system, "star")
            ET.SubElement(star, "name").text = p["star_name"].strip()
            ET.SubElement(star, "age").text = p["star_age"]
            ET.SubElement(star, "radius").text = p["star_radius"]
            ET.SubElement(star, "mass").text = p["star_mass"]
            ET.SubElement(star, "spectraltype").text = p["star_sp_type"]
            ET.SubElement(star, "temperature").text = p["star_teff"]
            ET.SubElement(star, "metallicity").text = p["star_metallicity"]

        planet = ET.SubElement(star, "planet")
        ET.SubElement(planet, "name").text = p["name"].strip()
        ET.SubElement(planet, "semimajoraxis", errorminus=p["semi_major_axis_error_min"], errorplus=p["semi_major_axis_error_max"]).text = p["semi_major_axis"]
        ET.SubElement(planet, "periastron", errorminus=p['omega_error_min'], errorplus=p['omega_error_max']).text = p["omega"]
        ET.SubElement(planet, "eccentricity", errorminus=p['eccentricity_error_min'], errorplus=p['eccentricity_error_max']).text = p["eccentricity"]
        ET.SubElement(planet, "longitude", errorminus=p['lambda_angle_error_min'], errorplus=p['lambda_angle_error_max']).text = p["lambda_angle"]
        ET.SubElement(planet, "inclination", errorminus=p['inclination_error_min'], errorplus=p['inclination_error_max']).text = p["inclination"]
        ET.SubElement(planet, "period", errorminus=tofl(p['orbital_period_error_min']), errorplus=tofl(p['orbital_period_error_max'])).text = p["orbital_period"]
        ET.SubElement(planet, "mass", errorminus=p['mass_error_min'], errorplus=p['mass_error_max']).text = p["mass"]
        ET.SubElement(planet, "radius", errorminus=p['radius_error_min'], errorplus=p['radius_error_max']).text = p["radius"]
        try:
            if float(p["radius"])>0.:
                ET.SubElement(planet, "istransiting").text = "1"
        except:
            pass
        if p["detection_type"]=="Radial Velocity":
            ET.SubElement(planet, "discoverymethod").text = "RV"
        elif p["detection_type"]=="Primary Transit":
            ET.SubElement(planet, "discoverymethod").text = "transit"
        elif p["detection_type"]=="Imaging":
            ET.SubElement(planet, "discoverymethod").text = "imaging"


        ET.SubElement(planet, "temperature").text = p["temp_measured"]
        # to match OEC 
        if p['detection_type'].find("radial") != -1:
            ET.SubElement(planet, "discoverymethod").text = "RV"
        elif p['detection_type'].find("imaging") != -1:
            ET.SubElement(planet, "discoverymethod").text = "imaging"
        elif p['detection_type'].find("transit") != -1:
            ET.SubElement(planet, "discoverymethod").text = "transit"
        ET.SubElement(planet, "discoveryyear").text = p["discovered"]
        ET.SubElement(planet, "lastupdate").text = p["updated"].replace("-","/")[2:]
        ET.SubElement(planet, "list").text = "Confirmed planets"
        ET.SubElement(planet, "description").text = "Data for this planet was imported from the exoplanet.eu database."

        # ET.SubElement(planet, "spinorbitalignment").text = p[""]

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        ET.ElementTree(system).write(outputfilename) 

if __name__=="__main__":
    get()
    parse()
