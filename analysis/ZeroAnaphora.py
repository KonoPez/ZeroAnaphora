#module containing functions reused across scripts to show I understand basic coding practices
import json
import re

COORDINATORS = ["conj","parataxis","xcomp"]
TRANSITIVES = ["combine","mix","separate","cut","cook","do","serve","leave","put","remove","set"]
LOCATIVE = ["put", "remove"]

#return dictionary of sentences in a recipe mapped to their parse
def getParseDict(parsepath:str):
    parses = []
    parsedict={}
    readparse = open(parsepath,"r")
    for x in readparse:
        parses.append(json.loads(x))
    for x in parses:
        parsedict[x["output"][0]["sentence"].strip()] = x
    
    readparse.close()
    return parsedict

#return a list of verb tokens found in sentence rooted by given verb
def getVerbs(verb):
    verbs = []
    verbs.append(verb["token"].lower())

    if "tree" in verb:
        for kid in verb["tree"]:
        #if sentence has multiple potential verbs, count all verbs
            if kid in COORDINATORS:
                for conj in verb["tree"][kid]:
                    verbs += getVerbs(conj)
    
    return verbs

#return true iff the given verb in a Parsey McParseface parse and every coordinate verb has a direct object (="dobj" dependency)
def checkForDobj(verb):
    hasDobj = False

    if "tree" in verb:
        for kid in verb["tree"]:
        #if verb has dobj, change out to true
            if kid == "dobj":
                hasDobj = True

        for kid in verb["tree"]:
        #if sentence has multiple potential verbs, make sure all verbs have dobj
            if kid in COORDINATORS:
                for conj in verb["tree"][kid]:
                    hasDobj = hasDobj and checkForDobj(conj)
    
    return hasDobj

#return true iff the given verb in a Parsey McParseface parse and every coordinate verb has a location (="prep" dependency)
def checkForLoc(verb):
    hasLoc = False

    if "tree" in verb:
        for kid in verb["tree"]:
        #if verb has preposition dependency, change out to true
            if kid == "prep":
                hasLoc = True

        for kid in verb["tree"]:
        #if sentence has multiple potential verbs, make sure all verbs have loc
            if kid in COORDINATORS:
                for conj in verb["tree"][kid]:
                    hasLoc = hasLoc and checkForLoc(conj)
    
    return hasLoc and checkForDobj(verb)