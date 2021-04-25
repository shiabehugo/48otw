import os
import re

def scanFolder(folder):
	return [i for i in os.listdir(folder) if i[-4:] == ".mp3" or i[-5:] == ".flac"]

def findStartingIndex(fileList):

	charsToCheck = min([len(x) for x in fileList])
	differentChars = [0 for j in range(charsToCheck)]

	for i in range(charsToCheck):
		alreadySeenChars = []
		for file in fileList:
			if file[i] not in alreadySeenChars:
				differentChars[i] += 1
				alreadySeenChars.append(file[i])

	startIndex = charsToCheck - 1
	while startIndex > -1 and differentChars[startIndex] != 1:
		startIndex -= 1
	return startIndex + 1


mypath = input("path: ")
endPattern = r"\.(mp3)|\.(flac)"

f = scanFolder(mypath)
startIndex = findStartingIndex(f)
userInput = input(f"start index ({startIndex}): ")
startIndex = int(userInput) if len(userInput) > 0 else startIndex

file = open("out.txt","w")
for fa in f:
	if not fa.endswith(".mp3") and not fa.endswith(".flac"):
		continue
	print(fa)
	me = re.finditer(endPattern, fa)

	start = 0
	end = 0
	for a in me:
		end = a.start()
		break

	res = fa[startIndex:end]
	print(res)
	file.write(res + "\n")
file.close()