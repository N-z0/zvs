#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the meshes resources"#information describing the purpose of this module
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
from commonz.datafiles import obj
from commonz.ds import array



class Mesh:
	"""store an openGL 3d mesh as resource for world items"""
	def __init__(self,pathname,name=''):
		"""
		pathname must be the path of a valid obj file
		name is the object that need to retrieve from the file
		"""
		
		### load file
		datafile=obj.load_obj_file(pathname)
		
		### extract data from file
		vertex_list=datafile[obj.VT]
		vertice_list=datafile[obj.V]
		normal_list=datafile[obj.VN]
		
		### get the first object name if no default name
		#print('mesh objects:',datafile[obj.OBJECTS].keys())
		if not name :
			names_list= tuple(datafile[obj.OBJECTS].keys())
			name=names_list[0]
		
		### get the vertex groups
		self.groups=datafile[obj.OBJECTS][name]
		#print('mesh groups:',datafile[obj.OBJECTS][name].keys())
		
		### compile vertex data
		vertex_data=()
		offset=quantum=0
		for group_name in self.groups :
			surfaces=self.groups[group_name]
			for mat_lib_name in surfaces :
				mat_lib=surfaces[mat_lib_name]
				for mat_name in mat_lib :
					faces_list=mat_lib[mat_name]
					for face in faces_list :
						new_face=[]
						for vertex in face :
							xyz=vertice_list[vertex[0]-1]
							uv=vertex_list[vertex[1]-1]
							nor=normal_list[vertex[2]-1]
							new_face.append([xyz,uv,nor])
							
						## Tangent Bitangent calculation
						p0=new_face[0]
						p1=new_face[1]
						p2=new_face[2]
						edge1= (p1[0][0]-p0[0][0], p1[0][1]-p0[0][1], p1[0][2]-p0[0][2])
						edge2= (p2[0][0]-p0[0][0], p2[0][1]-p0[0][1], p2[0][2]-p0[0][2])
						delta1= (p1[1][0]-p0[1][0], p1[1][1]-p0[1][1])
						delta2= (p2[1][0]-p0[1][0], p2[1][1]-p0[1][1])
						
						f = 1.0 / (delta1[0]*delta2[1] - delta2[0]*delta1[1])
						
						tx = f * (delta2[1] * edge1[0] - delta1[1] * edge2[0])
						ty = f * (delta2[1] * edge1[1] - delta1[1] * edge2[1])
						tz = f * (delta2[1]  * edge1[2] - delta1[1] * edge2[2])
						tangent=tuple(array.normalized_vector(tx,ty,tz))
						
						bx = f * (-delta2[0] * edge1[0] + delta1[0] * edge2[0])
						by = f * (-delta2[0] * edge1[1] + delta1[0] * edge2[1])
						bz = f * (-delta2[0] * edge1[2] + delta1[0] * edge2[2])
						bitangent=tuple(array.normalized_vector(bx,by,bz))
						
						for vertex in new_face :
							vertex_data += vertex[0]+vertex[1]+vertex[2]+tangent+bitangent
							quantum+=1
					
					mat_lib[mat_name]=(offset,quantum)
					offset+=quantum
					quantum=0
		
		### get a new Vertex Array Object and activate it as the current
		self.vao = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(self.vao)
		
		### get the necessary  Vertex Buffer Objects  for vertices,texture,normals and others
		self.vbo = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		vertex_data = numpy.array(vertex_data, dtype=numpy.float32)# opengl need static data type
		gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_data, gl.GL_STATIC_DRAW)# allocates a part of GPU memory and adds data into
		
		#float_size= ctypes.sizeof(ctypes.c_float)
		float_size = ctypes.sizeof(gl.GLfloat)
		stride= 14*float_size #usually want this to be a power of 2 for compatibility with some hardware
		
		### Describe the data layout in the buffer
		ofset= ctypes.cast(0*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(0)
		#self.position = gl.glGetAttribLocation(shaderx, 'position')
		gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		ofset= ctypes.cast(3*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(1)
		#self.position = gl.glGetAttribLocation(shaderx, 'uv')
		gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		ofset= ctypes.cast(5*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(2)
		#self.position = gl.glGetAttribLocation(shaderx, 'normal')
		gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		ofset= ctypes.cast(8*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(3)
		#self.position = gl.glGetAttribLocation(shaderx, 'tangent')
		gl.glVertexAttribPointer(3, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
		ofset= ctypes.cast(11*float_size, ctypes.c_void_p)
		gl.glEnableVertexAttribArray(4)
		#self.position = gl.glGetAttribLocation(shaderx, 'bitangent')
		gl.glVertexAttribPointer(4, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ofset )
		
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
	
	
	def get_groups_names(self):
		"""return the names of the vertex groups"""
		return self.groups.keys()
	
	def get_matlib_names(self,group_name):
		"""return the materials lib list used by the specified group"""
		return self.groups[group_name].keys()
	
	def get_material_names(self,group_name,mat_lib_name):
		"""return the materials list used by the specified materials lib"""
		return self.groups[group_name][mat_lib_name].keys()
	
	
	def draw(self,group_name,mat_lib_name,material_name):
		"""draw the on openGL 3D mesh"""
		
		### get index of the selected vertex
		ref=self.groups[group_name][mat_lib_name][material_name]
		ofset=ref[0]
		quantum=ref[1]
		
		### bind select
		gl.glBindVertexArray(self.vao)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		#gl.glEnableVertexAttribArray(0)
		#gl.glEnableVertexAttribArray(1)
		#gl.glEnableVertexAttribArray(2)
		
		### draw mesh as GL_TRIANGLE
		#gl.glEnableClientState(gl.GL_VERTEX_ARRAY)#
		#gl.glVertexPointer(3,gl.GL_FLOAT,0,0)#
		gl.glDrawArrays(gl.GL_TRIANGLES,ofset,quantum)
		
		### unbind unselect
		gl.glBindVertexArray(0)
		#gl.glDisableVertexAttribArray(0)
		#gl.glDisableVertexAttribArray(1)
		#gl.glDisableVertexAttribArray(2)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
	
	
	def __del__(self):
		"""clear the resources taken by the mesh"""
		gl.glDeleteVertexArrays(1, [self.vao])
		gl.glDeleteBuffers(1, [self.vbo])
	
	