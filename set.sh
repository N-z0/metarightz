#!/bin/bash

### N-z0
### 2019
### v0
### write metadata
### With the use of exiftool
### So exiftool need to be installed
### https://www.sno.phy.queensu.ca/~phil/exiftool/



## check argument
if [ ! $# -eq 2 ]
  then
		echo 'ERROR: need input file path and metadata file'
		exit 1
fi


#echo "filepath:$1 tagfile:$2"
echo "WARNING This will change/replace the metadata of file(s): $1 with $2"
read -p "Are You Sure? [Y/n] " answer
if [[ ! $answer =~ ^[Yy]$ ]]
then
    exit 1
fi


## add metadata
## ExifTool creates a copy of the original file, appending _original to the file name, as a backup.
## To avoid that and modify files directly, use the -overwrite_original option.
#exiftool -tagsFromFile $tagfile $imgfile
exiftool -recurse -forcePrint -progress -overwrite_original -json=$2 $1

