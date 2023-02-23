import re

regex = 'data-id="([0-9A-Za-z_-]*)"'
file = open("driveElement.txt", "r")
content = file.read()

elements = re.findall(regex, content)

print("found {} elements".format(len(elements)))
file = open("out.txt","w")
for element in elements:
	file.write("https://drive.google.com/uc?export=download&id={}\n".format(element))
file.close()
