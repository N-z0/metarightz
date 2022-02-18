#!/bin/bash

### N-z0
### 2019
### v0
### delete all metadata
### With the use of exiftool
### So exiftool need to be installed
### https://www.sno.phy.queensu.ca/~phil/exiftool/



## check argument
if [ $# -eq 0 ]
  then
		echo 'ERROR: need to give a path'
		exit 1
fi


echo "WARNING This will remove/delete all the metadata of file(s): $1"
read -p "Are You Sure? [Y/n] " answer
if [[ ! $answer =~ ^[Yy]$ ]]
then
    exit 1
fi


## del metadata
## ExifTool creates a copy of the original file, appending _original to the file name, as a backup.
## To avoid that and modify files directly, use the -overwrite_original option.
exiftool -recurse -progress -all= -overwrite_original $1

