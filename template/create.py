import re
import os

def methodfunc(m,classname, cpp=True):
	out = []
	if m is None: return ''
	for meth in m:

		dlr,param = meth.replace(')','').split('(')

		param = param.split(',')
		if param[0] is '': param = []

		if cpp:
			s = (' ' + classname + '::').join(dlr.split())
			s += '('
			tmp = []
			if len(param) > 0:
				for p in param:
					p = p.strip().split()
					if len(p) < 2:
						p.append("TEMPNAME")

					tmp.append(p[0]+' '+p[1])

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

def class_files(classname,public_methods=[],private_methods=[]):
	directory = os.path.dirname(__file__)
	#print(directory)
	cpp_template = ""
	hpp_template = ""
	with open(os.path.join(directory,'template.cpp'), 'r') as tmp:
		cpp_template = tmp.read()
	with open(os.path.join(directory,"template.h"), 'r') as tmp:
		hpp_template = tmp.read()
	
	cpp_name = "{}.cpp".format(classname.lower())
	hpp_name = "{}.h".format(classname.lower())
	
	with open(cpp_name,'w+') as dg:

		dg.write(cpp_template.format(classname=classname,classnamelower=classname.lower(),
		public_methods=methodfunc(public_methods, classname, cpp=True),
		private_methods=methodfunc(private_methods, classname, cpp=True)))

	with open(hpp_name,'w+') as dg:
		dg.write(hpp_template.format(classname=classname,classnamelower=classname.lower(),
		public_methods=methodfunc(public_methods, classname, cpp=False),
		private_methods=methodfunc(private_methods, classname, cpp=False)))

def cpp_from_h(header):
	directory = os.path.dirname(__file__)
	
	cpp_template = ""
	header_file = ""
	with open(os.path.join(directory,'template.cpp'), 'r') as tmp:
		cpp_template = tmp.read()
	with open(header, 'r') as tmp:
		header_file = tmp.read()
	
	classname = re.search(r"class\s+(\w+)",header_file).group(1)
	findmeth = re.compile(r"^\s+\w+\s+\w+?\(.*?\)",re.MULTILINE)
	methods = findmeth.findall(header_file)
	cpp_name = "{}.cpp".format(classname.lower())

	with open(cpp_name,'w+') as dg:
		dg.write(cpp_template.format(classname=classname,classnamelower=header,
		public_methods=methodfunc(m=methods, classname=classname, cpp=True),
		private_methods=' '))

