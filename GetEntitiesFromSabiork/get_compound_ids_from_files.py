import glob
import json

file_names = glob.glob("./JsonEntries/*.json")


# turns a json tree into a list of key-value pairs
def flatten_json( j ):

    print("not done, yet")
    exit()

    return list()

for file_name in file_names:



    f = open(file_name)

    entry_json = print(json.load(f))

    f.close()

    l = flatten_json(entry_json)

    exit()


