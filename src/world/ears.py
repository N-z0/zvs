#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Ear class"#information describing the purpose of this module
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
#import numpy

### PyOpenAL require an OpenAL shared library
#import openal

### commonz imports
from commonz.constants import *
from commonz.ds import array

### local imports
from . import items



class Ear(items.Item):
	"""manage a place of listening"""
	def __init__(self,volume,active,position,orientation,scale):
		"""volume is the general sound gain"""
		items.Item.__init__(self,active,position,orientation,scale)
		
		self.volume=volume
		
		### i know its ugly
		### but i want see all class atributs in init
		### for the absolute calculation of vectors
		self.position_vector=array.vector( 0,0,0,1 )
		self.front_vector=array.vector( 0,0,-1,0 )
		self.up_vector=array.vector( 0,1,0,0 )
		self.new_position=None
		self.old_position=None
	
	
	def is_open(self):
		"""return True if the ear is enable or False if disabled"""
		return self.active
	
	
	def set_volume(self,volume=None):
		"""change gain of sound"""
		if volume is not None :
			self.volume= volume
	
	
	def get_volume(self):
		"""retrieve the gain of sound"""
		return self.volume
	
	def get_vector_position(self):
		"""retrieve the position vector"""
		self.old_position=self.new_position
		position= self.abs_mod_mat.dot( self.position_vector )
		self.new_position= array.vector( position[X],position[Y],position[Z] )
		return self.new_position
	
	def get_vector_front(self):
		"""retrieve the front vector"""
		front= self.abs_mod_mat.dot( self.front_vector )
		return array.vector( front[X],front[Y],front[Z] )
	
	def get_vector_up(self):
		"""retrieve the up vector"""
		up= self.abs_mod_mat.dot( self.up_vector )
		return array.vector( up[X],up[Y],up[Z] )
	
	def get_vector_velocity(self):
		"""retrieve the velocity vector"""
		if self.old_position is not None :
			velocity= self.new_position-self.old_position
		else :
			velocity= array.vector( 0,0,0 )
		return velocity

