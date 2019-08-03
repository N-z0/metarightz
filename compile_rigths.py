#!/usr/bin/env python3




#import sys
import os
from os import path
import mimetypes

#from PIL import Image
#from PIL.ExifTags import TAGS
import json
import exiftool
import csv #CSV/TSV File Reading and Writing




DIALECT='unix-tsv'
csv.register_dialect(DIALECT, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)


JSON_FILES="tools/metadatatool/data/tags/templates"
ROOT_PATH="../.."
FILES_PATH="."
OUTPUT_FILE="docs/licenses.tsv"
EXCLUDE_PREFIXES=('__', '.')

LICENSE_FILE="license.md"
LICENSE_TYPE="license"
LOCAL_LICENSE="Rights specified by the local license file"

EXIF_TYPES=('image/png','image/jpeg','image/gif','image/svg+xml','audio/ogg','audio/flac')
TXT_TYPES=('text/markdown','text/plain','text/csv','text/tab-separated-values','application/json')
CODE_TYPES=('text/x-sh','text/x-python')
APP_TYPES=('application/x-xcf')

FILE_TAG='SourceFile'

SOURCE='SOURCE'
SOFTWARE='SOFTWARE'
CREATOR='CREATOR'
CONTRIBUTORS='CONTRIBUTORS'
OWNER='OWNER'
CONTACT_URL='CONTACT_URL'
DATE='YYYY:MM:DD'
RIGHTS='RIGHTS'
RIGHTS_URL='RIGHTS_URL'
KEYS=(SOURCE,SOFTWARE,CREATOR,CONTRIBUTORS,OWNER,CONTACT_URL,DATE,RIGHTS,RIGHTS_URL)

FILE_FIELD="#File"
SOURCE_FIELD="#Source"
SOFTWARE_FIELD="#Software"
CREATOR_FIELD="#Creator"
CONTRIBUTORS_FIELD="#Contributors"
OWNER_FIELD="#Owner"
CONTACT_URL_FIELD="#ContactURL"
DATE_FIELD="#date"
RIGHTS_FIELD="#Rights"
RIGHTS_URL_FIELD="#RightsURL"
HEAD_FIELDS=[FILE_FIELD,DATE_FIELD,SOURCE_FIELD,SOFTWARE_FIELD,CREATOR_FIELD,CONTRIBUTORS_FIELD,OWNER_FIELD,RIGHTS_FIELD,RIGHTS_URL_FIELD,CONTACT_URL_FIELD]


WRN1="WARNING:unknow type: "
WRN2="WARNING:file unlicensed: "
#ERR1="missing code:"
#ERR2="missing :"




def get_valu(metadata,tags):
	valu=""
	for t in tags :
		v=str(metadata.get(t,"")).strip()
		if valu in v :
			valu=v
		elif not v in valu :
			if valu=="" :
				valu=v
			else:
				valu=";".join([valu,v])
	return valu


def get_img_metadata_pil(pathfile):
	"""not working as well, because just returning the dpi of the images"""
	img = Image.open(pathfile)
	for tag, value in img.info.items():
		key = TAGS.get(tag, tag)
		print(key+" "+str(value))

def get_img_metadata(pathfile,keys):
	metadata={}
	with exiftool.ExifTool() as et :
		md=et.get_metadata(pathfile)
		#print(md)
		metadata[FILE_FIELD]=md[FILE_TAG]
		#print(md[FILE_TAG])
		metadata[SOURCE_FIELD]=get_valu(md,keys[SOURCE])
		metadata[SOFTWARE_FIELD]=get_valu(md,keys[SOFTWARE])
		metadata[CREATOR_FIELD]=get_valu(md,keys[CREATOR])
		metadata[CONTRIBUTORS_FIELD]=get_valu(md,keys[CONTRIBUTORS])
		metadata[OWNER_FIELD]=get_valu(md,keys[OWNER])
		metadata[CONTACT_URL_FIELD]=get_valu(md,keys[CONTACT_URL])
		metadata[DATE_FIELD]=get_valu(md,keys[DATE])
		metadata[RIGHTS_FIELD]=get_valu(md,keys[RIGHTS])
		metadata[RIGHTS_URL_FIELD]=get_valu(md,keys[RIGHTS_URL])
	return metadata

def get_file_type(pathfile):
	filename=os.path.basename(pathfile)
	#tip=path.splitext(name)[1]
	tip=mimetypes.guess_type(filename,strict=True)[0]#registered with IANA.
	return tip






