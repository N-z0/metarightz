#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "extract metadata from License files"#information describing the purpose of this module
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
#from os import path

### commonz modules
#from commonz import logger
from commonz.fs import pathnames

### local modules
from metadata import *



def get_license_metadata(file_index,default_owner,default_contact,file_date,local_license_text):
	"""get relevant metadata from a license file"""
	metadata=METADATA.copy()
	metadata[FILE_FIELD]= pathnames.join_pathname(pathnames.get_path(file_index),'*')
	metadata[OWNER_FIELD]=default_owner
	metadata[CONTACT_URL_FIELD]=default_contact
	metadata[DATE_FIELD]= file_date
	metadata[RIGHTS_FIELD]=local_license_text
	metadata[RIGHTS_URL_FIELD]=file_index
	
	return metadata
