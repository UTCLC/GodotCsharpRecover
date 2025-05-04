import os
import re

def replace(csdir, projdir):
	if (projdir.endswith("/")):
		projdir = projdir[:-1]
	if (csdir.endswith("/")):
		csdir = csdir[:-1]
	with (open(projdir + "/project.godot", mode="r+", encoding="utf-8") as f):
		replaced = re.sub(r'(PackedStringArray\()("[^"]+"),\s*("[^"]+")(\))', r'\1\2, "C#", \3\4', f.read())
		f.seek(0)
		f.write(replaced)
	for dirfile in os.listdir(csdir):
		path = os.path.join(csdir, dirfile)
		if (os.path.isfile(path)):
			with open(path, mode="r", encoding="utf-8") as f:
				found = False
				contents = f.read()
				contents = contents.replace("\n\t[Export(PropertyHint.None, \"\")]","").replace("[Nullable(1)] ","")
				search = re.search("\\[ScriptPath\\(\".*\"\\)\\]",contents)
				if (search):
					found = True
					targetdir = search.group().replace("[ScriptPath(\"","").replace("\")]","")
					print(f"Found {targetdir} in {path}")
					targetdir = targetdir.replace("res:/", projdir)
					contents = contents.replace(search.group(),"")
				else:
					found = False
					print(f"ScriptPath was not found in {path}")
				
				while True:
					search = re.search("\npublic class [\\s\\S]*? : ",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,"\npublic partial class "+result.replace("\npublic class ","").replace(" : ","")+" : ")
					else:
						break
				while True:
					search = re.search("\tpublic new class MethodName[\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\t")
					else:
						break
				while True:
					search = re.search("\tpublic new class PropertyName[\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\t")
					else:
						break
				while True:
					search = re.search("\tpublic new class SignalName[\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\t")
					else:
						break
				while True:
					search = re.search("\t\\[EditorBrowsable\\(EditorBrowsableState\\.Never\\)\\][\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\t")
					else:
						break
				while True:
					search = re.search("\t\\[EditorBrowsable\\(EditorBrowsableState\\.Never\\)\\][\\s\\S]*?\t\\}\n}",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,"}")
					else:
						break
				while True:
					search = re.search("\t\\[AsyncStateMachine\\(typeof\\(.*\\)\\)\\]\n\t[^ ]+",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,f"\t{result.split("\t")[-1].replace(" ","").replace("\t","")} async")
					else:
						break
				while True:
					search = re.search("\tprotected void EmitSignal[\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\t")
					else:
						break
				while True:
					search = re.search("\tprotected void EmitSignal[\\s\\S]*?\t\\}\n\n\\}",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,"}")
					else:
						break
				while True:
					search = re.search("\n\t[^ ]+ async Task [\\s\\S]*?return",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,result.replace("return","await"))
					else:
						break
				while True:
					search = re.search("\n\t[^ ]+ async GDTask [\\s\\S]*?return",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,result.replace("return","await"))
					else:
						break
				while True:
					search = re.search("\n\tpublic event [^ ]+EventHandler[\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
					if (search):
						result = search.group()[:-1]
						contents = contents.replace(result,"\n\t")
					else:
						break
				while True:
					search = re.search("\n\tprivate [^ ]+EventHandler backing_\\w+;",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,"")
					else:
						break
				# while True:
				# 	search = re.search("\t\\[StructLayout\\(.*\\)\\][\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
				# 	if (search):
				# 		result = search.group()[:-1]
				# 		contents = contents.replace(result,"\t")
				# 	else:
				# 		break
				# while True:
				# 	search = re.search("\t\\[CompilerGenerated\\][\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
				# 	if (search):
				# 		result = search.group()[:-1]
				# 		contents = contents.replace(result,"\t")
				# 	else:
				# 		break
				# while True:
				# 	search = re.search("\t\\[DebuggerHidden\\][\\s\\S]*?\t\\}\n\n\t[^\t]",contents)
				# 	if (search):
				# 		result = search.group()[:-1]
				# 		contents = contents.replace(result,"\t")
				# 	else:
				# 		break
				
				if (found):
					write(targetdir, contents)
				elif (dirfile.endswith(".csproj")):
					with (open(projdir + "/project.godot", mode="r", encoding="utf-8") as f):
						version = re.search('config\\/features=PackedStringArray\\("(.*)", "C#", "(.*)"\\)',f.read()).group(1)
					contents = contents.replace("<Project Sdk=\"Microsoft.NET.Sdk\">","<Project Sdk=\"Godot.NET.Sdk/"+version+"\">").replace("\n    <LangVersion>1</LangVersion>","").replace("netcoreapp8.0",".net8.0")
					search = re.search("<TargetFramework>.*<\\/TargetFramework>",contents)
					if (search):
						result = search.group()
						contents = contents.replace(result,"<TargetFramework>.net"+("8" if (int(version.split(".")[1])>=4 and int(version.split(".")[1])>=4) else "6")+".0</TargetFramework>")
					write(projdir + "/" + dirfile, contents)
				else:
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
				with open(path, mode="r", encoding="utf-8") as f:
					if (f.read() == "\n" or f.read() == ""):
						print(f"Found {path} in {projdir}")
						write(path, contents)
					else:
						print(f"Found {path} but it is not empty inside")
					break
		elif (os.path.isdir(path)):
			find(dirfilee, path, contents)


replace(input("CS files dir："),input("Project dir："))