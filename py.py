import subprocess, os, io, re
import githubController

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

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

albumMusicPath = "/media/pi/Untitled/music/static/" + input("- Enter album path with music files: ").replace('\\', '/')

if input("get song names? (y/n): ").lower() == 'y':
	os.chdir('getSongNames')
	subprocess.run(['python', 'py.py', albumMusicPath])
	os.chdir('..')

if input("get song urls? (y/n): ").lower() == 'y':
	os.chdir('getSongUrls')
	subprocess.run(['python', 'py.py', albumMusicPath])
	os.chdir('..')

print("- Enter artist name: ", end='')
artistName = input()
print("- Enter album name: ", end='')
albumName = input()

if input("save info to local repo? (y/n): ").lower() == 'y':

	# combine out files
	with open("getSongNames/out.txt", 'r') as f:
		names = f.read().splitlines()
	with open("getSongUrls/out.txt", 'r') as f:
		urls = f.read().splitlines()

	outputString = artistName + '\\' + albumName + '\n'
	urlToNameDict = {urls[i]: names[i] for i in range(len(urls))}
	urls = natural_sort(urls)
	for url in urls:
		outputString += urlToNameDict[url] + '\\' + url + '\n'
	# for pair in zip(names, urls):
		# outputString += pair[0] + '\\' + pair[1] + '\n'

	print(outputString)
	with open('out.txt', 'w') as output:
		output.write(outputString)

	# save to local repo
	print("- Enter album cover image url: ", end='')
	imageUrl = input()
	try:
		subprocess.run(["mkdir", f"{hostFolderName}/{NameToDirectoryName(artistName)}"], stdout=subprocess.DEVNULL)
	except:
		pass
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat", 'w+') as albumDat:
		albumDat.write(outputString)
	with open(f"{hostFolderName}/{NameToDirectoryName(artistName)}/albums.dat", 'a+') as albumsDat:
		albumsDat.write(f"{albumName}\\{datHost}/{hostFolderName}/{NameToDirectoryName(artistName)}/{NameToDirectoryName(albumName)}.dat\\{imageUrl}\n")

	with io.open(f"{hostFolderName}/artists.dat", mode='r', encoding='utf-8') as artistsFile:
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
	
subprocess.run(['git', 'restore', '.'])
subprocess.run(['git', 'clean', '-f'])
subprocess.run(['git', 'pull'])
