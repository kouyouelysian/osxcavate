import os, shutil
from modules import common, classes
from modules.common import v, vv, vvv


"""
HIGH-LEVEL FUNCTIONS USED BY THE MAIN PROJECT FILE AND OTHER SUBPROGRAMS
"""

#--------------------------------------------------------------------------------------------------------------------------------

def scanplaces_extension(extension, username, list, pseudonym=None, verbose="v"):
	"""
	takes in a list of "interesting places" as a file, recursively finds any dirs in it that have a file of a given extension
	ARGUMENTS: username (string) - target user name of the computer, list (string) - interesting places txt file location,
	           verbose (string) - verboseness level
	RETURNS:   (list) of subdirectories or False on error
	"""
	if (v(verbose)):
		print("\n---- recursive scanning for ["+extension+"] files for username ["+username+"], list of places fetched from ["+list+"]\n")
	out = []
	fh = open(os.path.join(os.getcwd(), list), "r")
	lines = fh.readlines()
	fh.close()
	dirs = []
	ignore = []
	mode = True
	for line in lines:
		if line.strip() == "INCLUDE:":
			mode = True
		elif line.strip() == "IGNORE:":
			mode = False
		else:
			if (mode):
				dirs.append(common.template_fill_field(line.rstrip(), "user", username))
			else:
				ignore.append(common.template_fill_field(line.rstrip(), "user", username)) 

	for directory in dirs:
		if vv(verbose):
			print("scanning "+directory+" recursively for files of ["+extension+"] extension...")

		temp = common.dirs_with_files_of_extension(directory, extension, ignorelist=ignore, verbose=verbose)
		if temp == False:
			if v(verbose):
				print("Error processing directory (maybe bad dir?): "+ directory)
		out += temp
	if not pseudonym==None:
		for o in out:
			o["search_place"] = o["search_place"].replace(username, pseudonym)
		return classes.Dirlist(data=out, username=pseudonym, verbose=verbose)
	return classes.Dirlist(data=out, username=username, verbose=verbose)

#--------------------------------------------------------------------------------------------------------------------------------

def scanplaces_plist(username, pseudonym=None, verbose="v"):
	"""
	recursively finds any dirs in it that have a plist in them based off pre-defined "interesting folders"
	ARGUMENTS: username (string) - target user name of the computer, verbose (string) - verboseness level
	RETURNS:   (list) of subdirectories
	"""
	return scanplaces_extension("plist", username, "lists/bundled/places.txt", pseudonym, verbose)

#--------------------------------------------------------------------------------------------------------------------------------

def scanplaces_sqlite(username, pseudonym=None, verbose="v"):
	"""
	recursively finds any dirs in it that have a sqlite in them based off pre-defined "interesting folders"
	ARGUMENTS: username (target username of the computer), verbose (string) - verboseness level
	RETURNS:   (list) of subdirectories
	"""
	return scanplaces_extension("sqlite", username, "lists/bundled/places.txt", pseudonym, verbose)

#--------------------------------------------------------------------------------------------------------------------------------

def overlapping_files(source="./datasource/json", method="json", tolerance=0, verbose="v"):
	"""
	produces a list of files that are common (overlap) over many datadumps
	ARGUMENTS: source (string) - folder with source data, method (string) - datastore type (only json for now),
	           tolerance (int) - how many data dumps may have the file not present, verbose (string) - verboseness level
	RETURNS: (list) of common files or False on fail
	"""
	if (v(verbose)):
		print("\n---- detecting overlapping files in dumps by ["+method+"] method, data fetched from ["+source+"]\n")

	if method=="json":

		# import
		files = common.files_of_extension_in_dir(source, method, verbose)
		
		if (len(files) <= tolerance):
			print("[x] Tolerance of", tolerance, "cannot be more than the number of data dumps imported -", len(files))
			return False

		if vv(verbose):
			print("found "+str(len(files))+" json files in "+source+", trying to load")
		dirlists = []
		for f in files:
			d = classes.Dirlist(verbose=verbose)
			if d.import_json(f):
				if vv(verbose):
					print("success loading "+f)
				dirlists.append(d)
		if vv(verbose):
			print("imported "+str(len(dirlists))+" datadumps, searching for common filepaths")

		# process
		dict = {}

		for dlist in dirlists:
			for d in dlist.data:
				for f in d["files"]:
					path = common.path_pseudonym_replace(d["search_place"]+d["directory"]+"/"+f)
					if not path in dict:
						if vvv(verbose):
							print("added "+path)
						dict[path] = 1
					else:
						dict[path] += 1
						if vvv(verbose):
							print("another "+path+", count "+str(dict[path]))

		out = []
		threshold = len(dirlists) - tolerance # has to be this many or more to make it to the final list
		for key in dict.keys():
			if dict[key] >= threshold:
				out.append(key)
				if vvv(verbose):
					print("deemed common: "+key)
			else:
				if vvv(verbose):
					print("eliminated: "+key)
		if v(verbose):
			print("total common files found:", len(out))

		return out



#--------------------------------------------------------------------------------------------------------------------------------

def export_artefacts(username, artefacts, export_path, verbose="v"):

	counter = 0

	for a in artefacts:
		filepath = common.template_fill_field(a["path"], "user", username)
		outdir = os.path.join(export_path, a["rank"])
		
		try:
			shutil.copy2(filepath, outdir)
		except:
			if vv(verbose):
				print("was unable to copy file",filepath)
		else:
			if vvv(verbose):
				print("copied",filepath,"to",outdir)
			counter += 1

	if v(verbose):
			print("excavated",counter,"files out of",len(artefacts),"listed")






