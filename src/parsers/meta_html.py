#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "extract metadata from HTML files"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-06-22"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



###  HTML md are supposed to be used by validators,
### but in many cases most validators ignore them until they become official parts of the spec.
### So the only standard md right now are:
###    application-name
###    author
###    description
###    generator
###    keywords
### Source: http://dev.w3.org/html5/spec/text-level-semantics.html#the-small-element



### builtin modules
#import os

### HTML parser
### need to install  python3-bs4
from bs4 import BeautifulSoup

### commonz modules
#from commonz import logger
#from commonz.datafiles import html

### local modules
from metadata import *



def get_metadata(pathfile):
	"""extract all metadata from an html file"""
	metadata={}
	with open(pathfile, 'r') as pf :
		soup = BeautifulSoup(pf, "lxml")
		for meta in soup.find_all("meta"):
			name= meta.get("name",None)
			content= meta.get("content",None)
			if name and content :
				metadata[name]=content
	return metadata


def get_html_metadata(file_path,file_index,default_owner,default_contact,default_date):
	"""return relevant metadata from an html file"""
	md=get_metadata(file_path)
	#print(md)
	metadata=METADATA.copy()
	metadata[FILE_FIELD]=file_index
	metadata[CREATOR_FIELD]=md.get('author',default_owner)
	metadata[CONTRIBUTORS_FIELD]=md.get('contributors','')
	metadata[CONTACT_URL_FIELD]=md.get('contact',default_contact)
	metadata[DATE_FIELD]=md.get('date',default_date)
	metadata[RIGHTS_FIELD]=md.get('license','')
		
	return metadata

