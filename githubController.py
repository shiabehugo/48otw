import datetime
import requests
import json
from github import Github

githubRepo = "48otw"
githubToken = "9115eb126eb6c518e7748135bf73fda76564a785"

def getFile(fileName):
	g = Github(githubToken)
	repo = g.get_user().get_repo(githubRepo)

	try:
		file_content = repo.get_contents(fileName)
		return file_content.decoded_content.decode()
	except:
		return None
		pass

def saveFile(fileName, fileContent):
	g = Github(githubToken)
	repo = g.get_user().get_repo(githubRepo)

	# create or update accordingly
	try:
		file = repo.get_contents(fileName)
		repo.update_file(fileName, f"update {fileName}", fileContent, file.sha)
	except:
		repo.create_file(fileName, f"create {fileName}", fileContent)
		pass

	return f"https://raw.githubusercontent.com/shiabehugo/{githubRepo}/master/{fileName}"

def deleteFile(fileName):
	g = Github(githubToken)
	repo = g.get_user().get_repo(githubRepo)

	try:
		file = repo.get_contents(fileName)
		repo.delete_file(fileName, f"delete {fileName}", file.sha)
	except:
		return False
		pass
	return True