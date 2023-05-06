import os
from os import path, system
import datetime


"""
COMMON FUNCTIONS TO BE USED BY OTHER MODULES OF THE PROJECT
"""

#--------------------------------------------------------------------------------------------------------------------------------

def v(arg):
	"""
	these check for low verboseness level
	ARGUMENTS: any (expects string of v, v or vvv)
	RETURNS:   bool
	"""
	if (arg=="v") or (arg=="vv") or (arg=="vvv"):
		return True
	return False

def vv(arg):
	"""
	these check for med verboseness level
	ARGUMENTS: any (expects string of v, v or vvv)
	RETURNS:   bool
	"""
	if (arg=="vv") or (arg=="vvv"):
		return True
	return False

def vvv(arg):
	"""
	these check for high verboseness level
	ARGUMENTS: any (expects string of v, v or vvv)
	RETURNS:   bool
	"""
	if (arg=="vvv"):
		return True
	return False

#--------------------------------------------------------------------------------------------------------------------------------

def clear():
	"""
	clears the console screen
	ARGUMENTS: none
	RETURNS:   none
	"""
	system('cls' if os.name=='nt' else 'clear')


#--------------------------------------------------------------------------------------------------------------------------------

def timestmap():
	"""
	returns current local timestamp
	ARGUMENTS: none
	RETURNS:   integer unix timestamp
	"""
	return int(datetime.datetime.now().timestamp())

#--------------------------------------------------------------------------------------------------------------------------------

def get_extension(filename):
	"""
	gets the extension part of the file
	ARGUMENTS: filename (string) - name of a file to get the extension of
	RETURNS:   string - extension of the file
	"""
	return filename.split(".")[-1]

#--------------------------------------------------------------------------------------------------------------------------------

def dirs_with_files_of_extension(directory, extension, ignorelist=None, verbose="v"):
	"""
	Recursively finds all folders and subfolders with at least one file with needed extension inside
	Is needed to gather a lits of locations for interesting files like .plist or .sqlite
	ARGUMENTS: directory (string) - a valid directory like "/Users/Username"; extension (string) - target extension without the
	           dot like "plist";
	           verbose (string) - verbose marker, "v" for verbose, "vv" for very verbose, anything else = not verbose
	RETURNS:   list of {"directory":<directorystring>, "files":[file1, file2..], "search_place":<dirbeingscanned>} dicts 
	"""


	if not os.path.isdir(directory): # catch bad dir
		if v(verbose):
			print("dirs_with_files_of_extension - provided directory does not exist!") 
		return False

	out = [] # initialize output list
	foldercount = 0
	filecount   = 0
	scannedfolder = None
	

	for root, dirs, files in os.walk(directory, topdown=True): # walk and add needed directories

		for d in dirs:
			p = os.path.join(root, d)
			if p in ignorelist:
				dirs.remove(d)
				if vv(verbose):
					print("ignoring "+p+"...")
				continue



		for name in files:
			ext = name.split(".")[-1]
			if (ext == extension):
				if not root == scannedfolder:
					scannedfolder = root
					if (vvv(verbose)):
						print(str(foldercount)+": file with [."+extension+"] in folder "+root+", registering...")
					selectedfiles = files_of_extension_in_dir(root, extension, verbose)
					dict = {"directory":root.replace(directory, ""), "files":selectedfiles, "search_place":directory}
					out.append(dict)
					foldercount += 1
					filecount   += len(selectedfiles)
	if vv(verbose): # indicate end, return
		if (foldercount == 0):
			print("found no folders with [."+extension+"] inside")
		else:
			print("found "+str(foldercount)+" folders with [."+extension+"] inside, "+str(filecount) + " files registered total")
	return out

#--------------------------------------------------------------------------------------------------------------------------------

def files_of_extension_in_dir(directory, extension, verbose):
	"""
	returns all files of a particular extension in a folder
	ARGUMENTTS:
	RETURNS:    list of files of given ext
	"""
	if not os.path.isdir(directory): # catch bad dir
		if v(verbose):
			print("files_of_extension_in_dir - provided directory does not exist!") 
		return False
	out = []
	li = os.listdir(directory)
	for l in li:
		if get_extension(l) == extension:
			if vvv(verbose):
				print("  added "+l+" from "+directory)
			out.append(l)
	return out

#--------------------------------------------------------------------------------------------------------------------------------

