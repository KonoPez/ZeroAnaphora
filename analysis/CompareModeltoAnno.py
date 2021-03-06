import glob, re
#script to assess the accuracy of a model by comparing the candidates it outputs to candidates selected by a human annotator

falPos = 0 #lines incorrectly included as zero candidate
falNeg = 0 #lines incorrectly excluded from zero candidates
truPos = 0 #lines correctly identifed as zero candidate
truNeg = 0 #lines correctly excluded from zero candidates
totalLines = 0

def compareOneRecipe(filepath:str, direct:str, annodir:str):
    annoPos, annoNeg, modelPos = ([],[],[]) #lists of lines from recipe
    model = 0

    #read in zero candidates identified by model to modelPos
    txtpath = re.search("/([A-Za-z0-9\-]+)\..*txt",filepath).group(1)
    try:
        model = open(filepath,"r")
    except FileNotFoundError:
        return (0,0,0,0,0)
    for line in model:
        modelPos.append(line.strip())
    model.close()
    
    #add lines with zeros to annoPos and lines without to annoNeg based off annotations
    recipe = open(direct + txtpath + ".txt","r") #recipe
    anno = open(filepath,"r") #annotations for that recipe
    for line in anno:
       annoPos.append(line.strip())
    for line in recipe:
        if not line.strip() in annoPos:
            annoNeg.append(line.strip())
    recipe.close()
    anno.close()

    #count true positives and false negatives
    tPos, fNeg = (0,0)
    for zero in annoPos:
        if zero in modelPos:
            tPos += 1
        else:
            fNeg += 1
            print("FALSE NEG: "+ zero)

    #count true negatives and false positives
    tNeg, fPos = (0,0)
    for non in annoNeg:
        if non in modelPos:
            fPos += 1
            print("FALSE POS: "+ non)
        else:
            tNeg += 1
    
    #print results
    totLines = len(annoPos) + len(annoNeg)
    totCorrect = tPos+tNeg
    print("Correctly identified sentences: " + str(totCorrect) + "/" +str(totLines))
    print("False positives (of candidates identified): " + str(fPos) + "/" +str(len(modelPos)))
    print("False negatives (of lines excluded): " + str(fNeg) + "/" + str(totLines-len(modelPos))+"\n")
    return (fPos, fNeg, tPos, tNeg, totLines)


#get input directories from user
recipedir = input("In what directory are text recipes located?")
canddir = input("In what directory are the candidate sentences located? (the output of the model being assessed)")
annodir = input("In what directory are the annotated recipes located?")

annotations = glob.glob(annodir + "*.annotated.txt") #directory of annotated recipes

for x in annotations:
    print("In "+re.search("/([A-Za-z0-9\-]+)\..*txt",x).group(1))
    stats = compareOneRecipe(x, recipedir, annodir)
    falPos, falNeg, truPos, truNeg, totalLines = (falPos + stats[0], falNeg + stats[1], truPos + stats[2], truNeg + stats[3], totalLines + stats[4])

print("Totals:")
print("Correctly identified sentences: " + str(truPos+truNeg) + "/" +str(totalLines))
print("False positives/total pos/total: " + str(falPos) + "/" + str(falPos + truPos) + "/" + str(totalLines))
print("False negatives/total neg/total: " + str(falNeg) + "/" + str(falNeg + truNeg) + "/" + str(totalLines))