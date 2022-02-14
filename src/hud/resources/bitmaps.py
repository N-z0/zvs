#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the bitmaps resources"#information describing the purpose of this module
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



class Bitmap :
	"""store an image as openGL ressource for hud icons"""
	def __init__(self,image_file):
		"""image_file must be the path of a valid bitmap image file"""
		
		### load the image
		img= image.Bitmap_File(image_file)
		#print("IMG info:",img.get_mode(),img.img.mode,img.get_info())
		self.size= img.get_size()
		
		### need to flip upside-down, because opengl images origin is at the left down corner
		img.transpose(image.FLIP_VERTICALLY)
		
		### Deprecated
		### since openGL4 the next commands are not available
		#gl.glLoadIdentity()
		#gl.glRasterPos2f(position[X],position[Y])
		#gl.glWindowPos2f(position[X],position[Y])
		#gl.glPixelZoom(zoom[X],zoom[Y])
		
		### store identity attributes
		self.index=gl.glGenTextures(1)
		
		### then need to select 
		self.select()
		
		### set the repeat parameters
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,gl.GL_REPEAT)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,gl.GL_REPEAT)
		
		### set filtering parameters
		### filtering mode can be GL_NEAREST(fast but ugly) or GL_LINEAR(slow but pretty)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
		
		### create gl texture for the bitmap
		size=img.get_size()
		gl_img=img.get_gl_data()
		#gl_img=img.get_array('f')
		#gl_img=Image.fromstring("RGBX",(size[X],size[Y]),self.data)
		### tex_mode can be GL_REPLACE GL_MODULATE GL_DECAL GL_BLEND
		#tex_mode=gl.GL_REPLACE
		#gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE,tex_mode)#deprecated
		gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)
		#gluBuild2DMipmaps(GL_TEXTURE_2D,3,IMAGE_SIZE_X,IMAGE_SIZE_Y,GL_RGBA,GL_UNSIGNED_BYTE,IMAGE)#
		### 7th and 8th arguments describes the data passed in the last argument.
		### internalFormat (2nd argument) defines the format that OpenGL should use to store the data internally.
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.size[Y],self.size[X], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, gl_img)
		###  generate mipmaps
		gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
	
	
	def get_size(self):
		"""return the size of the image"""
		return self.size
	
	
	def select(self):
		"""select the texture that openGL will use"""
		### activate the texture unit first before binding texture
		gl.glActiveTexture(gl.GL_TEXTURE0)
		### bind texture
		gl.glBindTexture(gl.GL_TEXTURE_2D,self.index)
	
	
	def __del__(self):
		"""clear the resources taken by the bitmap"""
		gl.glBindTexture(gl.GL_TEXTURE_2D,0)
	
	