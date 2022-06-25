![Logo icon](contents/logo/logo.svg "Software-name logo")
# MetaRightz
**get from files copyrights**


## 📋 Glossary
*metadata schema types:*

 - IPTC  
	Often called "legacy" IPTC.
	
 - Exif  
	These metadata are often created by cameras and other capture devices.
	Including technical information about photo capture method, 
	such as exposure settings, capture time, GPS location information and camera model.
	Older than XMP, not supporting Unicode and not supported by JPEG 2000 or PNG file format.
	
 - XMP  
	The most recent,made by Adobe but opensource,
	Supporting Unicode and unlimited metadata..
	
 - Dublin Core  
	Metadata schema use by many image libraries and a wide variety of industries
	for the store of image information.
	Several of its fields are inter operable with IPTC formats.


## ℹ️ Description
The goal of this project is to get from files the related license and copyrights metadata,
With the the option to write those collected data into a *cvs* or *deb* file.

There is many existing software for set and get metadata,
but not easy to find one with large wide metadata scope*(all metadata types)* 
and who can make *csv/tsv* output reports.

Also, it include metadata from dedicated license.md files found in your project.

Currently this software require [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool)


## 👉 References:
 - [iptc-standard](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata)  
	Photo Metadadata Standard 2017.1, including:
	 - IPTC Core Metadata Schema 1.2
	 - IPTC Extension Metadata Schema 1.4
 - [MWG specification](http://www.metadataworkinggroup.org/ )  
	The Metadata Working Group (MWG) 
	recommends techniques to allow certain overlapping EXIF, IPTC and XMP tags
	To be reconciled when reading, and synchronized when writing.
 - Creative Commons official recommendation  
	Concerning XMP metadata information
	is to use identical content for the dc:rights and xmpRights:UsageTerms fields.
	Also xmpRights:Marked should be set to False if Public Domain, True otherwise.
 - PNG metadata  
	The iTXt, tEXt, and zTXt chunks (text chunks) 
	are used for conveying textual information associated with the image. 
	They are the places we can find all metadata of PNG file.
	Each of the text chunks contains as its first field a keyword that indicates the type of information represented by the text string. 
	Other keywords may be invented for other purposes.
	The keyword must be at least one character and less than 80 characters long.
	According to XMP Specification,
	an XMP packet is embedded in a PNG graphic file by adding a chunk of type iTXt 
	with the keyword 'XML:com.adobe.xmp'.
	But there are no standard for Exif, IPTC data. In Exiv2, 
	when Exif, IPTC are added, they are stored in zTXt text chunks and save as ASCII.


## 👀 See also:
 - [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool)  
	ExifTool is a platform-independent Perl library plus a command-line application
	for reading, writing and editing meta information in a wide variety of files.
 - [pyexiftool](https://github.com/smarnach/pyexiftool)  
	PyExifTool is a Python library
	to communicate with an instance of Phil Harvey's ExifTool command-line application.
 - [exiv2](https://www.exiv2.org/index.html)  
	C++ metadata library and tools.
 - [pyexiv2](https://pypi.org/project/pyexiv2/)  
	It runs on C++ API of exiv2. 
	for read and modify metadata of digital image, including EXIF, IPTC, XMP. It 


## 📜 History
 - Origin:  
	Project initiate by [Nz0](https://github.com/N-z0) .

 - Development:  
	- Hosted  on [GitHub](https://github.com/N-z0/metarightz.git)
