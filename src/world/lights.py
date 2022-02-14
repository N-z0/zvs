#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Light class"#information describing the purpose of this module
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
from commonz.constants import *
from commonz.ds import array

### local imports
from . import items



class Light(items.Item):
	"""manage a place emitting light"""
	def __init__(self,ambient,diffuse,active,position,orientation,scale):
		"""the orientation rotate the light direction"""
		items.Item.__init__(self,active,position,orientation,scale)
		
		### for the absolute calculation of vectors
		self.position_vector= array.vector( 0,0,0,1 )
		self.direction_vector= array.normalized_vector( 0,0,-1,0 )
		
		### i know its ugly
		### but i want see all class attributes in init
		self.ambient= None; self.set_color_ambient(ambient)
		self.diffuse= None; self.set_color_diffuse(diffuse)
	
	
	def is_active(self):
		"""return True if the light is enable or False if disabled"""
		return self.active
	
	
	def set_color_ambient(self,new_ambient=None):
		"""change the added color surrounding the objects"""
		if new_ambient is not None :
			self.ambient= numpy.array( new_ambient, dtype=numpy.float32 )
	
	def set_color_diffuse(self,new_diffuse=None):
		"""change the diffuse color added to object directly exposed"""
		if new_diffuse is not None :
			self.diffuse= numpy.array( new_diffuse, dtype=numpy.float32 )
	
	
	def get_vector_position(self):
		"""retrieve the vector of the light position"""
		position= self.abs_mod_mat.dot( self.position_vector )
		return array.vector( position[X],position[Y],position[Z] )
	
	def get_vector_direction(self):
		"""retrieve the vector of the light direction"""
		direction= self.abs_mod_mat.dot( self.direction_vector )
		return array.vector( direction[X],direction[Y],direction[Z] )
	
	
	def get_color_ambient(self):
		"""retrieve the added color surrounding the objects"""
		return self.ambient
	
	def get_color_diffuse(self):
		"""retrieve the diffuse color added to object directly exposed"""
		return self.diffuse
	
	