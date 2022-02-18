#!/usr/bin/env python3

### N-z0
### 2021
### v2
### the all-tags.txt files are created by the compilation of all tags found in each json directories.
 

import json
#import sys
import os
from os import path

JSON_FILES="../data/tags/"
OUTPUT_FILE="all-tags.txt"
JSON_EXT='.json'


def get_keys(pathfile):
	with open(pathfile, 'r') as f :
		dico = json.load(f)[0]
	return dico.keys()


def write_args(db,output_file):
	dbl=['-'+key+"\n" for key in db ]
	dbl.sort()
	with open(output_file,'w') as of :
		of.writelines(dbl)


if __name__ == '__main__' :
	progpath= path.dirname(__file__)
	jsonpath= path.normpath(path.join(progpath,JSON_FILES))
	#print( __file__, progpath, jsonpath )
	
	for elements in os.walk(jsonpath) :
		directory=elements[0]
		files=elements[2]
		db=set([])
		for name in files :
			if path.splitext(name)[1]==JSON_EXT :
				pathfile=os.path.join(directory,name)
				print( "get: ",pathfile )
				db.update( get_keys(pathfile) )
		if db :
			outfile= path.join(directory,OUTPUT_FILE)
			print( "write: ",outfile )
			write_args(db,outfile)