def get_all_metadata(fl):
	outtags=set([])
	with exiftool.ExifTool() as et :
		md=et.get_metadata_batch(fl)
		for d in md :
			outtags.update(d.keys())
	return outtags

def get_metadata(fl,tags):
	with exiftool.ExifTool() as et :
		return et.get_tags_batch(tags,fl)


def check_metadata_database(fl,kd):
	instags=set([])
	for k in kd :
		instags.update(kd[k])

	outtags=set([])
	with exiftool.ExifTool() as et :
		md=et.get_tags_batch(instags,fl)
		for d in md :
			outtags.update(d.keys())

	adapted_instags=set([FILE_TAG])
	for t in instags :
		adapted_instags.add(t)


	out=list(outtags-adapted_instags)
	out.sort()

	ins=list(adapted_instags-outtags)
	ins.sort()

	if not (out==[] and ins==[]) :
		print(out)
		print()
		print(ins)







def get_files(root_path=".",exclude_prefixes=EXCLUDE_PREFIXES):
	db=[]
	for root, dirs, files in os.walk(root_path):
		dirs[:] = [d for d in dirs if not d.startswith(exclude_prefixes)]
		files = [f for f in files if not f.startswith(exclude_prefixes)]
		for name in files :
			pathfile=path.normpath(os.path.join(root,name))
			db.append(pathfile)
	return db

def get_keys_database(files_list):
	keys={}
	for p in files_list :
		with open(p, 'r') as f :
			dico = json.load(f)[0]
			for tag in dico :
				key=dico[tag]
				if key in KEYS :
					tag=tag.replace("XMP-xmpRights:","XMP:").replace("XMP-dc:","XMP:").replace("XMP-cc:","XMP:").replace("XMP-tiff:","XMP:").replace("XMP-iptcExt:","XMP:")
					if key in keys :
						keys[key].update([tag])
					else :
						keys[key]=set([tag])
	return keys

def get_metadata_database(path_list,keys_database):
	#print(pathfile_list)

	licenses_path_list=[]
	files_path_list=[]
	for p in path_list :
		if os.path.basename(p)==LICENSE_FILE :
			lp= path.dirname(p)+os.sep
			licenses_path_list.append(lp.lstrip(os.sep))
		else :
			files_path_list.append(p)
	licenses_path_list=sorted(licenses_path_list,reverse=True)
	#print(licenses_path_list)

	db=[]
	for pathfile in files_path_list :
		tip=get_file_type(pathfile)
		if tip in EXIF_TYPES :
			metadata=get_img_metadata(pathfile,keys_database)
		elif tip in TXT_TYPES : 
			continue
		elif tip in CODE_TYPES : 
			continue
		elif tip in APP_TYPES : 
			continue
		else :
			print(WRN1,tip)
			continue

		if not ( metadata[RIGHTS_FIELD] or metadata[RIGHTS_URL_FIELD] ) :
			for license_path in licenses_path_list :
				#print(pathfile,license_path)
				if pathfile.startswith(license_path) :
					#print(pathfile,path.join(license_path,LICENSE_FILE))
					metadata[RIGHTS_FIELD]=LOCAL_LICENSE
					metadata[RIGHTS_URL_FIELD]=path.join(license_path,LICENSE_FILE)
					break
			else :
				print(WRN2,pathfile)

		db.append(metadata)
	return db

def write_tsv_files(db,output_file,head_fields):
	with open(output_file,'w',newline='') as tsv_file :
		tsv_file.write("\t".join(head_fields)+"\n")
		writer = csv.DictWriter(tsv_file,fieldnames=head_fields,dialect=DIALECT)
		for data in db :
			writer.writerow(data)






if __name__ == '__main__':
	progpath= path.dirname(__file__)
	rootpath= path.normpath(path.join(progpath,ROOT_PATH))
	os.chdir(rootpath)
	#print( __file__, progpath, rootpath, FILES_PATH, OUTPUT_FILE )
	
	jl=get_files(JSON_FILES)
	kd=get_keys_database(jl)
	#print(kd.keys())
	fl=get_files(FILES_PATH)
	#print(fl)
	#print(get_metadata(fl,("XMP:CopyrightYear","XMP:DateTime","XMP:Date","XMP:ArtworkDateCreated")))
	#print(get_all_metadata(fl))
	check_metadata_database(fl,kd)
	md=get_metadata_database(fl,kd)
	#print(md)
	write_tsv_files(md,OUTPUT_FILE,HEAD_FIELDS)

