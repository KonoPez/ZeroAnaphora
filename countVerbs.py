import glob, re, ZeroAnaphora

#counts the number of times every verb is found in a given directory of txt files, given the directory in which those files have an existing tweaked parse
def getVerbCounts(filepath:str, verbCounts:dict, parsedir:str):
    parsepath = parsedir + re.search("/([A-Za-z0-9\-]+)\..*txt",filepath).group(1) + ".tweakedparse.txt"
    parseDict = ZeroAnaphora.getParseDict(parsepath) #dictionary of sentences in a recipe mapped to their parse
    candidates = open(filepath, "r") #file containing candidate sentences
    sentences = [] #list of candidate sentences

    #copy all candidate sentenceas from file into list
    for sen in candidates:
        sentences.append(sen.strip())
    
    #for every sentence in the list, find all the verbs it contains and add its counts to dictionary
    for sen in sentences:
        verbs = ZeroAnaphora.getVerbs(parseDict[sen]["output"][0]["tree"]["ROOT"][0])
        for verb in verbs:
            if verb in verbCounts:
                verbCounts[verb] = verbCounts[verb] + 1
            else:
                verbCounts[verb] = 1
    
    candidates.close()
    return verbCounts

#get input directories and output file from user
txtdir = input("In what directory are the text files located?")
parsedir = input("In what directory are the parsed recipes located? (filename should end with  \".tweakedparse.txt\")")
outfile = input("In what file should the results be output? (probably a txt file)")

directory = glob.glob(txtdir + "*.txt") #directory of files containing candidate sentences or all sentences from each recipe
verbCounts = {} #dictionary of verb types mapped to token counts
counts = open(outfile,"w") #file for data output

#add the counts in each recipe to the dictionary
for recipe in directory:
    verbCounts = getVerbCounts(recipe, verbCounts, parsedir)
verbCounts = {k: v for k, v in sorted(verbCounts.items(), key=lambda item: item[1])}

#print all the verb counts to output file
for verb in verbCounts:
    counts.write(verb + ":  "+str(verbCounts[verb])+"\n")

counts.close()