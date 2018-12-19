# Jay Huskins 2018

import os, re

def get_file_duplicates(filename, line_trim = 1, count_trim = 2, duplicates = {}):
	with open(filename) as f:
		lines = f.readlines()

	for line in lines:
		cur_line = line.strip()
		cur_line = cur_line.replace(","," ")
		
		#skip line if it only contains whitespace or is shorter than line_trim cutoff
		if not re.match('\w', cur_line) or len(cur_line) < line_trim:
			continue

		#if the line is already recorded, increment the number of duplicates
		if cur_line in duplicates.keys():
			duplicates[cur_line] += 1
		#if the line is unrecorded, make a new entry
		else:
			duplicates[cur_line] = 0

	for key in duplicates.keys():
		#remove duplicated line if the number of duplicates is less than count_trim cutoff
		if duplicates[key] < count_trim:
			duplicates.pop(key, None)

	return duplicates


def get_dir_duplicates(directory, line_trim = 1, count_trim = 2, write_to = None, filetype= 'java'):
	#duplicates is a dict with lines of code as keys
	# the value is a list where [0] is an int counting the duplication of the key line
	# [1:] of the list is all the names of files where the key line is found
	duplicates = {}
	for root, dirs, files in os.walk(directory):
		for file in files:
			#for every file in the directory, if it is the target filetype, parse it
			if file.endswith("."+ filetype):		
				#get full path name ( '\'' replaced with '/' for Mac-Win consistency)
				filename = os.path.join(root, file).replace("\\","/")
				with open(filename) as f:
					lines = f.readlines()

				for line in lines:
					cur_line = line.strip()
					cur_line = cur_line.replace(","," ")
					#skip line if it only contains whitespace 
					# or is shorter than line_trim cutoff 
					# or is an import statement
					if not re.match('\w', cur_line) or len(cur_line) < line_trim or line.startswith("import "):
						continue

					#if the line is already recorded, increment the number of duplicates and record the source
					if cur_line in duplicates.keys():
						duplicates[cur_line][0] += 1
						duplicates[cur_line].append(filename)
					#if the line is unrecorded, make a new entry
					else:
						duplicates[cur_line] = [0]

	text = ''
	for line in duplicates.keys():
		count =  duplicates[line][0]
		#remove duplicated line if the number of duplicates is less than count_trim cutoff
		if count < count_trim:
			duplicates.pop(line, None)
		# add a row to the csv output
		# format of row: # of duplicates, duplicated line, sources...
		else:
			text += ",".join([str(count), line] + duplicates[line][1:]) + "\n"

	if write_to:
		if not write_to.endswith(".csv"):
			write_to += ".csv"
		header = ["Duplications, Line, Sources..."]
		with open(write_to, 'w') as f:
			f.write(",".join(header) + "\n" + text)			

	return duplicates


if __name__ == "__main__":

	get_dir_duplicates("../mahout/mahout-0.1", 30, 5, "mahout_duplicates" )
