#!/bin/bash

### N-z0
### 2019
### v0
### read metadata
### With the use of exiftool
### So exiftool need to be installed
### https://www.sno.phy.queensu.ca/~phil/exiftool/



## check argument
if [ $# -eq 0 ]
  then
		echo 'ERROR: need to give a path'
		exit 1
fi


## read metadata
exiftool -args -recurse -groupHeadings -dateFormat %Y%m%d $1

