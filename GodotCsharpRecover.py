import os
import re

def replace(csdir, projdir):
	if (projdir.endswith("/")):
		projdir = projdir[:-1]
	for dirfile in os.listdir(csdir):
		path = os.path.join(csdir, dirfile)
		if (os.path.isfile(path)):
			with open(path, mode="r", encoding="utf-8") as f:
				contents = f.read()
				search = re.search("\\[ScriptPath\\(\".*\"\\)\\]",contents)
				if (search):
					targetdir = search.group().replace("[ScriptPath(\"","").replace("\")]","")
					print(f"Found {targetdir} in {path}")
					targetdir = targetdir.replace("res:/", projdir)
					write(targetdir, contents)
				else:
					print(f"ScriptPath was not found in {path}")
					find(dirfile, projdir, contents)
		elif (os.path.isdir(path)):
			replace(path, projdir)

def write(targetdir, contents):
	if (os.path.exists(targetdir)):
		print(f"Write in {targetdir}")
		with open(targetdir, mode="w", encoding="utf-8") as f:
			f.write(contents)
	else:
		print(f"Dir {targetdir} not exists")

def find(dirfilee, projdir, contents):
	for dirfile in os.listdir(projdir):
		path = os.path.join(projdir, dirfile)
		if (os.path.isfile(path)):
			if (dirfile == dirfilee):
				print(f"Found {path} in {projdir}")
				write(path, contents)
		elif (os.path.isdir(path)):
			find(dirfilee, path, contents)


replace(input("CS files dir："),input("Project dir："))