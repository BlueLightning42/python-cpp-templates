import re
import os

# messy and some parts are unessisary/just for beautification but it works
def methodfunc(m,classname, cpp=True):
	out = []
	if m is None: return ''
	for meth in m:
		dlr,param = meth.replace(')','').split('(')

		param = param.split(',')
		if param[0] == '': param = []

		if cpp:
			s = (' ' + classname + '::').join(dlr.split()) + '('
			tmp = []
			if len(param) > 0:
				for p in param:
					p = p.strip().split()
					if len(p) < 2:
						p.append("TEMPNAME")

					tmp.append( f"{p[0]} {p[1]}")

				if len(tmp) > 0:
					s += ', '.join(tmp)
			s += '){\n\t\n}\n'
		else: # .h
			s = '\n\t' + dlr + '('
			tmp = []
			if len(param) > 1:
				for p in param:
					p = p.strip().split(' ')
					tmp.append(p[0])
				if len(tmp) > 0:
					s += ', '.join(tmp)
			s += ');'
		out.append(s)
	return ''.join(out)


def format_cpp_methods(private, public, clsnm, find=True):
	
	findmethods = re.compile(r"^\s+\w+\s+\w+?\(.*?\)",re.MULTILINE)

	if private is None: private = ""
	else:
		if find:
			private = findmethods.findall(private.group(1))
			if len(private) == 0: private = None
		if private is None: private = ""
		else: # not None
			private = "\n// Private Methods\n" + methodfunc(m=private, classname=clsnm, cpp=True)
	
	if public is None: public = ""
	else:
		if find:
			public = findmethods.findall(public.group(1))
			if len(public) == 0: public = None
		if public is None: public = ""
		else: # not None
			public = "\n// Public Methods\n" + methodfunc(m=public, classname=clsnm, cpp=True)
	
	return private + public


def class_files(classname,public_methods=[],private_methods=[]):
	directory = os.path.dirname(__file__)
	#print(directory)
	cpp_template = ""
	hpp_template = ""
	with open(os.path.join(directory,'template.cpp'), 'r') as tmp:
		cpp_template = tmp.read()
	with open(os.path.join(directory,"template.h"), 'r') as tmp:
		hpp_template = tmp.read()
	
	cpp_name = f"{classname.lower()}.cpp"
	hpp_name = f"{classname.lower()}.h"
	
	with open(cpp_name,'w+') as dg:
		dg.write(cpp_template.format(classname=classname,
									classnamelower=classname.lower(),
									methods=format_cpp_methods(private_methods, public_methods, classname, find=False))
		)

	with open(hpp_name,'w+') as dg:
		dg.write(hpp_template.format(classname=classname,
									classnamelower=classname.lower(),
									public_methods=methodfunc(public_methods, classname, cpp=False),
									private_methods=methodfunc(private_methods, classname, cpp=False))
		)



def cpp_from_h(header):
	directory = os.path.dirname(__file__)
	
	cpp_template = ""
	header_file = ""
	with open(os.path.join(directory,'template.cpp'), 'r') as tmp:
		cpp_template = tmp.read()
	with open(header, 'r') as tmp:
		header_file = tmp.read()
	
	classname = re.search(r"class\s+(\w+)",header_file).group(1)

	private = re.compile(r"private:(.*?)((public:)|(};))", re.DOTALL)
	public  = re.compile(r"public:(.*?)((private:)|(};))", re.DOTALL)
	private = private.search(header_file)
	public  = public.search(header_file)

	methods = format_cpp_methods(private, public, classname, find=True)

	cpp_name = f"{classname.lower()}.cpp"
	

	with open(cpp_name,'w+') as dg:
		dg.write(cpp_template.format(classname=classname,
									classnamelower=classname.lower(),
									methods=methods)
		)

