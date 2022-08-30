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
		self.position=None;self.tra_mat=None;self.reckon_relative_position(position)
		self.orientation=None;self.rot_mat=None;self.reckon_relative_orientation(orientation)
		self.scale=None;self.sca_mat=None;self.reckon_relative_dimension(scale)
		### is necessary for calculating the inner relative transformations
		self.rel_mod_mat= None;self.reckon_relative_matrix()
	
	
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
	
	
	def reckon_relative_position(self,position=None,cumulative=False):
		"""calculation of the translation"""
		if position is not None :
			if cumulative is True :
				rot_mat= array.matrix_from_quaternion( array.normalise_quaternion(self.orientation) )
				move_vector = rot_mat.dot( array.vector( position[X],position[Y],0,1 ) )
				move_vector = array.vector( move_vector[X],move_vector[Y],0 )
				self.position += move_vector
			else :
				self.position= array.vector( position[X],position[Y],-0.5 )
			self.tra_mat= array.translate_matrix(self.position[X],self.position[Y],self.position[Z])
	
	def reckon_relative_orientation(self,orientation=None,cumulative=False):
		"""calculation of the rotation"""
		if orientation is not None :
			if cumulative is True :
				self.orientation += orientation
			else :
				self.orientation = orientation
			self.rot_mat= array.rotate_matrix((0,0,1),self.orientation)
	
	def reckon_relative_dimension(self,scale=None,cumulative=False):
		"""calculation of the scale(zoom)"""
		if scale is not None :
			scale_vector=array.vector( scale[X],scale[Y],1 )
			if cumulative is True :
				self.scale *= scale_vector
			else :
				self.scale= scale_vector
			self.sca_mat= array.scale_matrix(self.scale[X],self.scale[Y],1)
	
	
	def reckon_relative_matrix(self):
		"""calculation of relative matrix transformation"""
		self.rel_mod_mat= self.tra_mat @ self.rot_mat @ self.sca_mat
	
	def reckon_relative_transformation(self,position=None,orientation=None,scale=None,cumulative=False):
		"""change the optional position orientation scale"""
		if  position is not None  or  orientation is not None  or  scale is not None :
			self.reckon_relative_position(position,cumulative)
			self.reckon_relative_orientation(orientation,cumulative)
			self.reckon_relative_dimension(scale,cumulative)
			self.reckon_relative_matrix()
			self.changed=True
	
	
	def reckon_absolute_matrix(self,mod_mat):
		"""calculation of absolute matrix transformation"""
		self.abs_mod_mat= mod_mat @ self.rel_mod_mat
	
	
	def reckon_absolute_transformation(self,mod_mat,spread=False):
		"""check and if necessary do calculation for itself and all children"""
		if self.active :
			### check if re-calculation is necessary
			if self.changed or spread :
				self.reckon_absolute_matrix(mod_mat)
				self.changed=False
				spread=True
			### changed check will continue on all children
			for child in self.icons_list :
				child.reckon_absolute_transformation(self.abs_mod_mat,spread)
	
	
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
	
	
