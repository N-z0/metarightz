#!/usr/bin/env python3



import sys
import os
from os import path
import mimetypes

import json
#import exiftool

from tags import *

import meta_img
import meta_others
import meta_py
import meta_html

import write_tsv
import write_deb



#OUTPUT_FILE="docs/licenses.tsv"
EXCLUDE_PREFIXES=('__', '.')

LICENSE_FILE="license.md"
#LICENSE_TYPE="license"

EXIF_TYPES=('image/png','image/jpeg','image/gif','image/svg+xml','audio/ogg','audio/flac')
HTML_TYPES=('text/html',)
PY_TYPES=('text/x-python',)
XCF_TYPES=('application/x-xcf',)#Gimp files
OTHERS_TYPES=('text/x-sh','text/css','text/markdown','text/plain','text/csv','text/tab-separated-values','application/json')

WRN1="WARNING:unknow type: "
WRN2="[WARNING]file without copyrights date: "
WRN3="[WARNING]file without copyrights owner: "
WRN4="[WARNING]file without copyrights license: "
#ERR1="missing code:"
#ERR2="missing :"



def get_file_type(pathfile):
	filename=os.path.basename(pathfile)
	#tip=path.splitext(name)[1]
	tip=mimetypes.guess_type(filename,strict=True)[0]#registered with IANA.
	return tip


def get_files(root_path=".",exclude_prefixes=EXCLUDE_PREFIXES):
	db=[]
	for root, dirs, files in os.walk(root_path):
		dirs[:] = [d for d in dirs if not d.startswith(exclude_prefixes)]
		files = [f for f in files if not f.startswith(exclude_prefixes)]
		for name in files :
			pathfile=path.normpath(os.path.join(root,name))
			db.append(pathfile)
	return db



def get_metadata_database(path_list,default_owner,default_contact,file_date,glob):
	#print(pathfile_list)

	licenses_path_list=[]
	files_path_list=[]
	for p in path_list :
		if os.path.basename(p)==LICENSE_FILE :
			licenses_path_list.append(p)
		else :
			files_path_list.append(p)
	#print(licenses_path_list)

	exif_path_list=[]
	html_path_list=[]
	code_path_list=[]
	xcf_path_list=[]
	others_path_list=[]
	for pathfile in files_path_list :
		#print(pathfile)
		tip=get_file_type(pathfile)
		if tip in EXIF_TYPES :
			exif_path_list.append(pathfile)
		elif tip in HTML_TYPES : 
			html_path_list.append(pathfile)
		elif tip in PY_TYPES : 
			code_path_list.append(pathfile)
		elif tip in OTHERS_TYPES : 
			others_path_list.append(pathfile)
		else :
			print(WRN1,tip,"for file:",pathfile)
			others_path_list.append(pathfile)

	db={}
	if exif_path_list :
		db.update(meta_img.get_img_metadata(exif_path_list))
	if html_path_list :
		db.update(meta_html.get_html_metadata(html_path_list))
	if others_path_list :
		db.update(meta_others.get_others_metadata(others_path_list,licenses_path_list,default_owner,default_contact,file_date,glob))
	if code_path_list :
		db.update(meta_py.get_py_metadata(code_path_list))
		
	return db



def check_metadata(metadata_files):
	for pathfile in metadata_files.keys() :
		#pathfile=metadata[FILE_FIELD]
		metadata=metadata_files[pathfile]
		if not metadata[DATE_FIELD] :
			print(WRN2,pathfile)
		if not ( metadata[RIGHTS_FIELD] or metadata[RIGHTS_URL_FIELD] ) :
			print(WRN4,pathfile)
		if not ( metadata[OWNER_FIELD] or metadata[CREATOR_FIELD] or metadata[CONTACT_URL_FIELD] ) :
			print(WRN3,pathfile)

				

if __name__ == '__main__':
	progpath= path.dirname(__file__)
	#jsonpath= path.normpath(path.join(progpath,JSON_PATH))
	#json_files = [jf for jf in get_files(jsonpath) if path.splitext(jf)[1]==JSON_EXT ]
	#print( __file__, progpath, jsonpath)
	#kd=get_keys_database(json_files)
	#print(kd)
	
	fl=get_files(".")
	#print(get_metadata(fl,("XMP:CopyrightYear","XMP:DateTime","XMP:Date","XMP:ArtworkDateCreated")))
	#print(get_all_metadata(fl))
	#check_metadata_database(fl,kd)
	md=get_metadata_database(fl,default_owner="N-z0",default_contact='syslog@mail.com',file_date=True,glob=True)
	#print(md.keys())
	check_metadata(md)
	#exit()
	
	output_file=sys.argv[1]
	write_tsv.write_tsv_files(md,output_file)
	#write_deb.write_debian_copyright(md,output_file,included_license=True)

