#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "create the all-tags.txt file by the compilation of all tags found in each json directories."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-06-22"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



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

