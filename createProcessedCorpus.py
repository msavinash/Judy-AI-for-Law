import csv
import os
from preProcessor import preProcess

FOLDER = "dataset"
NEW_FOLDER = "dataset2"


# LOGFILE = "log.txt"



def getFilesRecursive(folder):
	# folder = rewritePath(folder)
	files = []
	for root,d_names,f_names in os.walk(folder):
		files.extend(list(map(lambda x:os.path.join(root, x), f_names)))
	return files


def storeData(data, path, fileName):
	# print(path)
	path = path.replace(FOLDER, NEW_FOLDER)
	# print(path)
	# path = os.path.join(NEW_FOLDER, fileName)
	try:
		os.makedirs(path)
	except FileExistsError:
		pass
	# print(data)
	with open(os.path.join(path, fileName), "w") as f:
		f.write("\n".join(data))

files = getFilesRecursive(FOLDER)

# print(files[0])
skippedCount = 0
skippedFiles = []
for file in files:
	print(file)
	lines = None
	with open(file, "r") as f:
		lines = f.readlines()
	processedData = []
	for line in lines:
		tokens = preProcess(line)
		# print(tokens)
		# print(tmpParts[:-1])
		processedLine = " ".join(tokens)
		processedData.append(processedLine)
	tmpParts = file.split("\\")
	path = os.path.join(*tmpParts[:-1])
	fileName = tmpParts[-1]
	storeData(processedData, path, fileName)
	# with open(LOGFILE, "w") as f:
	# 	f.writelines([str(skippedCount)] + skippedFiles)

