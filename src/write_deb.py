#!/usr/bin/env python3



import collections

from tags import *
import meta_others



LICENCES_SYSTEM_PATH=""



def get_copyright(metadata):
	date=metadata[DATE_FIELD]
	
	if metadata[OWNER_FIELD] :
		person=metadata[OWNER_FIELD]
	else :
		person=metadata[CREATOR_FIELD]
	
	if not metadata[CONTACT_URL_FIELD] in person :
		address=metadata[CONTACT_URL_FIELD]
	else :
		address=''
		
	return ' '.join([date,person,address])


def get_license(metadata,licenses_files,included_license=True):
	if metadata[RIGHTS_FIELD]==metadata[RIGHTS_URL_FIELD] :
		license=metadata[RIGHTS_FIELD]
	elif metadata[RIGHTS_FIELD]==meta_others.LOCAL_LICENSE :
		license_path=metadata[RIGHTS_URL_FIELD]
		if license_path in licenses_files :
			license=licenses_files[license_path]
		else :
			if included_license :
				license="L-"+str(len(licenses_files)+1)
			else :
				license=license_path
			licenses_files[license_path]=license
	else :
		license=' '.join([metadata[RIGHTS_FIELD],metadata[RIGHTS_URL_FIELD]])
				
	return license
	
	
def get_comment(metadata):
	comment=''
	if metadata[OWNER_FIELD] and metadata[CREATOR_FIELD]:
		comment+="Creator[{}] ".format(metadata[CREATOR_FIELD])
	if metadata[CONTRIBUTORS_FIELD] :
		comment+="Contributors[{}] ".format(metadata[CONTRIBUTORS_FIELD])
	if metadata[SOFTWARE_FIELD] :
		comment+="Software Used[{}] ".format(metadata[SOFTWARE_FIELD])
	if metadata[SOURCE_FIELD] :
		comment+="Work Based On[{}] ".format(metadata[SOURCE_FIELD])
	return comment
	


def write_debian_copyright(db,output_file,included_license=True):
	licenses_files={}
	with open(output_file,'w',newline='') as copyright_file :
		### write_header
		copyright_file.write("Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n")
		copyright_file.write("\n")
		for item in sorted(db.items()) :
			pathname=item[0]
			metadata=item[1]
			copyright_file.write("\n")
			copyright_file.write("Files: {}\n".format(pathname))
			copyright_file.write("Copyright: {}\n".format( get_copyright(metadata)) )
			copyright_file.write("License: {}\n".format( get_license(metadata,licenses_files,included_license)) )
			copyright_file.write("Comment: {}\n".format( get_comment(metadata)) )
		copyright_file.write("\n")
		if included_license :
			for license in licenses_files :
				copyright_file.write("\n")
				copyright_file.write("License: {}\n".format( licenses_files[license] ))
				with open(license,'r',newline='') as lf :
					for line in lf.readlines() :
						if not line=="\n" :
							line='\t'+line#.replace('\n','\n\t')
						else :
							line='\t.\n'
						copyright_file.write(line)
			
			
			
