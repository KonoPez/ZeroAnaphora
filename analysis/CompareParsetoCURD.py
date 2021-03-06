import xml.etree.ElementTree as ET
import re, glob, ZeroAnaphora

#identifies which sentences in each recipe are zero anaphora candidates by comparing the CURD annotations to the Parsey McParseface parse
#sentences identified as candidates are printed to a .candidates.txt file in a directory given by user
#candidates are identifed by checking the parse for a direct object for each verb if a sentence if the CURD annotation expects one
#if the CURD annotations for a sentence expect a location (put or remove), verbs are also checked for prepositional dependencies
#additionally prints a txt file with the number of sentences identified in each recipe and in the whole directory

def getZeroCandidates(xmlpath: str, outdir: str, parsedir: str, counts):
    candidates = []

    #read in xml file as a tree
    tree = ET.parse(xmlpath).iter()

    #read in parsed sentences
    parsepath = parsedir + re.search("/([A-Za-z0-9\-]+)\.rcp_tagged.xml",xmlpath).group(1) + ".tweakedparse.txt"
    parsedict = ZeroAnaphora.getParseDict(parsepath)
    
    #for every sentence-annotation pair
    for line in tree:
        if line.tag == "line" and re.search("([a-z]+)\(",line.findtext("annotation")).group(1) in ZeroAnaphora.TRANSITIVES:
            action = re.search("([a-z]+)\(",line.findtext("annotation")).group(1) #the action for the line in the CURD annotation
            sentence = line.findtext("originaltext").strip() #the sentence
            add = not sentence in candidates
            parse = parsedict[sentence]
            verb = parse["output"][0]["tree"]["ROOT"][0]

            if add and action in ZeroAnaphora.LOCATIVE:
                add = not ZeroAnaphora.checkForLoc(verb)
            #if the annotation is a transitive action
            elif add and action in ZeroAnaphora.TRANSITIVES:
                add = not ZeroAnaphora.checkForDobj(verb)

            if add:
                candidates.append(sentence)
    
    #print candidates to file
    candpath = outdir + re.search("/([A-Za-z0-9\-]+)\.rcp_tagged.xml",xmlpath).group(1) + ".candidates.txt"
    candwrite = open(candpath, "w")
    for x in candidates:
        candwrite.write(x+"\n")
    counts.write(candpath+"   "+str(len(candidates))+"/"+str(len(parsedict))+"\n")

    candwrite.close()
    return (len(parsedict),len(candidates))

#get input directories and output file from user
recipedir = input("In what directory are text recipes located?") #asked seperately from xml directory to allow the use of a subset of the full recipe set as training data, leaving other data for testing
xmldir = input("In what directory are the CURD annotated recipes located?")
parsedir = input("In what directory are the parsed recipes located? (filename should end with  \".tweakedparse.txt\")")
outdir = input("In what directory should the candidates be printed?")
outfile = input("In what file should the results be output? (probably a txt file)")   

txtdirectory = glob.glob(recipedir + "*.txt")
totalSens, totalCands= (0, 0)
counts = open(outfile,"w")

for recipe in txtdirectory:
    xml = xmldir + re.search("/([A-Za-z0-9\-]+)\.txt",recipe).group(1) + ".rcp_tagged.xml"
    sens, cands = getZeroCandidates(xml, outdir, parsedir, counts)
    totalSens += sens
    totalCands += cands

counts.write("\nTotal:  "+str(totalCands)+"/"+str(totalSens))
counts.close()