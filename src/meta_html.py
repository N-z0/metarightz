#!/usr/bin/env python3


###  metatags are supposed to be used by validators,
### but in many cases most validators ignore them until they become official parts of the spec.
### So the only standard metatags right now are:
###    application-name
###    author
###    description
###    generator
###    keywords
### Source: http://dev.w3.org/html5/spec/text-level-semantics.html#the-small-element



### need to install  python3-bs4
from bs4 import BeautifulSoup

from tags import *



def get_metadata(pathfile):
	metadata={}
	with open(pathfile, 'r') as pf :
		soup = BeautifulSoup(pf, "lxml")
		for meta in soup.find_all("meta"):
			name= meta.get("name",None)
			content= meta.get("content",None)
			if name and content :
				metadata[name]=content
	return metadata


def get_html_metadata(pathfile_list):
	metadata_files={}
	for pathfile in pathfile_list :
		metatags=get_metadata(pathfile)
		#print(metatags)
		
		metadata=METADATA.copy()
		#metadata[FILE_FIELD]=pathfile
		metadata[CREATOR_FIELD]=metatags.get('author','')
		metadata[CONTRIBUTORS_FIELD]=metatags.get('contributors','')
		metadata[CONTACT_URL_FIELD]=metatags.get('contact','')
		metadata[DATE_FIELD]=metatags.get('date','')
		metadata[RIGHTS_FIELD]=metatags.get('license','')
		
		metadata_files[pathfile]=metadata#.append(metadata)
		
	return metadata_files

