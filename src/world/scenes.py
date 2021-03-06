#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Scene class"#information describing the purpose of this module
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

### OpenGL imports
from OpenGL import GL as gl
#from OpenGL.GL import shaders
#from OpenGL import GLU as glu
#from OpenGL import GLE as gle
#from OpenGL.GL.ARB.multitexture import *#
#from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays,glBindVertexArray#

### PyOpenAL require an OpenAL shared library
import openal

### commonz imports
from commonz import logger
from commonz.constants import *
#from commonz.ds import array

### local imports
from . import items



class Scene(items.Item) :
	"""Scene are the root item of any 3d worlds"""
	def __init__(self,shader,background_color,fog_color,blend_factor,position,orientation,scale):
		"""position orientation scale are normally not necessary"""
		items.Item.__init__(self,True,position,orientation,scale)
		
		self.shader=shader
		
		self.eyes_list= []
		self.lights_list= []
		self.ears_list= []
		
		### i know its ugly
		### but i want see all class attributes in init
		self.fog_color=None;self.set_fog_color(fog_color)
		self.background_color=None;self.set_background_color(background_color)
		self.blend_factor=None;self.set_blend_factor(blend_factor)
	
	
	def display(self,window_size,log_context):
		"""display all children items"""
		
		### update absolute matrix of moved items
		logger.log_debug(75,context=log_context)
		self.render_calculation(self.abs_mod_mat,self.view_mat)
		
		logger.log_debug(76,context=log_context)
		self.render_item_sound()
		
		logger.log_debug(77,context=log_context)
		self.render_item_draw(window_size)
	
	def render_item_draw(self,window_size):
		"""draw all 3d graphic of the items"""
		
		### glClear values
		#gl.glClearDepth(1.0)# depth buffer value on clear, The default value is 1
		gl.glClearColor(self.background_color[R],self.background_color[G],self.background_color[B],self.background_color[A])# color for the COLOR_BUFFER
		#gl.glClearStencil(0)  #Specifies the index used when the stencil buffer is cleared. The initial value is 0.
		#gl.glClearAccum(0,0,0,0)
		
		### clear buffers
		gl.glClear( gl.GL_COLOR_BUFFER_BIT )
		gl.glClear( gl.GL_DEPTH_BUFFER_BIT )
		#gl.glClear( gl.GL_STENCIL_BUFFER_BIT )
		#gl.glClear( gl.GL_ACCUM_BUFFER_BIT )
		
		### choice between speed and quality of rendering : GL_FASTEST GL_DONT_CARE GL_NICEST
		### maybe deprecated and useless
		gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)
		#gl.glHint(gl.GL_POINT_SMOOTH_HINT,gl.GL_NICEST)
		gl.glHint(gl.GL_POLYGON_SMOOTH_HINT,gl.GL_NICEST)
		#gl.glHint(gl.GL_FOG_HINT,gl.GL_NICEST)
		#gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT,gl.GL_NICEST)
		#gl.glHint(gl.GL_GENERATE_MIPMAP_HINT,gl.GL_NICEST)
		
		### anti-aliasing
		### need to enable Blending
		### maybe deprecated and useless
		gl.glDisable(gl.GL_POLYGON_SMOOTH)#polygon smoothing display gaps between polygons
		gl.glEnable(gl.GL_LINE_SMOOTH)
		#gl.glEnable(gl.GL_POINT_SMOOTH)
		
		### set an offset for drawing points n lines above polygons and Width
		### maybe deprecated and useless
		gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
		gl.glEnable(gl.GL_POLYGON_OFFSET_LINE)
		gl.glEnable(gl.GL_POLYGON_OFFSET_POINT)
		gl.glPolygonOffset(-10.,-10.)#
		gl.glLineWidth(1)# pixel width
		gl.glPointSize(3)# pixel width
		
		### specify individual color components in frame buffer that can or not be written.
		gl.glColorMask(gl.GL_TRUE,gl.GL_TRUE,gl.GL_TRUE,gl.GL_TRUE)
		
		### removal of hidden faces
		gl.glFrontFace(gl.GL_CCW)#choose how is the FRONT FACE, GL_CW clockwise or GL_CCW counter-clockwise (the default)
		gl.glCullFace(gl.GL_BACK)#face not to show
		gl.glEnable(gl.GL_CULL_FACE)#enable the hide of face for not translucent objects
		gl.glDisable(gl.GL_CULL_FACE)# disable the hide of hidden faces for translucent objects
		
		### depth filter
		gl.glEnable(gl.GL_DEPTH_TEST)#enable pixel depth test
		#gl.glDisable(gl.GL_DEPTH_TEST)# for translucent objects
		gl.glDepthMask(gl.GL_TRUE)#pecifies whether the depth buffer is enabled for writing. If flag is GL_FALSE, depth buffer writing is disabled.
		#gl.glDepthMask(gl.GL_FALSE)#pecifies whether the depth buffer is enabled for writing. If flag is GL_FALSE, depth buffer writing is disabled.
		gl.glDepthFunc(gl.GL_LEQUAL) # The Type Of Depth Test To Do ,  GL_LESS par defaut
		gl.glDepthRange(0,1) # 0,1 is the default
		
		### blending
		#gl.glEnable(gl.GL_BLEND)
		gl.glDisable(gl.GL_BLEND)
		gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )#Transparency is best implemented using (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		###
		gl.glDisable(gl.GL_COLOR_LOGIC_OP)# To enable or disable the glLogicOp
		gl.glLogicOp(gl.GL_AND)# specifies logical operation between the incoming color and the color at the corresponding location in the frame buffer
		
		### Stencil
		#gl.glDisable(gl.GL_STENCIL_TEST)
		#gl.glStencilFunc(gl.GL_ALWAYS,1,1)
		#gl.glStencilOp(gl.GL_KEEP,gl.GL_REPLACE,gl.GL_REPLACE)
		
		### select shader for drawing
		gl.glUseProgram(self.shader.index)# don't forget to activate the shader before setting uniforms!
		
		### textures
		textures_list=("emissive_texture","ao_texture","base_texture","highlight_texture","metal_texture","normal_texture")
		for index in range(len(textures_list)) :
			loc = gl.glGetUniformLocation(self.shader.index,textures_list[index])
			gl.glUniform1i(loc,index) # set it manually
			#ourShader.setInt("texture2", 1) # or with shader class
		
		### fog
		location = gl.glGetUniformLocation(self.shader.index,"fog")
		gl.glUniform4fv(location, 1, self.fog_color)
		
		### blend 0 = only pure material is draw, 1 = texture fully cover the object
		location = gl.glGetUniformLocation(self.shader.index,"blend_factor")
		gl.glUniform1fv(location, 1, self.blend_factor)
		
		### EYE
		for eye in self.eyes_list :
			if eye.is_open() :
				
				eye_frame_position=eye.get_frame_position()
				eye_frame_size=eye.get_frame_size()
				frame_position=(int(eye_frame_position[X]*window_size[X]),int(eye_frame_position[Y]*window_size[Y]))
				frame_size=(int(eye_frame_size[X]*window_size[X]),int(eye_frame_size[Y]*window_size[Y]))
				
				gl.glViewport(frame_position[X],frame_position[Y],frame_size[X],frame_size[Y])
				
				loc = gl.glGetUniformLocation(self.shader.index, 'view_matrix')
				gl.glUniformMatrix4fv(loc, 1, True, eye.get_matrix_view() )
				
				loc = gl.glGetUniformLocation(self.shader.index, 'projection_matrix')
				gl.glUniformMatrix4fv(loc, 1, True, eye.get_matrix_projection() )
				
				### for each light, the scene is redrawn, eventually adding more colors to the pixels.
				### for now only one light is considered
				for light in self.lights_list :
					if light.is_active() :
						atribs={}
						#atribs["light_vector"]=light.get_position()
						atribs["light_vector"]=light.get_vector_direction()
						atribs["light.ambient"]=light.get_color_ambient()
						atribs["light.diffuse"]=light.get_color_diffuse()
						for a in atribs :
							location = gl.glGetUniformLocation(self.shader.index, a)
							gl.glUniform3fv(location, 1, atribs[a])
							
				### draw the scene objects
				self.render_draw(self.shader)
		
		### unselect shader
		gl.glUseProgram(0)
		
		### finish the draw
		#gl.glFlush()
	
	def render_item_sound(self):
		"""play all 3d sound of the items"""
		
		openal.alDistanceModel( openal.AL_EXPONENT_DISTANCE )#The default distance model is AL_INVERSE_DISTANCE_CLAMPED
		#openal.alDopplerFac(1)#The default Doppler factor is 1
		#openal. alSpeedOfSound(343.3)# The default speed of sound is 343.3
		
		### for each Listeners
		### for now only one ear is considered
		for ear in self.ears_list :
			if ear.is_open() :
				volume= ear.get_volume()
				position_vector= ear.get_vector_position()
				front_vector= ear.get_vector_front()
				up_vector= ear.get_vector_up()
				velocity_vector= ear.get_vector_velocity()
				
				orientation_vector=numpy.concatenate([front_vector,up_vector])
				
				listener= openal.oalGetListener()
				listener.set_gain(volume)
				listener.set_position(position_vector)
				listener.set_orientation(orientation_vector)
				listener.set_velocity(velocity_vector)
		
		### play scene objects sounds
		self.render_sound()
	
	
	def set_background_color(self,background_color=None):
		"""change the color of where nothing is draw"""
		if background_color is not None :
			self.background_color= background_color
	
	def set_fog_color(self,fog_color=None):
		"""change the fog color and opacity"""
		if fog_color is not None :
			self.fog= numpy.array( fog_color, dtype=numpy.float32 )
	
	def set_blend_factor(self,blend_factor=None):
		"""change the blending factor between material and textures of objects"""
		if blend_factor is not None :
			self.blend_factor= numpy.array( (blend_factor,), dtype=numpy.float32 )
		
	
	def add_light(self,index_list,light):
		"""append a light item"""
		parent= self.get_child(index_list[:-1])
		parent.add_child(index_list[-1],light)
		self.lights_list.append(light)
	
	def set_light(self,index_list,ambient_color,diffuse_color):
		"""change light item parameters"""
		light= self.get_child(index_list)
		light.set_color_ambient(ambient_color)
		light.set_color_diffuse(diffuse_color)
	
	def del_light(self,index_list):
		"""remove a specified light item"""
		parent= self.get_child(index_list[:-1])
		light= parent.get_child(index_list[-1])
		self.lights_list.remove(light)
		parent.del_child(index_list[-1])
	
	
	def add_eye(self,index_list,eye):
		"""append an eye item"""
		parent= self.get_child(index_list[:-1])
		parent.add_child(index_list[-1],eye)
		self.eyes_list.append(eye)
	
	def set_eye(self,items_index,window_size,frame_position,frame_size,focal):
		"""change eye item parameters"""
		eye= self.get_child(items_index)
		eye.set_frame_position(frame_position)
		eye.set_projection(window_size,frame_size,focal)
	
	def del_eye(self,index_list):
		"""remove a specified eye item"""
		parent= self.get_child(index_list[:-1])
		eye= parent.get_child(index_list[-1])
		self.eyes_list.remove(eye)
		parent.del_child(index_list[-1])
	
	
	def resize(self,window_size):
		"""change the frame size for the eyes"""
		for eye in self.eyes_list :
			eye.resize(window_size)
	
	
	def add_ear(self,index_list,ear):
		"""append an ear item"""
		parent= self.get_child(index_list[:-1])
		parent.add_child(index_list[-1],ear)
		self.ears_list.append(ear)
	
	def set_ear(self,items_index,volume):
		"""change ear item parameters"""
		ear= self.get_child(items_index)
		ear.set_volume(volume)
	
	def del_ear(self,index_list):
		"""remove a specified ear item"""
		### first remove from the list
		parent= self.get_child(index_list[:-1])
		ear= parent.get_child(index_list[-1])
		self.ears_list.remove(ear)
		parent.del_child(index_list[-1])
	
	
	def add_item_child(self,index_list,child):
		"""append a child"""
		parent= self.get_child(index_list[:-1])
		parent.add_child(index_list[-1],child)
	
	def set_item(self,index_list,activity,position,orientation,scale):
		"""change parameters of one child"""
		child= self.get_child(index_list)
		child.set_activity(activity)
		child.set_transformation_relative(position,orientation,scale)
	
	def del_item_child(self,index_list):
		"""remove a child"""
		parent= self.get_child(index_list[:-1])
		parent.del_child(index_list[-1])
	
	
	def add_item_model(self,index_list,model):
		"""assign 3d graphic to one item"""
		child= self.get_child(index_list)
		child.add_model(model)
		
	def set_item_model(self,index_list,mesh_group):
		"""change 3d graphic for the specified item"""
		child= self.get_child(index_list)
		child.set_model(mesh_group)
	
	def del_item_model(self,index_list):
		"""remove 3d graphic from specified item"""
		child= self.get_child(index_list)
		child.del_model()
	
	
	def add_item_noise(self,index_list,noise):
		"""assign 3d sound to one item"""
		child= self.get_child(index_list)
		child.add_noise(noise)

	def set_item_noise(self,index_list,volumes,pitch,playout):
		"""change 3d sound for the specified item"""
		child= self.get_child(index_list)
		child.set_noise(volumes,pitch,playout)
	
	def del_item_noise(self,index_list):
		"""remove 3d sound from a specified item"""
		child= self.get_child(index_list)
		child.del_noise()
	
	