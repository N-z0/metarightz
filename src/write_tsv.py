#!/usr/bin/env python3



import csv #CSV/TSV File Reading and Writing

from tags import *



DIALECT='unix-tsv'
csv.register_dialect(DIALECT, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)

HEAD_FIELDS=[FILE_FIELD,DATE_FIELD,SOURCE_FIELD,SOFTWARE_FIELD,CREATOR_FIELD,CONTRIBUTORS_FIELD,OWNER_FIELD,RIGHTS_FIELD,RIGHTS_URL_FIELD,CONTACT_URL_FIELD]



def write_tsv_files(db,output_file):
	with open(output_file,'w',newline='') as tsv_file :
		tsv_file.write("\t".join(HEAD_FIELDS)+"\n")
		writer = csv.DictWriter(tsv_file,fieldnames=HEAD_FIELDS,dialect=DIALECT)
		for item in sorted(db.items()) :
			pathname=item[0]
			metadata=item[1]
			metadata[FILE_FIELD]=pathname
			#print("DATA:",data)
			writer.writerow(metadata)

