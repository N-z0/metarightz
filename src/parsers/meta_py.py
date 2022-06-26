#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "extract metadata from Python files"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-06-22"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
#import os

### Py parser
import ast

### commonz modules
#from commonz import logger

### local modules
from metadata import *



DOCSTRINGS=('__doc__','__status__','__version__','__license__','__date__','__author__','__maintainer__','__credits__','__contact__')



def get_metadata(pathfile):
	"""extract all metadata from a py file"""
	metadata={}
	with open(pathfile, 'r') as pf :
		#print(pathfile)
		tree = ast.parse(pf.read())
		for node in tree.body :
			if isinstance(node, ast.Assign) and hasattr(node.targets[0],'id'):
				#print(ast.dump(node))
				#print(dir(node.targets[0]))
				name = node.targets[0].id
				if name in DOCSTRINGS :
					valu = node.value
					if isinstance(valu, ast.Constant) :
						data = valu.value
					elif isinstance(valu, ast.List) or isinstance(valu, ast.Tuple) :
						data =[]
						for c in valu.elts :
							data.append(c.value)
					else :
						print("BAD:",ast.dump(node))
					#print(name,data)
					metadata[name]=data
	return metadata


def get_py_metadata(file_path,file_index,default_owner,default_contact,default_date):
	"""return relevant metadata from a py file"""
	
	md=get_metadata(file_path)
	#print(md)
	
	metadata=METADATA.copy()
	metadata[FILE_FIELD]=file_index
	metadata[CREATOR_FIELD]=md.get('__author__',default_owner)
	contributors=list(md.get('__credits__',[]))
	maintainer=md.get('__maintainer__','')
	metadata[CONTRIBUTORS_FIELD]=','.join(contributors+[maintainer]).strip(',')
	metadata[CONTACT_URL_FIELD]=md.get('__contact__',default_contact)
	metadata[DATE_FIELD]=md.get('__date__',default_date)
	metadata[RIGHTS_FIELD]=md.get('__license__','')
	
	return metadata

