#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing sprites class"#information describing the purpose of this module
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
import ctypes

### OpenGL imports
from OpenGL import GL as gl
#from OpenGL.GL import shaders
#from OpenGL import GLU as glu
#from OpenGL import GLE as gle
#from OpenGL.GL.ARB.multitexture import *#
#from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays,glBindVertexArray#

### commonz imports
from commonz.constants import *
from commonz.ds import array



class Sprite:
	"""the combination of rectangle square mesh and texture for hud icons"""
	def __init__(self,window_size,bitmap,anchor,relative_position,relative_width,relative_height,color):
		"""bitmap must be a textures ressource"""
		
		self.bitmap= bitmap
		
		self.color=None;self.set_color(color)
		
		self.relative_width=relative_width
		self.relative_height=relative_height
		self.relative_position=relative_position
		
		self.anchor_matrix= array.translate_matrix(anchor[X],anchor[Y],0)
		
		### use matrix for the scale factors
		self.pre_scale_matrix=None
		self.post_scale_matrix=None
		self.resize(window_size)
		
		### build vertex data
		vertex_data=[]
		half_size= array.vector(self.bitmap.get_size())/2
		
		xyz=[0-half_size[X],0-half_size[Y],0]
		uv=[0,0]
		vertex_data+=xyz+uv
		
		xyz=[0-half_size[X],half_size[Y],0]
		uv=[0,1]
		vertex_data+=xyz+uv
		
		xyz=[half_size[X],half_size[Y],0]
		uv=[1,1]
		vertex_data+=xyz+uv
		
		xyz=[half_size[X],0-half_size[Y],0]
		uv=[1,0]
		vertex_data+=xyz+uv
		
		### get a new Vertex Array Object and activate it as the current
		self.vao = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(self.vao)
		
		### get the necessary  Vertex Buffer Objects  for vertices,texture,normals and others
		self.vbo = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertex_data = numpy.array(tuple(vertex_data), dtype=numpy.float32)# opengl need static data type
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_data, gl.GL_STATIC_DRAW)# allocates a part of GPU memory and adds data into
		
		#float_size= ctypes.sizeof(ctypes.c_float)
		float_size = ctypes.sizeof(gl.GLfloat)
		stride= 5*float_size #usually want this to be a power of 2 for compatibility with some hardware
		
		### Describe the data layout in the buffer
		ofset= ctypes.cast(0*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(0)
		#self.position = gl.glGetAttribLocation(shaderx, 'position')
		gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		ofset= ctypes.cast(3*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(1)
		#self.position = gl.glGetAttribLocation(shaderx, 'uv')
		gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		###deprecated
		#glVertexPointer(VV_SIZE,GL_FLOAT, RECORD_LEN, VERTEX_OFFSET)
		#glNormalPointer(GL_FLOAT, RECORD_LEN, NORMAL_OFFSET)
		#glTexCoordPointer(TV_SIZE,GL_FLOAT, RECORD_LEN, MAP_OFFSET)
		#glColorPointer(3, GL_FLOAT, record_len, color_offset)
		
		### Unbind
		### Unbind the VAO first (Important)
		gl.glBindVertexArray( 0 )
		### Unbind other stuff
		#gl.glDisableVertexAttribArray(self.position)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
	
	
	def set_color(self,color=None):
		"""change the color that will be mixed with the 2d graphic"""
		if color is not None :
			self.color= numpy.array( (color,), dtype=numpy.float32 )
	
	 
	def render_draw(self,shader,model_matrix):
		"""display the 2d graphic on the overlay"""
		
		### blend color
		location = gl.glGetUniformLocation(shader.index,"blend_color")
		gl.glUniform3fv(location, 1, self.color)
		
		### give the model_matrix to the shader
		model_matrix= self.anchor_matrix @ self.pre_scale_matrix @ model_matrix @ self.post_scale_matrix
		loc = gl.glGetUniformLocation(shader.index, 'model_matrix')
		gl.glUniformMatrix4fv(loc, 1, True, model_matrix )
		
		### select the bitmap
		self.bitmap.select()
		
		### Deprecated
		#gl.glLoadIdentity()
		#gl.glRasterPos2f(position[X],position[Y])
		#gl.glWindowPos2f(position[X],position[Y])
		#gl.glPixelZoom(zoom[X],zoom[Y])
		#gl.glDrawPixels(self.size[X],self.size[Y],GL_RGBA,GL_UNSIGNED_BYTE,self.data)
		
		### bind select
		gl.glBindVertexArray(self.vao)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		#gl.glEnableVertexAttribArray(0)
		#gl.glEnableVertexAttribArray(1)
		#gl.glEnableVertexAttribArray(2)
		
		### draw as GL_TRIANGLE
		### GL_QUADS have been removed from core OpenGL 3.1 and above
		#gl.glEnableClientState(gl.GL_VERTEX_ARRAY)#
		#gl.glVertexPointer(3,gl.GL_FLOAT,0,0)#
		gl.glDrawArrays(gl.GL_TRIANGLE_FAN,0,4)
		
		### unbind unselect
		gl.glBindVertexArray(0)
		#gl.glDisableVertexAttribArray(0)
		#gl.glDisableVertexAttribArray(1)
		#gl.glDisableVertexAttribArray(2)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
	
	
	def resize(self,window_size):
		"""change the size of the 2d graphic"""
		bitmap_size= self.bitmap.get_size()
		
		if self.relative_width :
			width= 1/bitmap_size[X]
		else:
			width= 1/window_size[X]
		
		if self.relative_height :
			height= 1/bitmap_size[Y]
		else:
			height= 1/window_size[Y]
		
		if self.relative_position :
			self.pre_scale_matrix= array.identity_matrix()
			self.post_scale_matrix= array.scale_matrix(width,height,1)
		else:
			x= 1/window_size[X]
			y= 1/window_size[Y]
			self.pre_scale_matrix= array.scale_matrix(x,y,1)
			self.post_scale_matrix= array.scale_matrix(width/x,height/y,1)
	
	
	def __del__(self):
		"""clear the resources taken by the 2d graphic"""
		gl.glDeleteVertexArrays(1, [self.vao])
		gl.glDeleteBuffers(1, [self.vbo])
	
	