def template_fill_field(text, field, value):
	"""
	Fills in a string with a predefined template <<<field>>> with value ("Users/<<<user>>>" --> "Users/Target")
	ARGUMENTS: text (string) - target string; field (string) - field name, without <<< >>>; value (string) - text to
	           replace the field with
	RETURNS:   string with "<<<field>>>" replaced with "value" or the original text on error
	"""
	target = "<<<" + field + ">>>"
	if text.find(target) == -1:
		return text
	return text.replace(target, value)

#--------------------------------------------------------------------------------------------------------------------------------

""" global generation dictionaries for pseudonymizing functions """
pseudodict_a = ["Big","Small","Average","Raging","Smiling","Happy","Sad","Slow","Quick","Temporary","Permanent",\
	"Soft","Edgy","Whole","Suspicious","Cutie","Random","Unremarkable","Singing"]
pseudodict_b = ["Duck","Dog","Cat","Goose","Sheep","Horse","Roach","Snake","Fish","Shark","Tiger",\
	"Ox","Ram","Fox","Wolf","Dragon","Tree","Miku","Demoman"]
pseudodict_c = ["0","1","2","3","4","5","6","7","8","9"]

#--------------------------------------------------------------------------------------------------------------------------------

def pseudonym_generate():
	"""
	generates a random pseudonym - total 20*20*10000=4000000 (4 million) possibilities
	ARGUMENTS: none
	RETURNS:   out (string) - pseudonym string
	"""
	global pseudodict_a
	a = pseudodict_a
	global pseudodict_b
	b = pseudodict_b
	global pseudodict_c
	c = pseudodict_c

	import random
	from math import floor
	random.seed()
	out = a[floor(random.random()*len(a))] + b[floor(random.random()*len(b))] + c[floor(random.random()*len(c))]\
	 + c[floor(random.random()*len(c))] + c[floor(random.random()*len(c))] + c[floor(random.random()*len(c))]
	return out

#--------------------------------------------------------------------------------------------------------------------------------

def pseudonym_detect(arg):
	"""
	detects if a string could be generated by this program's pseudonymizer
	ARGUMENTS: arg (string) - string to check
	RETURNS:   bool - True (is like an OSXCAVATE pseudonym) or False (is not)

	"""
	global pseudodict_a
	global pseudodict_b
	global pseudodict_c

	p = arg
	for a in pseudodict_a:
		if a in arg:
			arg = arg.replace(a, "")
			break
	for b in pseudodict_b:
		if b in arg:
			arg = arg.replace(b, "")

	if len(arg)==4:
		if arg.isdigit():
			return True

	return False

#--------------------------------------------------------------------------------------------------------------------------------

def path_pseudonym_replace(arg, replace_with="<<<user>>>"):
	"""
	tries to replace a pseudonym in a path like /Users/[pseudonym]/...
	ARGUMENTS: arg (string) - the path string to replace
	RETURNS:   out (string) - path with pseudonym replaced with <<<username>>> (if it is
	           a /Users folder), original string (if not)
	"""
	bits = arg.split("/")
	found = None
	for b in bits:
		if pseudonym_detect(b):
			found = b
	if found == None:
		return arg # no pseudonymlike part found
	out = ""
	for b in bits[1:]:
		if b == found:
			out += "/" + replace_with
		else:
			out += "/" + b
	return out

#--------------------------------------------------------------------------------------------------------------------------------

def strlist_to_file(fpath, lines, verbose="v"):
	"""
	puts a list[] of strings to a file at <fpath> as separate lines
	ARGUMENTS: fpath (string) - path to the target file, 
			   lines (list of strings) - contents to write
	RETURNS:   none 
	"""
	for x in range(len(lines)-1):
		lines[x] += "\n"
	fh = open(fpath, "w")
	fh.writelines(lines)
	fh.close()
	if (vvv(verbose)):
		print("wrote", len(lines), "lines to", fpath)

#--------------------------------------------------------------------------------------------------------------------------------

def str_to_file(fpath, line, verbose="v"):
	"""
	puts a string to a file at <fpath> as separate lines
	ARGUMENTS: fpath (string) - path to the target file, 
			   lines (string) - contents to write
	RETURNS:   none 
	"""
	fh = open(fpath, "w")
	fh.writelines(line)
	fh.close()
	if (vvv(verbose)):
		print("wrote to", fpath)

#--------------------------------------------------------------------------------------------------------------------------------