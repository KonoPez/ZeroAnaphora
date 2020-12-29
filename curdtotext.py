import xml.etree.ElementTree as ET
import re
import glob

#takes a recipe annotated in Carnegie Mellon's CURD markup language and prints out the orginal
#text of the recipe instructions, omitting ingredient list
def xmltotxt(xmlpath: str, dir: str):
    #parse the xml file at the given path
    recipe = ET.parse(xmlpath).iter()
    instructions = []

    #add every unique line that is not introducing a new ingredient to list instruction
    for line in recipe:
        if line.tag == "line" and not (line.findtext("originaltext") in instructions or "create_ing" in line.findtext("annotation")):
            instructions.append(line.findtext("originaltext"))

    #prints the unannotated instructions to a txt file in recipes folder
    txtpath = dir + re.search("/([A-Za-z0-9\-]+)\.rcp_tagged.xml",xmlpath).group(1) + ".txt"
    txt = open(txtpath,"x")
    for line in instructions:
        txt.write(line+"\n")

    txt.close()

#run this process on every xml file in the given indir and output them in the given outdir
indir = input("In what directory are the annotated recipes located?")
outdir = input("In what directory should the unannotated recipes be output?")

allfiles = glob.glob(indir + "*.xml")
for xml in allfiles:
    xmltotxt(xml,outdir)