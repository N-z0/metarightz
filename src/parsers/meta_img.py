#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "extract metadata from image files"#information describing the purpose of this module
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

### Images parser
#from PIL import Image
#from PIL.ExifTags import TAGS
import exiftool

### commonz modules
#from commonz import logger
from commonz.datafiles import jon

### local modules
from metadata import *



JSON_FILES=["tags/useful/describe","tags/useful/personal","tags/useful/rights"]

SOURCE='SOURCE'
SOFTWARE='SOFTWARE'
CREATOR='CREATOR'
CONTRIBUTORS='CONTRIBUTORS'
OWNER='OWNER'
CONTACT_URL='CONTACT_URL'
DATE='YYYY:MM:DD'
RIGHTS='RIGHTS'
RIGHTS_URL='RIGHTS_URL'
TAGS=(SOURCE,SOFTWARE,CREATOR,CONTRIBUTORS,OWNER,CONTACT_URL,DATE,RIGHTS,RIGHTS_URL)



def get_keys_database(data_pathnames):
	"""extract relevant tags from json files"""
	tags={}
	for json_path in JSON_FILES :
		json_full_path= data_pathnames[json_path]
		dico = jon.get_keys(json_full_path)[0]
		#print(dico )
		for item in dico.items() :
			key=item[0]
			tag=item[1]
			if tag in TAGS :
				key=key.replace("XMP-xmpRights:","XMP:").replace("XMP-dc:","XMP:").replace("XMP-cc:","XMP:").replace("XMP-tiff:","XMP:").replace("XMP-iptcExt:","XMP:")
				if tag in tags :
					tags[tag].update([key])
				else :
					tags[tag]=set([key])
	return tags


def get_metadata(fl,tags):
	"""return relevant metadata from an image file"""
	with exiftool.ExifTool() as et :
		return et.get_tags_batch(tags,fl)


def get_valu(metadata,tags):
	"""return a particular metadata value"""
	valu=""
	for t in tags :
		v= str(metadata.get(t,""))
		v= v.replace("\t", " ")
		v= v.replace("\n", " ")
		v= v.strip()
		if valu in v :
			valu=v
		elif not v in valu :
			if valu=="" :
				valu=v
			else:
				valu=";".join([valu,v])
	return valu


def get_img_metadata(file_path,file_index,data_pathnames,default_owner,default_contact,default_date):
	"""return relevant metadata from an image file"""
	tags=get_keys_database(data_pathnames)
	#print(tags)
	metadata=METADATA.copy()
	with exiftool.ExifTool() as et :
		md=et.get_metadata(file_path)
		#print(md)
		metadata[FILE_FIELD]=file_index
		metadata[SOURCE_FIELD]=get_valu(md,tags[SOURCE])
		metadata[SOFTWARE_FIELD]=get_valu(md,tags[SOFTWARE])
		metadata[CREATOR_FIELD]=get_valu(md,tags[CREATOR])
		metadata[CONTRIBUTORS_FIELD]=get_valu(md,tags[CONTRIBUTORS])
		metadata[OWNER_FIELD]=get_valu(md,tags[OWNER]) or default_owner
		metadata[CONTACT_URL_FIELD]=get_valu(md,tags[CONTACT_URL]) or default_contact
		metadata[DATE_FIELD]=get_valu(md,tags[DATE]) or default_date
		metadata[RIGHTS_FIELD]=get_valu(md,tags[RIGHTS])
		metadata[RIGHTS_URL_FIELD]=get_valu(md,tags[RIGHTS_URL])
	return metadata

