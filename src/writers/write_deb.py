#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "write output in Debian copyrights file."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
#import os
#import collections

### commonz modules
#from commonz import logger
from commonz.fs import pathnames#,checks,actions

### local modules
from metadata import *



DEBIAN_COPYRIGHT_FORMAT="Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/"
DEBIAN_DIRECTORY="/usr/share"
#LICENCES_SYSTEM_PATH=""



def get_pathname(metadata,prog_path):
	"""return the full path name of the file"""
	path_index= metadata[FILE_FIELD]
	full_path= pathnames.join_pathname(prog_path,path_index)
	return full_path


def get_copyright(metadata):
	"""make and return a copyright string line"""
	copyrights=[]
	
	if metadata[DATE_FIELD] :
		copyrights.append(metadata[DATE_FIELD])
	
	if metadata[OWNER_FIELD] :
		person=metadata[OWNER_FIELD]
	else :
		person=metadata[CREATOR_FIELD]
	copyrights.append( person )
	
	if not metadata[CONTACT_URL_FIELD] in person :
		copyrights.append( metadata[CONTACT_URL_FIELD] )
	
	return ' '.join(copyrights).strip()


def get_local_license(license_index,licenses_files,prog_path,included_license=True):
	"""get the local license path or reference"""
	if included_license :
		license="L-"+str(len(licenses_files.keys())+1)
	else :
		license= pathnames.join_pathname(prog_path,license_index)
	
	return license.strip()


def get_distant_license(metadata):
	"""get the distant license URL"""
	if metadata[RIGHTS_FIELD]==metadata[RIGHTS_URL_FIELD] :
		license=metadata[RIGHTS_FIELD]
	else :
		license=' '.join([metadata[RIGHTS_FIELD],metadata[RIGHTS_URL_FIELD]])
	
	return license.strip()


def get_comment(metadata):
	"""get comment made from the metadata"""
	comments=[]
	if metadata[OWNER_FIELD] and metadata[CREATOR_FIELD]:
		comments.append("Creator[{}]".format(metadata[CREATOR_FIELD]))
	if metadata[CONTRIBUTORS_FIELD] :
		comments.append("Contributors[{}]".format(metadata[CONTRIBUTORS_FIELD]))
	if metadata[SOFTWARE_FIELD] :
		comments.append("Software Used[{}]".format(metadata[SOFTWARE_FIELD]))
	if metadata[SOURCE_FIELD] :
		comments.append("Work Based On[{}]".format(metadata[SOURCE_FIELD]))
	return ' '.join(comments)
	


def write_debian_copyright(directory,db,output_file,local_license_text,included_license=True):
	"""
	write metadata into debian copyright file
	if included_license is True the all license text files are copied
	"""
	
	prog_name= pathnames.get_name(directory)
	prog_path= pathnames.join_pathname(DEBIAN_DIRECTORY,prog_name)
	
	licenses_files={}
	with open(output_file,'w',newline='') as copyright_file :
		
		### write_header
		copyright_file.write(DEBIAN_COPYRIGHT_FORMAT+'\n')
		copyright_file.write("\n")
		
		### write_files
		for key in sorted(db.keys()) :
			metadata=db[key]
			
			copyright_file.write("\n")
			
			pathname= get_pathname(metadata,prog_path)
			copyright_file.write("Files: {}\n".format(pathname) )
			
			copyright= get_copyright(metadata)
			copyright_file.write("Copyright: {}\n".format(copyright) )
			
			if metadata[RIGHTS_FIELD]==local_license_text :
				license_index=metadata[RIGHTS_URL_FIELD]
				if license_index in licenses_files :
					license= licenses_files[license_index]
				else:
					license= get_local_license(license_index,licenses_files,prog_path,included_license)
					licenses_files[license_index]=license
			else :
				license= get_distant_license(metadata)
			copyright_file.write("License: {}\n".format(license) )
			
			comment=get_comment(metadata)
			if comment :
				copyright_file.write("Comment: {}\n".format(comment) )
			
		copyright_file.write("\n")
		
		### write_licenses
		if included_license :
			for item in licenses_files.items() :
				index=item[0]
				pathname=item[1]
				copyright_file.write("\n")
				copyright_file.write("License: {}\n".format( pathname ))
				license_path= pathnames.join_pathname(directory,index)
				with open(license_path,'r',newline='') as lf :
					for line in lf.readlines() :
						if not line=="\n" :
							line='\t'+line#.replace('\n','\n\t')
						else :
							line='\t.\n'
						copyright_file.write(line)

