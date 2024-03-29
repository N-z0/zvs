#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing Overlay class"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.0"# version number,date or about last modification made compared to the previous version
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

### commonz imports
from commonz import logger
from commonz.constants import *
from commonz.ds import array

### local imports
from . import icons



class Basic_Overlay :
	"""Overlay are the root of all icons"""
	def __init__(self,blend_factor,position,orientation,scale):
		"""position orientation scale are normally not necessary"""
		
		self.icons_list=[]
	
	
	def _add_element(self,elements_list,element):
		""" """
		if None in elements_list :
			element_index= elements_list.index(None)
			elements_list[element_index]=element
		else :
			element_index= len(elements_list)
			elements_list.append(element)
		return element_index
	
	
	def reckon(self,log_context):
		"""update absolute matrix of all moved icons"""
		logger.log_debug(79,context=log_context)
		for icon in self.icons_list :
			icon.reckon_absolute_transformation()
	
	
	def add_icon(self,parent_index,icon):
		"""append an icon child"""
		if parent_index is not None :
			parent=self.icons_list[parent_index]
			parent.add_child(icon)
		icon_index= self._add_element(self.icons_list,icon)
		return icon_index
	
	def set_icon(self,icon_index,activity,position,orientation,scale):
		"""change the parameters of one icon child"""
		icon= self.icons_list[icon_index]
		icon.set_activity(activity)
		icon.reckon_relative_transformation(position,orientation,scale)
	
	def del_icon(self,parent_index,icon_index):
		"""remove an icon child"""
		icon= self.icons_list[icon_index]
		if parent_index is not None :
			parent= self.icons_list[parent_index]
			parent.del_child(icon)
		self.icons_list[icon_index]=None


	def get_icon_activity(self,icon_index):
		"""return the state of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_activity()
	
	def get_icon_relative_position(self,icon_index):
		"""return the relative position of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_relative_position()
	
	def get_icon_relative_orientation(self,icon_index):
		"""return the relative angle of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_relative_orientation()
	
	def get_icon_relative_scale(self,icon_index):
		"""return the relative scale of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_relative_scale()
	
	def get_icon_absolute_position(self,icon_index):
		"""return the absolute position of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_absolute_position()
	
	def get_icon_absolute_direction(self,icon_index):
		"""return the absolute orientation of the specified icon"""
		icon= self.icons_list[icon_index]
		return icon.get_absolute_direction()








class Overlay(Basic_Overlay) :
	"""Overlay are the root of all icons"""
	def __init__(self,shader,blend_factor,position,orientation,scale):
		"""position orientation scale are normally not necessary"""
		Basic_Overlay.__init__(self,blend_factor,position,orientation,scale)
		
		self.shader=shader
		
		self.blend_factor=None;self.set_blend_factor(blend_factor)
	
	
	def set_blend_factor(self,blend_factor=None):
		"""change the transparency of the overlay"""
		if blend_factor is not None :
			self.blend_factor= numpy.array( (blend_factor,), dtype=numpy.float32 )
	
	
	def resize(self,window_size):
		"""ask children to change the size of the sprites"""
		for icon in self.icons_list :
			icon.resize_sprite(window_size)
	
	
	def render(self,window_size,log_context):
		"""display all icons of the overlay"""
		logger.log_debug(80,context=log_context)
		self.render_icons_sound()
		
		logger.log_debug(81,context=log_context)
		self.render_icons_draw(window_size)
	
	
	def render_icons_draw(self,window_size):
		"""draw all icons of the overlay"""
		
		### glClear values
		gl.glClearDepth(1.0)# depth buffer value on clear, The default value is 1
		#gl.glClearStencil(0)  #Specifies the index used when the stencil buffer is cleared. The initial value is 0.
		#gl.glClearAccum(0,0,0,0)
		
		### clear buffers
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
		#gl.glEnable(gl.GL_LINE_SMOOTH)
		#gl.glEnable(gl.GL_POINT_SMOOTH)
		
		### set an offset for drawing points n lines above polygons and Width
		### maybe deprecated and useless
		gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
		gl.glDisable(gl.GL_POLYGON_OFFSET_LINE)
		gl.glDisable(gl.GL_POLYGON_OFFSET_POINT)
		#gl.glPolygonOffset(-10.,-10.)#
		#gl.glLineWidth(1)# pixel width
		#gl.glPointSize(3)# pixel width
		
		### specify individual color components in frame buffer that can or not be written.
		gl.glColorMask(gl.GL_TRUE,gl.GL_TRUE,gl.GL_TRUE,gl.GL_TRUE)
		
		### removal of hidden faces
		gl.glFrontFace(gl.GL_CW)#choose how is the FRONT FACE, GL_CW clockwise or GL_CCW counter-clockwise (the default)
		gl.glCullFace(gl.GL_BACK)#face not to show
		gl.glEnable(gl.GL_CULL_FACE)#enable the hide of face for not translucent objects
		
		### depth filter
		gl.glDisable(gl.GL_DEPTH_TEST)# because sprites have different layer positions
		#gl.glDepthMask(gl.GL_TRUE)#pecifies whether the depth buffer is enabled for writing. If flag is GL_FALSE, depth buffer writing is disabled.
		#gl.glDepthFunc(gl.GL_LEQUAL) # The Type Of Depth Test To Do ,  GL_LESS par defaut
		#gl.glDepthRange(0,1) # 0,1 is the default
		
		### blending
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )#Transparency is best implemented using (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		### mix functions
		gl.glBlendEquation(gl.GL_FUNC_ADD)
		#gl.glEnable(gl.GL_COLOR_LOGIC_OP)# To enable or disable the glLogicOp
		#gl.glLogicOp(gl.GL_AND)# specifies logical operation between the incoming color and the color at the corresponding location in the frame buffer
		
		### Stencil
		#gl.glDisable(gl.GL_STENCIL_TEST)
		#gl.glStencilFunc(gl.GL_ALWAYS,1,1)
		#gl.glStencilOp(gl.GL_KEEP,gl.GL_REPLACE,gl.GL_REPLACE)
		
		### select shader for drawing
		gl.glUseProgram(self.shader.index)# don't forget to activate the shader before setting uniforms!
		
		gl.glViewport(0,0,window_size[X],window_size[Y])
		
		### blend 0 = overlays sprites are completely transparent
		### blend 1 = overlays sprites are completely opaque
		location = gl.glGetUniformLocation(self.shader.index,"blend_factor")
		gl.glUniform1fv(location, 1, self.blend_factor)
		
		loc = gl.glGetUniformLocation(self.shader.index, 'projection_matrix')
		projection = array.ortho_matrix(0,1,0,1,0,1)
		gl.glUniformMatrix4fv(loc, 1, True, projection )
		
		### display our overlay icons
		for icon in self.icons_list :
			icon.render_sprite(self.shader)
		
		### unselect shader
		gl.glUseProgram(0)
		
		### finish the draw
		#gl.glFlush()
	
	def render_icons_sound(self):
		"""play sound of icons"""
		for icon in self.icons_list :
			icon.render_signal()
	
	
	def add_icon_sprite(self,icon_index,sprite):
		"""assign 2d graphic to one icon"""
		icon= self.icons_list[icon_index]
		icon.add_sprite(sprite)
		
	def set_icon_sprite(self,icon_index,color):
		"""change a 2d graphic for specified icon"""
		icon= self.icons_list[icon_index]
		icon.set_sprite(color)
	
	def del_icon_sprite(self,icon_index):
		"""remove the 2d graphic from specified icon"""
		icon= self.icons_list[icon_index]
		icon.del_sprite()
	
	
	def add_icon_signal(self,icon_index,noise):
		"""assign audio sound to one icon"""
		icon= self.icons_list[icon_index]
		icon.add_signal(noise)

	def set_icon_signal(self,icon_index,volume,pitch,playout):
		"""change an audio sound for specified icon"""
		icon= self.icons_list[icon_index]
		icon.set_signal(volume,pitch,playout)
	
	def del_icon_signal(self,icon_index):
		"""remove an audio sound from specified icon"""
		icon= self.icons_list[icon_index]
		icon.del_signal()

