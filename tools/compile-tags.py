#!/usr/bin/env python3


import json
#import sys
import os
from os import path

JSON_FILES="../data/tags/templates"
OUTPUT_FILE="../data/tags/args.txt"
JSON_EXT='.json'


def get_files(root_path=".",exclude_prefixes=('__', '.')):
	db=[]
	for root, dirs, files in os.walk(root_path):
		# exclude all dirs starting with exclude_prefixes
		dirs[:] = [d for d in dirs if not d.startswith(exclude_prefixes)]
		files = [f for f in files if not f.startswith(exclude_prefixes)]
		for name in files :
			if path.splitext(name)[1]==JSON_EXT :
				pathfile=os.path.join(root,name)
				db.append(pathfile)
	return db


def get_keys(files_list):
	db=set([])
	for p in files_list :
		with open(p, 'r') as f :
			dico = json.load(f)[0]
			db.update( dico.keys() )
	return db


def write_args(db,output_file):
	dbl=['-'+key+"\n" for key in db ]
	dbl.sort()
	with open(output_file,'w') as of :
		of.writelines(dbl)


if __name__ == '__main__' :
	progpath= path.dirname(__file__)
	jsonpath= path.normpath(path.join(progpath,JSON_FILES))
	outfile= path.normpath(path.join(progpath,OUTPUT_FILE))
	#print( __file__, progpath, jsonpath, outfile )

	fl=get_files(jsonpath)
	db=get_keys(fl)
	write_args(db,outfile)

