#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Icons class"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.1"# version number,date or about last modification made compared to the previous version
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

### commonz imports
from commonz.constants import *
from commonz.ds import array



class Icon:
	"""
	are good for placing others Icons
	sprites and signal can be on it
	"""
	def __init__(self,active,position,orientation,scale):
		"""placement vectors are necessary"""
		
		self.icons_list=[]
		
		### if True the attributed sprite and noise will be render
		self.active=active
		
		self.sprite=None
		self.signal=None
		
		### if True it means absolute placement recalculation is needed
		self.changed=True
		
		### its necessary for calculating the absolute transformations
		self.abs_mod_mat= array.identity_matrix()
		
		### i know its ugly
		### but i want see all class atributs in init
		self.position=None;self.tra_mat=None;self.reckon_position(position)
		self.orientation=None;self.rot_mat=None;self.reckon_orientation(orientation)
		self.scale=None;self.sca_mat=None;self.reckon_dimension(scale)
		### is necessary for calculating the inner relative transformations of the item
		self.rel_mod_mat= None;self.reckon_matrix_relative()
	
	
	def add_child(self,child):
		"""append one specific child"""
		self.icons_list.append(child)
	
	def del_child(self,child):
		"""remove one specific child"""
		self.icons_list.remove(child)
	
	
	def set_activity(self,activity=None):
		"""change the state"""
		if activity is not None :
			self.active=activity
	
	def get_activity(self):
		"""return the state"""
		return self.active
	
	
	def reckon_position(self,new_position=None):
		"""calculation of the translation"""
		if new_position is not None :
			self.position= array.vector( new_position[X],new_position[Y],-0.5 )
			self.tra_mat= array.translate_matrix(self.position[X],self.position[Y],self.position[Z])
	
	def reckon_orientation(self,new_orientation=None):
		"""calculation of the rotation"""
		if new_orientation is not None :
			self.orientation= new_orientation
			self.rot_mat= array.rotate_matrix((0,0,1),self.orientation)
	
	def reckon_dimension(self,new_scale=None):
		"""calculation of the scale(zoom)"""
		if new_scale is not None :
			self.scale= array.vector( new_scale )
			self.sca_mat= array.scale_matrix(self.scale[X],self.scale[Y],1)
	
	def reckon_matrix_relative(self):
		"""calculation of relative matrix transformation"""
		self.rel_mod_mat= self.tra_mat @ self.rot_mat @ self.sca_mat
	
	def set_transformation_relative(self,position=None,orientation=None,scale=None):
		"""change the optional position orientation scale"""
		if  position is not None  or  orientation is not None  or  scale is not None :
			self.reckon_position(position)
			self.reckon_orientation(orientation)
			self.reckon_dimension(scale)
			self.reckon_matrix_relative()
			self.changed=True
	
	
	def reckon_matrix_absolute(self,mod_mat):
		"""calculation of absolute matrix transformation"""
		self.abs_mod_mat= mod_mat @ self.rel_mod_mat
	
	def set_transformation_absolute(self,mod_mat):
		"""do absolute transformation calculation for itself and all children"""
		self.reckon_matrix_absolute(mod_mat)
		self.changed=False
		for child in self.icons_list :
			if child.get_activity() :
				child.set_transformation_absolute(self.abs_mod_mat)
	
	def render_calculation(self,mod_mat):
		"""check if absolute transformation calculation is necessary"""
		if self.active :
			### check if re-calculation is necessary
			if self.changed :
				self.set_transformation_absolute(mod_mat)
			else:
				### changed check will continue on all children
				for child in self.icons_list :
					child.render_calculation(self.abs_mod_mat)
	
	
	def add_sprite(self,sprite):
		"""assign 2d graphic"""
		self.sprite= sprite
	
	def set_sprite(self,color):
		"""modify 2d graphic"""
		self.sprite.set_color(color)
		
	def del_sprite(self):
		"""delete 2d graphic"""
		self.sprite= None
	
	def render_sprite(self,shader):
		"""draw 2d graphic and ask children to do the same"""
		if self.active :
			if self.sprite is not None :
				self.sprite.render_draw(shader,self.abs_mod_mat)
			for child in self.icons_list :
				child.render_sprite(shader)
	
	
	def add_signal(self,signal):
		"""assign audio signal"""
		self.signal=signal
	
	def set_signal(self,volume,pitch,playout):
		"""modify audio signal"""
		self.signal.set_volume(volume)
		self.signal.set_pitch(pitch)
		self.signal.set_playout(playout)
	
	def del_signal(self):
		"""delete audio signal"""
		self.signal= None
	
	def render_signal(self):
		"""play audio signal and ask children to do the same"""
		if self.active :
			if self.signal is not None :
				self.signal.render_audio()
			for child in self.icons_list :
				child.render_signal()
	
	
	def resize(self,window_size):
		"""change the size of the sprites and ask children to do the same"""
		if self.sprite :
			self.sprite.resize(window_size)
		
		for child in self.icons_list :
			child.resize(window_size)
	
	
