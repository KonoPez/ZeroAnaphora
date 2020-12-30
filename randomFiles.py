import random, glob, shutil, re

#seperates set of recipes into equally sized training and test sets

#get input and output directories from user
indir = input("In what directory are the recipes located?")
dirA = input("What is the name of the first split set (training set)?")
dirB = input("What is the name of the second split set (test set)?")

recipes = glob.glob(indir + "*.txt")
target = len(recipes)//2
setB = []

#add half the recipes in the input directory to a list
while len(recipes) > target:
    item = random.choice(recipes)
    recipes.remove(item)
    setB.append(item)

#copy half the recipes to the training directory and the other half to the test directory
for a in recipes:
    shutil.copyfile(a, dirA + re.search("/([A-Za-z0-9\-]+\.txt)",a).group(1))
for b in setB:
    shutil.copyfile(b, dirB + re.search("/([A-Za-z0-9\-]+\.txt)",b).group(1))