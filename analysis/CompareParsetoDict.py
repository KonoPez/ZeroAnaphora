import re, glob, ZeroAnaphora, FrameDictionary

#compares Parsey McParseface to frame dictionary to recognize missing arguments as zero anaphora candidate
#see comments in FrameDictionary for more detail

#find the zero anpahora candidate sentences for a given file, print to a new file in given directory, and return number of candidates & sentences searched
def getZeroCandidates(txtpath: str, canddir: str, parsedir: str, frames: FrameDictionary, counts):
    candidates = []

    #read in parsed sentences
    parsepath = parsedir + re.search("/([A-Za-z0-9\-]+)\.txt",txtpath).group(1) + ".tweakedparse.txt"
    parsedict = ZeroAnaphora.getParseDict(parsepath)
    
    #for every sentence in the recipe
    for sentence in parsedict:
        parse = parsedict[sentence]
        verb = parse["output"][0]["tree"]["ROOT"][0]

        #if number of args for each verb in sentence is different from expected
        if not frames.checkArgCount(verb):
            candidates.append(sentence) #add as candidate
    
    #print candidates to file
    candpath = canddir + re.search("/([A-Za-z0-9\-]+)\.txt",txtpath).group(1) + ".candidates.txt"
    candwrite = open(candpath, "w")
    for x in candidates:
        candwrite.write(x+"\n")
    counts.write(candpath + "   " + str(len(candidates)) + "/" + str(len(parsedict)) + "\n")

    candwrite.close()
    return (len(parsedict),len(candidates))


#get input directories and output file from user
recipedir = input("In what directory are text recipes located?") #asked seperately from xml directory to allow the use of a subset of the full recipe set as training data, leaving other data for testing
parsedir = input("In what directory are the parsed recipes located? (filename should end with  \".tweakedparse.txt\")")
framefile = input("What file contains the frame dictionary? (probably a txt file)")  
outdir = input("In what directory should the candidates be printed?")
outfile = input("In what file should the results be output? (probably a txt file)")  

totalSens, totalCands= (0, 0)
recipedirectory = glob.glob(recipedir + "*.txt")
counts = open(outfile,"w")
frames = FrameDictionary.FrameDictionary(framefile)

for recipe in recipedirectory:
    sens, cands = getZeroCandidates(recipe, outdir, parsedir, frames, counts)
    totalSens += sens
    totalCands += cands
counts.write("\nTotal:  "+str(totalCands)+"/"+str(totalSens))
counts.close()
