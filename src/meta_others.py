#!/usr/bin/env python3



#import sys
#import os
from os import path
from datetime import datetime

#from PIL import Image
#from PIL.ExifTags import TAGS
import json
import exiftool

from tags import *



LOCAL_LICENSE="Rights specified by the local license file"



def get_time(pathfile,file_date):
	if file_date :
		### date UTC ISO8601 of modification of file content
		t= datetime.utcfromtimestamp(path.getmtime(pathfile)).strftime("%Y-%m-%d")
	else :
		t=''
	return t



def get_files_metadata(pathfile,licenses_path_list,default_owner,default_contact,file_date):
	metadata=METADATA.copy()
	#metadata[FILE_FIELD]=pathfile
	#print(md[FILE_TAG])
	metadata[OWNER_FIELD]=default_owner
	metadata[CONTACT_URL_FIELD]=default_contact
	metadata[DATE_FIELD]= get_time(pathfile,file_date)
	
	for license_path in licenses_path_list :
		#print(pathfile,license_path)
		if pathfile.startswith(path.dirname(license_path)) :
			#print("MATCH",pathfile,license_path)
			metadata[RIGHTS_FIELD]=LOCAL_LICENSE
			metadata[RIGHTS_URL_FIELD]=license_path
			break
	else :
		print(WRN2,pathfile)
	
	return metadata



def get_licenses_metadata(licenses_path,default_owner,default_contact,file_date):
	metadata=METADATA.copy()
	#metadata[FILE_FIELD]= path.join(path.dirname(licenses_path),'*')
	#print(md[FILE_TAG])
	metadata[OWNER_FIELD]=default_owner
	metadata[CONTACT_URL_FIELD]=default_contact
	metadata[DATE_FIELD]= get_time(licenses_path,file_date)
	metadata[RIGHTS_FIELD]=LOCAL_LICENSE
	metadata[RIGHTS_URL_FIELD]=licenses_path
	
	return metadata



def get_others_metadata(others_path_list,licenses_path_list,default_owner='',default_contact='',file_date=False,glob=True):
	metadata_files={}
	
	if glob :
		for licenses_path in licenses_path_list :
			metadata=get_licenses_metadata(licenses_path,default_owner,default_contact,file_date)
			licenses_path = path.join(path.dirname(licenses_path),'*')
			#print(metadata)
			metadata_files[licenses_path]=metadata#.append(metadata)
	else :
		#print(licenses_path_list)
		licenses_path_list=sorted(licenses_path_list,key=len,reverse=True)
		#print(licenses_path_list)
		for file_path in others_path_list :
			metadata= get_files_metadata(file_path,licenses_path_list,default_owner,default_contact,file_date)
			#print(metadata)
			metadata_files[file_path]=metadata#.append(metadata)
		
	return metadata_files

