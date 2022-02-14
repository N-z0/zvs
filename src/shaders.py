#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "dedicated OpenGL shaders module"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-04-01"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### OpenGL imports
from OpenGL import GL as gl



class Shader:
	"""Create and destroy shaders program"""
	def __init__(self,shader_pathname,shader_type):
		"""Shader are initialized with source files and a Shader type"""
		self.index=None
		with open(shader_pathname, 'r') as src_file:
			src_code = src_file.read()
			index = gl.glCreateShader(shader_type)
			gl.glShaderSource(index, src_code)
			gl.glCompileShader(index)
			self.index=index
	
	def check(self):
		"""return any error message"""
		if not gl.glGetShaderiv(self.index, gl.GL_COMPILE_STATUS):
			log= " ".join(gl.glGetShaderInfoLog(self.index).decode('ascii').splitlines())# convert the byte string to normal characters and join all lines
		else :
			log= ''
		return log
	
	def __del__(self):
		"""clean the shader's ressources"""
		if self.index: # if this is a valid shader object
			gl.glDeleteShader(self.index) # destroy the GL object


class Vertex_Shader(Shader):
	"""GL vertex shader"""
	def __init__(self,shader_pathname):
		"""vertex Shader is initialized with a source files"""
		Shader.__init__(self,shader_pathname,gl.GL_VERTEX_SHADER)


class Fragment_Shader(Shader):
	"""GL fragment shader"""
	def __init__(self,shader_pathname):
		"""fragment Shader is initialized with a source files"""
		Shader.__init__(self,shader_pathname,gl.GL_FRAGMENT_SHADER)


class Compiled_Shader():
	"""A compiled vertex and fragment Shader"""
	def __init__(self,vertex_shader,fragment_shader):
		"""is initialized with a vertex and a fragment shader"""
		index = gl.glCreateProgram()
		gl.glAttachShader(index, vertex_shader.index)
		gl.glAttachShader(index, fragment_shader.index)
		gl.glLinkProgram(index)
		self.index=index

	def check(self):
		"""return any error message"""
		if not gl.glGetProgramiv(self.index, gl.GL_LINK_STATUS):
			log= " ".join(gl.glGetProgramInfoLog(self.index).decode('ascii').splitlines())# convert the byte string to normal characters and join all lines
		else :
			log= ''
		return log
		
	def __del__(self):
		"""clean the shader's ressources"""
		#gl.glUseProgram(0) #means that no program is current, and therefore no program will be used for things that use programs. like shaders
		if self.index: # if this is a valid shader object
			gl.glDeleteProgram(self.index) # destroy the GL object
	
	