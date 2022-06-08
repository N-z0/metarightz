#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "write output in TSV file"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-06-21"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
#import os

### commonz modules
#from commonz import logger
from commonz.datafiles import tsv

### local modules
from metadata import *



HEAD_FIELDS=[FILE_FIELD,DATE_FIELD,SOURCE_FIELD,SOFTWARE_FIELD,CREATOR_FIELD,CONTRIBUTORS_FIELD,OWNER_FIELD,RIGHTS_FIELD,RIGHTS_URL_FIELD,CONTACT_URL_FIELD]



def write_tsv_files(database,output_file):
	"""
	write metadata into a TSV file
	"""
	
	db_list=[]
	for key in sorted(database.keys()) :
		data=database[key]
		db_list.append(data)
	
	tsv.write_dico(db_list,output_file,HEAD_FIELDS)

