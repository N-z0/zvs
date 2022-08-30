#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Items class"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.1"# version number,date or about last modification made compared to the previous version
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



class Item:
	"""
	items are good for placing others Items,
	and 3D shape and noise can be attributed on it
	"""
	def __init__(self,active,position,orientation,scale):
		"""placement vectors are necessary"""
		
		self.items_list=[]
		
		### if True the attributed 3D shape and noise will be render
		self.active=active
		
		self.model=None
		self.noise=None
		
		### if True it means absolute placement recalculation is needed
		self.changed=True
		
		### its necessary for calculating the absolute transformations in the world
		self.abs_mod_mat= array.identity_matrix()
		self.view_mat= array.identity_matrix()
		
		### i know its ugly
		### but i want see all class atributs in init
		self.position=None;self.tra_mat=None;self.reckon_relative_position(position)
		self.orientation=None;self.rot_mat=None;self.reckon_relative_orientation(orientation)
		self.scale=None;self.sca_mat=None;self.reckon_relative_dimension(scale)
		### is necessary for calculating the inner relative transformations
		self.rel_mod_mat= None;self.reckon_relative_matrix()
	
	
	def add_child(self,child):
		"""append one specific child"""
		self.items_list.append(child)
	
	def del_child(self,child):
		"""remove one specific child"""
		self.items_list.remove(child)
	
	
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
				move_vector = rot_mat.dot( array.vector( position[X],position[Y],position[Z],1 ) )
				move_vector = array.vector( move_vector[X],move_vector[Y],move_vector[Z] )
				self.position += move_vector
			else :
				self.position= array.vector( position[X],position[Y],position[Z] )
			self.tra_mat= array.translate_matrix(self.position[X],self.position[Y],self.position[Z])
	
	def reckon_relative_orientation(self,orientation=None,cumulative=False):
		"""calculation of the rotation"""
		if orientation is not None :
			quaternion= array.quaternion(orientation[0],orientation[1],orientation[2],orientation[3])
			if cumulative is True :
				self.orientation= array.multiply_quaternions(quaternion,self.orientation)
			else :
				self.orientation= quaternion
			self.rot_mat= array.matrix_from_quaternion(self.orientation)
	
	def reckon_relative_dimension(self,scale=None,cumulative=False):
		"""calculation of the scale"""
		if scale is not None :
			scale_vector=array.vector( scale[X],scale[Y],scale[Z] )
			if cumulative is True :
				self.scale *= scale_vector
			else :
				self.scale= scale_vector
			self.sca_mat= array.scale_matrix(self.scale[X],self.scale[Y],self.scale[Z])
	
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
	
	
	def reckon_absolute_matrix(self,mod_mat,view_mat):
		"""calculation of absolute matrix transformation"""
		self.abs_mod_mat= mod_mat @ self.rel_mod_mat
		self.view_mat= numpy.linalg.inv(self.rot_mat) @ numpy.linalg.inv(self.tra_mat) @ view_mat
	
	
	def reckon_absolute_transformation(self,mod_mat,view_mat,spread=False):
		"""check and if necessary do calculation for itself and all children"""
		if self.active :
			### check if re-calculation is necessary
			if self.changed or spread :
				self.reckon_absolute_matrix(mod_mat,view_mat)
				self.changed=False
				spread=True
			### changed check will continue on all children
			for child in self.items_list :
				child.reckon_absolute_transformation(self.abs_mod_mat,self.view_mat,spread)
	
	
	def add_model(self,model):
		"""assign 3d graphic"""
		self.model=model
	
	def set_model(self,group_name):
		"""modify 3d graphic"""
		self.model.set_group(group_name)
	
	def del_model(self):
		"""remove 3d graphic"""
		self.model=None
	
	def render_draw(self,shader):
		"""draw 3d graphic and ask children to do the same"""
		if self.active :
			if self.model is not None :
				self.model.render_draw(shader,self.abs_mod_mat)
			for child in self.items_list :
				child.render_draw(shader)
	
	
	def add_noise(self,noise):
		"""assign 3d sound"""
		self.noise=noise
	
	def set_noise(self,volumes,pitch,playout):
		"""modify 3d sound"""
		self.noise.set_volumes(volumes)
		self.noise.set_pitch(pitch)
		self.noise.set_playout(playout)
	
	def del_noise(self):
		"""remove 3d sound"""
		self.noise=None
	
	def render_sound(self):
		"""play 3d sound and ask children to do the same"""
		if self.active :
			if self.noise is not None :
				self.noise.render_audio(self.abs_mod_mat)
			for child in self.items_list :
				child.render_sound()

