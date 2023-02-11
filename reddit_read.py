import json
import os

dir = "data/"
files = os.listdir(dir)
print (files)

for file in files:
	try:
		fileName = dir+file
		f = open(fileName)
		data = json.load(f)
		print(file+" read successfully")
	except Exception as e:
		print("error in reading ::"+ file)
		print (e)


# for(file in files):
# 	f = open(file)
# 	data = json.load(f)
# 	print(file+" read successfully")





