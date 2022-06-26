#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide interface for the main module."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-05-1"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### builtin modules
import os # use for exit status and path separators

### commonz modules
from commonz import logger
from commonz.fs import pathnames#,checks,actions

### local modules
import main
#from writers import *
from writers import write_tsv
from writers import write_deb



LOCAL_LICENSE_TEXT="Rights specified by the local license file"



class Application():
	"""software application as object"""
	def __init__(self,prog_name,cfg,dirs,data_pathnames,env):
		"""initialization of the application"""
		
		### setup names
		self.prog_name=prog_name
		self.user_name=env['USER']
		
		### setup path 
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		
		### store configuration settings parameters
		input_cfg=cfg['INPUT']
		self.directory=input_cfg['directory']
		self.license=input_cfg['licenses']
		self.exclude=input_cfg['exclude']
		
		default_cfg=cfg['DEFAULT']
		self.default_owner=default_cfg['owner']
		self.default_contact=default_cfg['contact']
		
		output_cfg=cfg['OUTPUT']
		self.output_file=output_cfg['output']
		self.output_print=output_cfg['print']
		self.output_format=output_cfg['format']
		self.file_date=output_cfg['timestamp']
		self.glob=output_cfg['all']
		
		### keep datafiles
		self.data_pathnames= data_pathnames
	
	
	def run(self):
		"""operates the application object"""
		
		### get list of files
		logger.log_debug(6)
		files_list=pathnames.get_recursive_content(self.directory,includ_files=True,includ_directories=False,fullpath=False)
		
		### filter the list of files
		filtred_files_list=files_list.copy()
		for exlu in self.exclude.split(os.sep) :
			filtred_files_list= [ p for p in filtred_files_list if not exlu in p.split(os.sep) ]
		filtred_quantum=len(files_list)-len(filtred_files_list)
		logger.log_info(7,[filtred_quantum])
		
		### put in different directory licenses files and others files, including the fullpath
		license_items={}
		regular_items={}
		for file_index in filtred_files_list :
			file_path= pathnames.join_pathname(self.directory,file_index)
			if pathnames.get_name(file_index)==self.license :
				license_items[file_index]=file_path
			else :
				regular_items[file_index]=file_path
		logger.log_info(8,[len(license_items.keys())])
		logger.log_info(9,[len(regular_items.keys())])
		
		### get the metadata
		md=main.get_metadata_database(regular_items,license_items,self.default_owner,self.default_contact,self.file_date,self.glob,self.data_pathnames,LOCAL_LICENSE_TEXT)
		
		### output result
		if self.output_print :
			logger.log_info(10)
			self.print_output(md)
		### or write the output in file
		elif self.output_format=="tsv" :
			logger.log_info(11,[self.output_file])
			write_tsv.write_tsv_files(md,self.output_file)
		elif self.output_format=="deb" :
			logger.log_info(12,[self.output_file])
			write_deb.write_debian_copyright(self.directory,md,self.output_file,LOCAL_LICENSE_TEXT,included_license=True)#False
		
		### exit
		return os.EX_OK


	def print_output(self,database):
		"""print on terminal the metadata output of files"""
		for key in sorted(database.keys()) :
			data=database[key]
			for key in data.keys() :
				if data[key] :
					print(key,":",data[key])
			print("\n")

