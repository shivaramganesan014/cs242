import json

import os

def merge_JsonFiles(prefix, filename):
    result = list()
    for f1 in filename:
        with open(prefix+f1, 'r') as infile:
        	try:
        		result.extend(json.load(infile))
        	except:
        		print("error reading ",filename)
    with open('all_json.jsonl', 'w') as output_file:
        json.dump(result, output_file)

filenames = os.listdir("data/")
print (filenames)
merge_JsonFiles("data/", filenames);