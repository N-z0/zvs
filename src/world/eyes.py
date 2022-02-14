#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Eye class"#information describing the purpose of this module
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
import math # for degrees radian covert
import numpy

### commonz imports
from commonz.constants import *
from commonz.ds import array

### local imports
from . import items



class Eye(items.Item):
	"""manage a place of visioning"""
	def __init__(self,window_size,frame_position,frame_size,size,scope,focal,see,position,orientation,scale):
		"""window_size is necessary for calculating the absolute sizes and positions"""
		items.Item.__init__(self,see,position,orientation,scale)
		
		self.size= size/2
		self.scope=scope
		
		### i know its ugly
		### but i want see all class atributs in init
		self.frame_position=None;self.set_frame_position(frame_position)
		self.frame_size=None;self.set_frame_size(frame_size)
		self.start=None;self.set_focal(focal)
		self.aspect=None;self.reckon_aspect(window_size)
		self.projection_matrix=None;self.reckon_matrix_projection()
	
	
	def is_open(self):
		"""return True if the eye is enable or False if disabled"""
		return self.active
	
	
	def resize(self,window_size):
		"""change the eye projection according to the new window size"""
		self.reckon_aspect(window_size)
		self.reckon_matrix_projection()
	
	def set_projection(self,window_size,frame_size=None,focal=None):
		"""change the eye projection according to the parameters"""
		self.set_frame_size(frame_size)
		self.set_focal(focal)
		if frame_size is not None :
			self.reckon_aspect(window_size)
		if  frame_size is not None  or  focal is not None  :
			self.reckon_matrix_projection()
	
	
	def set_frame_position(self,new_position=None):
		"""change the position of the view area in the window"""
		if new_position is not None :
			self.frame_position= array.vector( new_position )
	
	def set_frame_size(self,new_size=None):
		"""change the size of the view area in the window"""
		if new_size is not None :
			self.frame_size= array.vector( new_size )
	
	def set_focal(self,angle=None):
		"""change the angle of view (need to be in radian)"""
		if angle is not None :
			self.start= self.size / math.tan(angle/2)
	
	
	def reckon_aspect(self,window_size):
		"""calculation of the width and height ratio of the view area"""
		size= window_size * self.frame_size
		#self.aspect= array.normalized_vector(size) * self.size
		self.aspect= size/numpy.max(size) * self.size
	
	def reckon_matrix_projection(self):
		"""calculation of the projection matrix"""
		
		### deprecated
		#glFrustum(0-self.format[X],self.format[X],0-self.format[Y],self.format[Y],self.clip_start,self.clip_end)
		#gluPerspective(self.focal,self.format,self.start,self.end)
		#glOrtho(0-format[X],format[X],0-format[Y],format[Y],self.clip_start,self.clip_end)
		#gluOrtho2D(0,-0.5 0, -1 )#deprecated
		
		self.projection_matrix= array.frustum_matrix(0-self.aspect[X],self.aspect[X],0-self.aspect[Y],self.aspect[Y],self.start,self.start+self.scope)
		#self.projection_matrix= array.perspective_matrix(self.focal, self.aspect, self.clip[0],self.clip[1])
	
	
	def get_frame_position(self):
		"""retrieve the position of the view area"""
		return self.frame_position
	
	def get_frame_size(self):
		"""retrieve the size of the view area"""
		return self.frame_size
	
	
	def get_matrix_projection(self):
		"""retrieve the projection matrix"""
		return self.projection_matrix
	
	def get_matrix_view(self):
		"""retrieve the view matrix"""
		return self.view_mat
	
	