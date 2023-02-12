import os

import json


path = "/home/cs242/ir_combined_data/"
filenames = os.listdir(path)

print(filenames)

new_data = dict()
for file_name in filenames:
	print(file_name)
	with open(path+file_name, "r+") as file:
		try:
			file_data = json.load(file)
			new_data[file_name.split('.')[0]] = file_data
		except:
			print("error while reading ", file_name)

with open('shiva.jsonl', 'w') as output_file:
    json.dump(new_data, output_file)