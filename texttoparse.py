import re, glob, requests, json

#parse the recipe at the given path and output the parse as a txt file in the given directory
def txttoparse(filepath: str, dir: str):
    #get output file name and check to see if parsed file already exists since parsing takes f o r e v e r
    outpath = dir + re.search("/([A-Za-z0-9\-]+)\.txt",filepath).group(1) + ".parsed.txt"
    try:
        txt = open(outpath,"x")
    except FileExistsError:
        print(filepath + " has already been parsed.")
        return

    #read in text of file
    recipe = parseFile(filepath)

    #prints the parsed instructions to a txt file in given directory
    for line in recipe:
        txt.write(json.dumps(line)+"\n")

    print("Parsed file: " + filepath)
    txt.close()

#for each sentence in the recipe at the given path, request a parse from Google's Parsey McParseface dependency parser
#return a sequential list of the parsed sentences in json format
def parseFile(filepath:str):
    source = open(filepath,"r")
    out = []
    for x in source:
        if x.strip():
            r = requests.post("https://api.deepai.org/api/parseymcparseface",
            data={
               'sentence': x,
            },
            headers={'api-key': 'ef45f03f-81bd-4ea2-80fb-3ea480b9ebb1'}
            )
            line = r.json()
            out.append(line)

            if "err" in line:
                errors.write("Error in " + filepath + "\n")
                print("Error in line: " + x.strip())
            else:
                print("Parsed line: " + x.strip())
    source.close()
    return out    

errors = open("parseErrors.txt","w") #file to which to write sentences that cause parse errors

#get input and output directories from user
indir = input("In what directory are the recipes located?")
outdir = input("In what directory should the parsed recipes be output?")

allfiles = glob.glob(indir + "*.txt")
for txt in allfiles:
    txttoparse(txt,outdir)

errors.close()