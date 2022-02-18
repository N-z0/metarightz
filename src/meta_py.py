#!/usr/bin/env python3



import ast

from tags import *



DOCSTRINGS=('__doc__','__status__','__version__','__license__','__date__','__author__','__maintainer__','__credits__','__contact__')



def get_metadata(pathfile):
	metadata={}
	with open(pathfile, 'r') as pf :
		#print(pathfile)
		tree = ast.parse(pf.read())
		for node in tree.body :
			if isinstance(node, ast.Assign) :
				#print(ast.dump(node))
				#print(str(node.targets[0]))
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


def get_py_metadata(pathfile_list):
	metadata_files={}
	for pathfile in pathfile_list :
		pmd=get_metadata(pathfile)
		
		metadata=METADATA.copy()
		#metadata[FILE_FIELD]=pathfile
		metadata[CREATOR_FIELD]=pmd.get('__author__','')
		
		contributors=list(pmd.get('__credits__',[]))
		maintainer=pmd.get('__maintainer__','')
		metadata[CONTRIBUTORS_FIELD]=','.join(contributors+[maintainer]).strip(',')
		
		metadata[CONTACT_URL_FIELD]=pmd['__contact__']
		metadata[DATE_FIELD]=pmd.get('__date__','')
		metadata[RIGHTS_FIELD]=pmd.get('__license__','')
		
		metadata_files[pathfile]=metadata#.append(metadata)
		
	return metadata_files

