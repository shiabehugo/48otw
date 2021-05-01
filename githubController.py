import datetime
import requests
import json
from github import Github

config = None
with open("config.json", 'r') as file:
	config = json.loads(file.read())
	print("config file loaded")

def getFile(fileName):
	g = Github(config['token'])
	repo = g.get_user().get_repo(config['repo'])

	try:
		file_content = repo.get_contents(fileName)
		return file_content.decoded_content.decode()
	except:
		return None
		pass

def saveFile(fileName, fileContent):
	g = Github(config['token'])
	repo = g.get_user().get_repo(config['repo'])

	# create or update accordingly
	try:
		file = repo.get_contents(fileName)
		repo.update_file(fileName, f"update {fileName}", fileContent, file.sha)
	except:
		repo.create_file(fileName, f"create {fileName}", fileContent)
		pass

	return f"https://raw.githubusercontent.com/shiabehugo/{config['repo']}/master/{fileName}"

def deleteFile(fileName):
	g = Github(config['token'])
	repo = g.get_user().get_repo(config['repo'])

	try:
		file = repo.get_contents(fileName)
		repo.delete_file(fileName, f"delete {fileName}", file.sha)
	except:
		return False
		pass
	return True