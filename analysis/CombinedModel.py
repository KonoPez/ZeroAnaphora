import xml.etree.ElementTree as ET
import re, glob, ZeroAnaphora, FrameDictionary

def getZeroCandidates(xmlpath: str, dir: str, frames:FrameDictionary, counts):
    candidates = []

    #read in xml file as a tree
    tree = ET.parse(xmlpath).iter()

    #read in parsed sentences
    parsepath = "./tweaked/" + re.search("/([A-Za-z0-9\-]+)\.rcp_tagged.xml",xmlpath).group(1) + ".tweakedparse.txt"
    parsedict = ZeroAnaphora.getParseDict(parsepath)
    
    #for every sentence-annotation pair
    for line in tree:
        if line.tag == "line" and re.search("([a-z]+)\(",line.findtext("annotation")).group(1) in ZeroAnaphora.TRANSITIVES:
            action = re.search("([a-z]+)\(",line.findtext("annotation")).group(1) #the action for the line in the CURD annotation
            sentence = line.findtext("originaltext").strip() #the sentence
            parse = parsedict[sentence]
            verb = parse["output"][0]["tree"]["ROOT"][0]
            add = not sentence in candidates

            #if the dictionary model says it has a zero pronoun, add it to candidates
            if add and not frames.checkArgCount(verb):
                candidates.append(sentence)
                add = False

            #if the dictionary model says no expected arguments are missing
            if add:
                #check to see if the sentence contains any verbs not registered in dictionary
                verbList = ZeroAnaphora.getVerbs(verb)
                missingVerb = False
                for token in verbList:
                    missingVerb = missingVerb or (frames.getArgCount(token) < 0)
            
                #if any of the verbs are not in the dictionary, compare parse to CURD annotations
                if missingVerb:
                    if action in ZeroAnaphora.LOCATIVE:
                     add = not ZeroAnaphora.checkForLoc(verb)
                    #if the annotation is a transitive action
                    elif action in ZeroAnaphora.TRANSITIVES:
                     add = not ZeroAnaphora.checkForDobj(verb)
                #if all verbs are in dictionary, do not add the sentence
                else:
                    add = False

            if add:
                candidates.append(sentence)
    
    #print candidates to file
    candpath = dir + re.search("/([A-Za-z0-9\-]+)\.rcp_tagged.xml",xmlpath).group(1) + ".candidates.txt"
    candwrite = open(candpath, "w")
    for x in candidates:
        candwrite.write(x+"\n")
    counts.write(candpath+"   "+str(len(candidates))+"/"+str(len(parsedict))+"\n")

    candwrite.close()
    return (len(parsedict),len(candidates))


xmldirectory = glob.glob("./annotated_recipes/*.xml")
totalSens, totalCands= (0, 0)
counts = open("combinedcandidatescounts.txt","w")
directory = "./combinedcandidates/"
frames = FrameDictionary.FrameDictionary("./frames50.txt")
for xml in xmldirectory:
    sens, cands = getZeroCandidates(xml,directory,frames,counts)
    totalSens += sens
    totalCands += cands
counts.write("\nTotal:  "+str(totalCands)+"/"+str(totalSens))
counts.close()