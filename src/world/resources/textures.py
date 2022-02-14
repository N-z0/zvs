#!python#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the textures resources"#information describing the purpose of this module
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
from commonz.constants import *
#from commonz.ds import array
from commonz.animasnd import image



class Texture:
	"""store an image as openGL texture resource for world items"""
	def __init__(self,image_file,slot,gl_format,img_format):
		"""
		image_file must be the path of a valid bitmap image file
		slot can be GL_TEXTURE0 to GL_TEXTURE5
		gl_format can be GL_RGB GL_RGBA GL_RED
		img_format can be GL_RGB GL_RGBA GL_RED
		"""
		
		### load the image
		img= image.Bitmap_File(image_file)
		#print("IMG info:",img.get_mode(),img.img.mode,img.get_info())
		self.size= img.get_size()
		
		### need to flip upside-down, because opengl images origin is at the left down corner
		img.transpose(image.FLIP_VERTICALLY)
		
		### store identity attributes
		self.slot=slot
		self.index=gl.glGenTextures(1)
		
		### then need to select 
		self.select()
		
		### set the texture repeat parameters
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,gl.GL_REPEAT)#GL_MIRRORED_REPEAT)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,gl.GL_REPEAT)#GL_MIRRORED_REPEAT)
		
		### set texture filtering parameters
		### filtering mode can be GL_NEAREST(fast but ugly) or GL_LINEAR(slow but pretty)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
		
		### create gl texture
		gl_img=img.get_gl_data()
		### tex_mode can be GL_REPLACE GL_MODULATE GL_DECAL GL_BLEND
		#tex_mode=gl.GL_REPLACE
		#gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE,tex_mode)#deprecated
		gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)
		#gluBuild2DMipmaps(GL_TEXTURE_2D,3,IMAGE_SIZE_X,IMAGE_SIZE_Y,GL_RGBA,GL_UNSIGNED_BYTE,IMAGE)#
		### 7th and 8th arguments describes the data passed in the last argument.
		### internalFormat (2nd argument) defines the format that OpenGL should use to store the data internally.
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl_format, self.size[Y],self.size[X], 0, img_format, gl.GL_UNSIGNED_BYTE, gl_img)
		###  generate mipmaps
		gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
	
	
	def get_size(self):
		"""return the size of the image"""
		return self.size
	
	
	def select(self):
		"""select the texture that openGL will use"""
		### activate the texture unit first before binding texture
		gl.glActiveTexture(self.slot)
		### bind texture
		gl.glBindTexture(gl.GL_TEXTURE_2D,self.index)
	
	
	def __del__(self):
		"""clear the resources taken by the texture"""
		gl.glBindTexture(gl.GL_TEXTURE_2D,0)



class Emissive_Texture(Texture) :
	"""store an image as openGL Emissive texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE0, gl.GL_RGBA, gl.GL_RGBA)



class AO_Texture(Texture) :
	"""store an image as openGL AO texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE1, gl.GL_RED, gl.GL_RED)



class Albedo_Texture(Texture) :
	"""store an image as openGL Albedo texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE2, gl.GL_RGBA, gl.GL_RGBA)



class Smoothness_Texture(Texture) :
	"""store an image as openGL Smoothness texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE3, gl.GL_RED, gl.GL_RED)



class Metallic_Texture(Texture) :
	"""store an image as openGL Metallic texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE4, gl.GL_RED, gl.GL_RED)



class Normal_Texture(Texture) :
	"""store an image as openGL Normal texture"""
	def __init__(self,img_path):
		"""img_path must be the path of a valid bitmap image file"""
		Texture.__init__(self, img_path, gl.GL_TEXTURE5, gl.GL_RGB, gl.GL_RGB)


