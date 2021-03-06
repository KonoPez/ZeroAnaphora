#class to create a FrameDictionary object which primarily maps verb tokens to how many dependencies they are supposed to have;
#transitive verbs (=expect a direct object) are mapped to 1, locative verbs (=expect dirobj + prepositional phrase) are mapped to 2
#intransitive verbs (very uncommon in recipes) would be mapped to 0
import ZeroAnaphora, re

class FrameDictionary:
    argDictionary = {} #dictionary object mapping verbs to number of arguments expected

    def __init__(self, txtpath:str):
        self.setDict(txtpath)

    #return the number of expected arguments mapped to a given verb token, here defaulting to 1 if not otherwise specifed
    #defaulting to 1 is somewhat more accurate overall than defaulting to 0, but results in a lot more false positives in zero anaphora identification
    def getArgCount(self, token:str):
        return self.argDictionary.get(token, 1)

    #read in a frame dicitionary from a txt file at the given path; the format for this file is verb then argument number seperated by a single character
    def setDict(self, txtpath:str):
        newDict = {}
        txtfile = open(txtpath)
        for line in txtfile:
            data = re.search("([a-z]+).([0-9]+)",line)
            newDict[data.group(1)] = int(data.group(2))
        
        self.argDictionary = newDict
        txtfile.close()

    #returns true iff the given verb in a parse has the correct number of arguments according to self's argDictionary
    def checkArgCount(self, verb):
        argsCount = 0
        argsExpected = self.getArgCount(verb["token"].lower())
        match = True

        if (argsExpected > 0) and "tree" in verb:

            #if verb has dobj, increase argCount
            if "dobj" in verb["tree"]:
                argsCount += 1
        
            if argsExpected == 2 and "prep" in verb["tree"]:
                argsCount += 1
            
            for coord in ZeroAnaphora.COORDINATORS:
            #if sentence has multiple potential verbs, make sure all verbs have loc
                if coord in verb["tree"]:
                    for conj in verb["tree"][coord]:
                        match = match and self.checkArgCount(conj)
        
        return match and (argsCount == argsExpected or argsExpected == -1)