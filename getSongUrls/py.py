import os
import re
import sys

def scanFolder(folder):
	return [i for i in os.listdir(folder) if i[-4:] == ".mp3" or i[-5:] == ".flac"]


if len(sys.argv) > 1:
	mypath = sys.argv[1]
else:
	mypath = input("path: ")
endPattern = r"\.(mp3)|\.(flac)"

f = scanFolder(mypath)
# print(f)
# input()
pathRoot = "/media/pi/Untitled/music/static/"
with open("out.txt", "w") as outFile:
	outFile.write("\n".join([f"{mypath.replace(pathRoot, '')}/{x}" for x in f]))

# file = open("out.txt","w")
# for fa in f:
# 	if not fa.endswith(".mp3") and not fa.endswith(".flac"):
# 		continue
# 	print(fa)
# 	me = re.finditer(endPattern, fa)

# 	start = 0
# 	end = 0
# 	for a in me:
# 		end = a.start()
# 		break

# 	res = fa[startIndex:end]
# 	print(res)
# 	file.write(res + "\n")
# file.close()