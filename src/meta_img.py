#!/usr/bin/env python3




#import sys
#import os
from os import path

#from PIL import Image
#from PIL.ExifTags import TAGS
import json
import exiftool

from tags import *



JSON_FILES=["data/tags/useful/describe.json","data/tags/useful/personal.json","data/tags/useful/rights.json"]

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



def get_valu(metadata,tags):
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


def get_img_metadata_pil(pathfile):
	"""not working as well, because just returning the dpi of the images"""
	img = Image.open(pathfile)
	for tag, value in img.info.items():
		key = TAGS.get(tag, tag)
		print(key+" "+str(value))

def get_keys_database():
	keys={}
	prog_path=path.dirname(__file__)
	for json_path in JSON_FILES :
		json_full_path= path.normpath(path.join(prog_path,json_path))
		#print(json_full_path)
		with open(json_full_path, 'r') as f :
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
	
def get_img_metadata(pathfile_list):
	keys=get_keys_database()
	metadata_files={}
	for pathfile in pathfile_list :
		metadata=METADATA.copy()
		with exiftool.ExifTool() as et :
			md=et.get_metadata(pathfile)
			#print(md)
			#metadata[FILE_FIELD]=md[FILE_TAG]
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
			metadata_files[pathfile]=metadata#.append(metadata)
	return metadata_files



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
	print(instags)

	outtags=set([])
	with exiftool.ExifTool() as et :
		md=et.get_tags_batch(instags,fl)
		for d in md :
			outtags.update(d.keys())
	print(outtags)
	
	adapted_instags=set([FILE_TAG])
	for t in instags :
		adapted_instags.add(t)

	### metadata founded - metadata that i wanted
	out=list(outtags-adapted_instags)
	out.sort()

	### metadata that i wanted - metadata founded
	ins=list(adapted_instags-outtags)
	ins.sort()

	if not (out==[] and ins==[]) :
		print("The metadatas founded but not wanted :")
		print(out)
		print()
		print("The metadatas that wanted but not founded :")
		print(ins)


