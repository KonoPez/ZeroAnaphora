import json, glob, re, ZeroAnaphora

#script to fix consistent and easily repairable parse errors in Parsey McParse output
#currently only corrects a specific error in which temporal modifiers are recognized as the direct object of a verb
#this occurs in sentences like "Bake fifteen minutes." The word "for" is elided where it is normally recquired, causing this error

TIME_HEADS = ["minutes","minute","seconds","second","hours","hour"] #possible heads of temporal NP as dobj error

#read in the parsed sentences in the txt file at the given path and return them in a sequential list
def getParse(filepath:str):
    #open txt file at filepath, containing parsed recipe
    parse = open(filepath, "r")
    out=[]
    
    #read in all the parsed lines and add to list to be returned
    for line in parse:
        out.append(json.loads(line))
    
    parse.close()
    return out

#search for known errors at given verb in a parse and correct them 
def tweak(verb):
    #maps the erroneous key to the key it should be replaced by
    keyswaps={}

    if "tree" in verb:
        for kid in verb["tree"]:
        #recursively tweak potential conjunct verbs as with the root
            if kid in ZeroAnaphora.COORDINATORS:
                for conj in verb["tree"][kid]:
                    tweak(conj)
        #fix issue where periods of time are parsed as dobj
            elif kid == "dobj":
                if verb["tree"]["dobj"][0]["token"] in TIME_HEADS:
                    keyswaps["dobj"] = "advmod"

    #make the tweaks recognized above
    for swap in keyswaps:
        verb["tree"][keyswaps[swap]] = verb["tree"].pop(swap)

#go thru every sentence in the parsed recipe contained by the txt file at the given path and fix known errors
def tweakFile(filepath:str,dir:str):
    parse = getParse(filepath)
    for line in parse:
        #tweak the root of the sentence
        tweak(line["output"][0]["tree"]["ROOT"][0])
    
    tweakpath = dir + re.search("/([A-Za-z0-9\-]+)\.parsed.txt",filepath).group(1) + ".tweakedparse.txt"
    newparse = open(tweakpath,"w")
    for line in parse:
        newparse.write(json.dumps(line)+"\n")
    
    newparse.close()


#get input and output directories from user
indir = input("In what directory are the parsed recipes located?")
outdir = input("In what directory should the tweaked parses be output?")

allfiles = glob.glob(indir + "*.txt")
for txt in allfiles:
    tweakFile(txt, outdir)
