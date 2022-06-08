#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide the principal function."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-05-1"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### commonz modules
from commonz.fs import pathnames,checks,timers

### local modules
#from parsers import *
from parsers import meta_img
from parsers import meta_py
from parsers import meta_html
from parsers import meta_license
from parsers import meta_others



### supported mimetype format
EXIF_TYPES=('image/png','image/jpeg','image/gif','image/svg+xml','audio/ogg','audio/flac')
HTML_TYPES=('text/html',)
PY_TYPES=('text/x-python',)
XCF_TYPES=('application/x-xcf',)#Gimp files
#OTHERS_TYPES=('text/x-sh','text/css','text/markdown','text/plain','text/csv','text/tab-separated-values','application/json')



def get_time(pathfile,file_date):
	"""get UTC ISO8601 date of the file content modification"""
	if file_date :
		timestamp= timers.get_modification_time(pathfile)
		t= timers.convert_time(timestamp,time_zone=False).strftime("%Y-%m-%d")
	else :
		t=''
	return t


def get_metadata_database(regular_items,license_items,default_owner,default_contact,file_date,glob,data_pathnames,local_license_text):
	"""return a dictionary of files with copyright and license attributes"""
	
	db={}
	
	other_items={}
	### get metadata from recognized types of files
	for item in regular_items.items() :
		file_index=item[0]
		file_path=item[1]
		tip=checks.get_mimetype(file_path)[0]
		default_date= get_time(file_path,file_date)
		if tip in EXIF_TYPES :
			db[file_path]= meta_img.get_img_metadata(file_path,file_index,data_pathnames,default_owner,default_contact,default_date)
		elif tip in HTML_TYPES :
			db[file_path]= meta_html.get_html_metadata(file_path,file_index,default_owner,default_contact,default_date)
		elif tip in PY_TYPES :
			db[file_path]= meta_py.get_py_metadata(file_path,file_index,default_owner,default_contact,default_date)
		else : 
			other_items[file_index]=file_path
	
	if not glob :
		for item in license_items.items() :
			file_index=item[0]
			file_path=item[1]
			license_path= pathnames.get_path(file_path)
			default_date= get_time(file_path,file_date)
			db[license_path]= meta_license.get_license_metadata(file_index,default_owner,default_contact,default_date,local_license_text)
	else :
		sorted_license_list=sorted(license_items,key=len,reverse=True)
		#print(sorted_license_list)
		for item in other_items.items() :
			file_index=item[0]
			file_path=item[1]
			default_date= get_time(file_path,file_date)
			db[file_path]= meta_others.get_others_metadata(file_index,sorted_license_list,default_owner,default_contact,default_date,local_license_text)
	return db

