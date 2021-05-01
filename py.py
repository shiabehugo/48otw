import subprocess, os
import githubController

datHost = 'https://raw.githubusercontent.com/shiabehugo/48otw/master'
hostFolderName = 'data'

def NameToDirectoryName(name):
	out = ''
	availableCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	for char in name:
		if char in availableCharacters:
			out += char
		elif char == ' ':
			out += '_'
	return out

if input("get song names? (y/n): ").lower() == 'y':
	os.chdir('getSongNames')
	subprocess.run(['python', 'py.py'])
	os.chdir('..')

if input("get drive links from html? (y/n): ").lower() == 'y':
	os.chdir('googleDrive')
	subprocess.run(['python', 'py.py'])
	os.chdir('..')

print("- Enter artist name: ", end='')
artistName = input()
print("- Enter album name: ", end='')
albumName = input()

if input("save info to local repo? (y/n): ").lower() == 'y':

	# combine out files
	with open("getSongNames/out.txt", 'r') as f:
		names = f.read().splitlines()
	with open("googleDrive/out.txt", 'r') as f:
		urls = f.read().splitlines()

	outputString = artistName + '\\' + albumName + '\n'
	for pair in zip(names, urls):
		outputString += pair[0] + '\\' + pair[1] + '\n'

	print(outputString)
	with open('out.txt', 'w') as output:
		output.write(outputString)

	# save to local repo
	print("- Enter album cover image url: ", end='')
	imageUrl = input()
	subprocess.run(["mkdir", f"{hostFolderName}/{NameToDirectoryName(artistName)}"], stdout=subprocess.DEVNULL)
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat", 'w+') as albumDat:
		albumDat.write(outputString)
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat", 'a+') as albumsDat:
		albumsDat.write(f"{albumName}\\{datHost}/{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat\\{imageUrl}\n")

	with open(f"{hostFolderName}/artists.dat", 'r') as artistsFile:
		lines = [x for x in artistsFile.read().split('\n') if len(x) > 0]
		artistNames = [x[:x.find('\\')] for x in lines]
		name2DatLine = {}
		for i in range(len(lines)):
			name2DatLine[artistNames[i]] = lines[i]
		name2DatLine[artistName] = f"{artistName}\\{datHost}/{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat"
		if artistName not in artistNames:
			artistNames.append(artistName)

		artistNames.sort()
		newFileContents = ""
		for name in artistNames:
			newFileContents += name2DatLine[name] + '\n'
	with open(f"{hostFolderName}/artists.dat", 'w') as artistsFile:
		artistsFile.write(newFileContents)

if input("upload to github? (y/n): ").lower() == 'y':

	# upload from local version
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat", 'r') as file:
		githubController.saveFile(f"{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat", file.read())
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat", 'r') as file:
		githubController.saveFile(f"{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat", file.read())
	with open(f"{hostFolderName}/artists.dat", 'r') as file:
		githubController.saveFile(f"{hostFolderName}/artists.dat", file.read())

	# upload directly
	# githubController.saveFile(f"{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat", outputString)
	# albumsDat = githubController.getFile(f"{NameToDirectoryName(artistName)}/albums.dat")
	# if albumsDat != None:
	# 	albumsDat += f"{albumName}\\{datHost}{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat\n"
	# else
	# 	albumDat = f"{albumName}\\{datHost}{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat\n"
	# githubController.saveFile(f"{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat", albumsDat)