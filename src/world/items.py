#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Items class"#information describing the purpose of this module
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



class Item:
	"""
	items are good for placing others Items,
	and 3D shape and noise can be attributed on it
	"""
	def __init__(self,active,position,orientation,scale):
		"""placement vectors are necessary"""
		
		self.children={}
		
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
		self.position=None;self.tra_mat=None;self.reckon_position(position)
		self.orientation=None;self.rot_mat=None;self.reckon_orientation(orientation)
		self.scale=None;self.sca_mat=None;self.reckon_dimension(scale)
		### is necessary for calculating the inner relative transformations
		self.rel_mod_mat= None;self.reckon_matrix_relative()
	
	
	def get_child(self,index_list):
		"""retrieve one specific child"""
		if len(index_list)>1 :
			return self.children[index_list[0]].get_child(index_list[1:])
		elif len(index_list)==1 :
			return self.children[index_list[0]]
		else :
			return self
	
	def add_child(self,name,child):
		"""append one specific child"""
		self.children[name]=child
	
	def del_child(self,name):
		"""remove one specific child"""
		del self.children[name]
	
	
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
			self.position= array.vector( new_position )
			self.tra_mat= array.translate_matrix(self.position[X],self.position[Y],self.position[Z])
	
	def reckon_orientation(self,new_orientation=None):
		"""calculation of the rotation"""
		if new_orientation is not None :
			self.orientation= array.quaternion(new_orientation[0],new_orientation[1],new_orientation[2],new_orientation[3])
			self.rot_mat= array.matrix_from_quaternion(self.orientation)
	
	def reckon_dimension(self,new_scale=None):
		"""calculation of the scale"""
		if new_scale is not None :
			self.scale= array.vector( new_scale )
			self.sca_mat= array.scale_matrix(self.scale[X],self.scale[Y],self.scale[Z])
	
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
	
	
	def reckon_matrix_absolute(self,mod_mat,view_mat):
		"""calculation of absolute matrix transformation"""
		self.abs_mod_mat= mod_mat @ self.rel_mod_mat
		self.view_mat= numpy.linalg.inv(self.rot_mat) @ numpy.linalg.inv(self.tra_mat) @ view_mat
	
	def set_transformation_absolute(self,mod_mat,view_mat):
		"""do absolute transformation calculation for itself and all children"""
		self.reckon_matrix_absolute(mod_mat,view_mat)
		self.changed=False
		for child in self.children.values() :
			if child.get_activity() :
				child.set_transformation_absolute(self.abs_mod_mat,self.view_mat)
	
	def render_calculation(self,mod_mat,view_mat):
		"""check if absolute transformation calculation is necessary"""
		if self.active :
			### check if re-calculation is necessary
			if self.changed :
				self.set_transformation_absolute(mod_mat,view_mat)
			else:
				### changed check will continue on all children
				for child in self.children.values() :
					child.render_calculation(self.abs_mod_mat,self.view_mat)
	
	
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
			for child in self.children.values() :
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
				self.noise.render_sound(self.abs_mod_mat)
			for child in self.children.values() :
				child.render_sound()

