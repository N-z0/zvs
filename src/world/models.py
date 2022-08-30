#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Models class"#information describing the purpose of this module
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

### OpenGL imports
from OpenGL import GL as gl
#from OpenGL.GL import shaders
#from OpenGL import GLU as glu
#from OpenGL import GLE as gle
#from OpenGL.GL.ARB.multitexture import *#
#from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays,glBindVertexArray#

### commonz imports
#from commonz.constants import *
#from commonz.ds import array



class Model:
	"""the combination of mesh texture and material for the items"""
	def __init__(self,mesh,obj_name,group_name,emit_tex,ao_tex,albedo_tex,smooth_tex,metal_tex,norm_tex,matarials):
		"""if group_name is not provided it will be the first group found"""
		
		self.mesh=mesh
		
		### if no obj_name then find the first object name
		self.obj_name= obj_name or tuple(self.mesh.get_objects_names())[0]
		### if no group_name then find the first group name
		self.group_name= group_name or tuple(self.mesh.get_groups_names(self.obj_name))[0]
		
		self.matarials=matarials
		
		self.emit_texture= emit_tex
		self.ao_texture= ao_tex
		self.albedo_texture= albedo_tex
		self.smooth_texture= smooth_tex
		self.metal_texture= metal_tex
		self.normal_texture= norm_tex
	
	
	def render_draw(self,shader,model_matrix):
		"""draw the 3d shape in the virtual world"""
		
		### give the model_matrix to the shader
		loc = gl.glGetUniformLocation(shader.index, 'model_matrix')
		gl.glUniformMatrix4fv(loc, 1, True, model_matrix )
		
		### select all the textures
		self.emit_texture.select()
		self.ao_texture.select()
		self.albedo_texture.select()
		self.smooth_texture.select()
		self.metal_texture.select()
		self.normal_texture.select()
		
		### for the group_name get each materials library
		for mat_lib_name in self.mesh.get_matlibs_names(self.obj_name,self.group_name) :
			#print('model mat_lib_name:',mat_lib_name)
			### for each materials library get each materials
			for material_name in self.mesh.get_materials_names(self.obj_name,self.group_name,mat_lib_name) :
				#print('model material_name:',material_name)
				### get the material object and give the the shader the attributes
				m=self.matarials[mat_lib_name].get(material_name)
				gl.glUniform4fv(gl.glGetUniformLocation(shader.index,"material.base"), 1, m.base)
				gl.glUniform4fv(gl.glGetUniformLocation(shader.index,"material.emit"), 1, m.emit)
				gl.glUniform1fv(gl.glGetUniformLocation(shader.index,"material.shine"), 1, m.shine)
				gl.glUniform1fv(gl.glGetUniformLocation(shader.index,"material.ao"), 1, m.ao)
				### ask to draw the specified designated mesh
				self.mesh.draw(object_name=self.obj_name,group_name=self.group_name,mat_lib_name=mat_lib_name,material_name=material_name)
	
	
	def set_group(self,group_name=None):
		"""change the group that will be draw"""
		if group_name is not None :
			self.group_name=group_name

