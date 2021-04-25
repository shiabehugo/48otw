import os
import re
import shutil

def listMusicFiles(folder):
	return [i for i in os.listdir(folder) if i[-4:] == ".mp3" or i[-5:] == ".flac"]

def listSubFolders(folder):
	return [x[0] for x in os.walk(directory)][1:]

directory = input("Enter folder: ")
directory = directory[:-1] if directory[-1] == '/' or directory[-1] == '\\' else directory

subfolders = listSubFolders(directory)

# move first folder files
firstFolderFiles = listMusicFiles(subfolders[0])
for file in firstFolderFiles:
	shutil.move(f"{subfolders[0]}/{file}", f"{directory}/{file}")
lastNumber = int(re.findall(r'^([0-9]+)', firstFolderFiles[-1])[0])

for folder in subfolders[1:]:

	folderFiles = listMusicFiles(folder)
	for file in folderFiles:
		fileNumber = int(re.findall(r'^([0-9]+)', file)[0])
		newNumber = lastNumber + fileNumber
		targetFile = re.sub(r'^([0-9]+)', f"{newNumber:02d}", file)

		shutil.move(f"{folder}/{file}", f"{directory}/{targetFile}")

	lastNumber += int(re.findall(r'^([0-9]+)', folderFiles[-1])[0])