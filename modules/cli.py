import os




"""
COMMAND LINE INTERFACE CORE FUNCTIONS
"""

#--------------------------------------------------------------------------------------------------------------------------------

def inp():
	"""general text input"""
	return input("#: ").strip().lower()

def param_validate(val, mode, mode_arg=None):
	"""validates a parameter by its requested mode"""
	x = "[x]"
	if mode == "file":
		if (os.path.isfile(val)):
			return val
		else:
			print(x, "is not a file path:", val)
	elif mode == "dir":
		if (os.path.isdir(val)):
			return val
		else:
			print(x, "is not a directory:", val)
	elif mode == "user":
		if (os.path.isdir(os.path.join("/Users", val))):
			return val
		else:
			print(x, "no user found:", val)
	elif mode == "int_pos":
		intval = None
		try:
			intval = int(val)
		except Exception as e:
			print(x, "cannot parse as integer:", val)
		else:
			if (intval >= 0):
				return intval
			else:
				print(x, "expected positive integer, got", val)
	elif mode == "inlist":
		if val in mode_arg:
			return val
		else:
			print(x, "value",val,"is not one of:",mode_arg)
	else:
		print("[?!] param_validate: no validation mode matched")
	return None



def param_read(mode, mode_arg=None):
	"""requests a parameter until a valid one is received"""
	while (1):
		value = param_validate(inp(), mode, mode_arg)
		if not value == None:
			return value

def get_params(param_descriptions, args=None):

	if not args == None: # fail if params are provided, but not all are there
		if not len(args) == len(param_descriptions):
			print("[x] Expected",len(param_descriptions),"arguments after command, got",len(args))
			return None

	out = []
	counter = 0

	for param in param_descriptions: # otherwise iterate over every parameter description
		param_message = param[0]
		param_mode = param[1]
		try:
			param_mode_arg = param[2]
		except:
			param_mode_arg = None

		if args == None: # interactive mode
			print(param_message)
			out.append(param_read(param_mode, param_mode_arg))
		else:
			value = param_validate(args[counter], param_mode, param_mode_arg)
			if value == None:
				return None
			out.append(value)
		counter += 1
	return out



