import glob
import json

from jsonpath_ng import jsonpath, parse

file_names = glob.glob("./JsonEntries/*.json")


# turns a json tree into a list of key-value pairs
def flatten_json( j ):
    # print(j)
    jsonpath_expression = parse('sbml.model.listOfSpecies.species[*].@name')

    print(jsonpath_expression)

    match = jsonpath_expression.find( j )

    return [m.value for m in match]



    # return match[0].value

for file_name in file_names:
    f = open(file_name)

    entry_json = json.load(f)

    f.close()

    l = flatten_json(entry_json)

    print(l)

    exit()


