#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the materials resources"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-04-01"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### built-in modules
#import math # for degrees radian covert
import numpy

### commonz imports
#from commonz.constants import *
#from commonz.ds import array
from commonz.datafiles import mtl



class Material:
	"""store the attributes of one material as resource for world items"""
	def __init__(self,atribs):
		"""atribs must be a dictionary containing the material attributes"""
		
		### get attributes from dictionary or a default value
		emit= atribs.get(mtl.KE) or (0,0,0,0) #should be RGBA
		ao= atribs.get(mtl.KA) or (1.0,) # KA should be (1float,) even if historically it was RGB
		base= atribs.get(mtl.KD) #should be RGBA
		shine= atribs.get(mtl.PR) or atribs.get(mtl.NS) # NS PR are 1float
		spec= atribs.get(mtl.KS) or (0.5,) # KS should be (1float,) even if historically it was RGB
		
		### fix values type for direct use by openGL
		self.emit= numpy.array( emit, dtype=numpy.float32 )
		self.base= numpy.array( base, dtype=numpy.float32 )
		self.shine= numpy.array( (shine or spec[0],), dtype=numpy.float32 )
		self.ao= numpy.array( (ao[0],), dtype=numpy.float32 )



class Mat_Lib:
	"""load and store materials from a file"""
	def __init__(self,pathname):
		"""pathname must be a valid mtl file"""
		materials=mtl.load_mtl_file(pathname)
		for name in materials.keys() :
			materials[name]=Material(materials[name])
		self.materials=materials
	
	def get(self,name):
		"""return the specified material"""
		return self.materials[name]

