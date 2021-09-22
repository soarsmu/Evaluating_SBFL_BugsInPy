import os                                                                                                             
import csv
from pathlib import Path
import math
from scipy.stats import rankdata
import sys

def list_files(dir):                                                                                                  
	r = []                                                                                                            
	subdirs = [x[0] for x in os.walk(dir)]                                                                            
	for subdir in subdirs:                                                                                     
		files = os.walk(subdir).__next__()[2]                                                                             
		if (len(files) > 0):   
			if "bug_patch.txt" in files:                                                                                       
				r.append(os.path.join(subdir, "bug_patch.txt"))                                                                         
	return r   
cwd = os.getcwd()
all_files = list_files(cwd)


modified = dict()
for file in all_files:
	arr_file = file.split("/")
	project = arr_file[-4]
	number = arr_file[-2]

	text_file = open(file, "r")
	lines = text_file.readlines()
	text_file.close()

	file_temp = file.replace("bug_patch.txt","bug.info")
	text_file_2 = open(file_temp, "r")
	lines_info = text_file_2.readlines()

	text_file_2.close()
	fix_array = lines_info[-2].rstrip().split('"')
	fix_array.pop(-1)
	fix_commit = fix_array[-1]

	test_array = lines_info[-1].rstrip().split('"')
	test_array.pop(-1)
	test_array = test_array[-1].split(";")
	print(test_array)

	i = 0
	file_mod = dict()

	bug = []
	bug_only_plus = []
	one = 0
	while i < len(lines):
		if "diff" in lines[i][:4]:
			name_file = lines[i].split("/")[-1].rstrip()
			bug = []
			bug_only_plus = []
			i += 1
			while i < len(lines) and "diff" not in lines[i][:4]:
				if "@@" in lines[i][:4]:
					temp = lines[i][4:]
					start = int(temp.split(",")[0])
					i += 1
					while i < len(lines) and "@@" not in lines[i][:4] and "diff" not in lines[i][:4]:
						if lines[i][0] == "+":
							temp2 = start - 1
							if temp2 in bug_only_plus:
								pass;
							else:
								if temp2 not in bug and temp2 not in bug_only_plus:
									bug_only_plus.append(start)
						elif lines[i][0] == "-":
							bug.append(start)
							start += 1
						else:
							start += 1
						i += 1
				else:
					i += 1
					if ("test_" not in name_file and "_test" not in name_file and "tests_" not in name_file and "_tests" not in name_file) or (project=="pandas" and number == "42"):
						file_mod[name_file] = {"bug": bug, "bug_only_plus":bug_only_plus, "fix_commit": fix_commit}
		else:
			i += 1

	if project in modified:
		modified[project][number] = file_mod
	else:
		modified[project] = {number:file_mod}

manual_check = open("manual_check.txt", "r")
lines = manual_check.readlines()

only_manual = set()
manual_check.close()
for line in lines:
	l = line.split("\t")
	if l[0] in modified:
		if l[1] in modified[l[0]]:
			modified[l[0]][l[1]] = ""
for line in lines:
	l = line.split("\t")
	a_list = l[3].strip().split(";")
	map_object = map(int, a_list)
	temp_array = list(map_object)
	file_cut = l[2].split("/")[-1].rstrip()
	if l[0] in modified:
		if l[1] in modified[l[0]]:
			if l[2] in modified[l[0]][l[1]]:
				modified[l[0]][l[1]][file_cut]["bug"].append(temp_array)
			else:
				modified[l[0]][l[1]] =  { file_cut : {"bug": [temp_array], "bug_only_plus": []}}
			only_manual.add(l[0]+l[1])



with open("bug-fixes.txt",'w', newline='', encoding='utf-8') as output:
	writer = csv.writer(output, delimiter=';')
	for p in modified:
		for n in modified[p]:
			only_plus = 0
			temp_a = ""
			temp_f = ""
			for f in modified[p][n]: 
				temp_f = f
				omission = 0
				if p+n in only_manual:
					omission = 1
				writer.writerow([p,n,f,modified[p][n][f]["bug"],modified[p][n][f]["bug_only_plus"],str(omission)])
				if modified[p][n][f]["bug"]:
					only_plus += 1
				else:
					only_plus -= 1

