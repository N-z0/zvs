#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "interface module for managing the virtual world"#information describing the purpose of this module
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
#import os
#from ctypes import sizeof, c_float, c_void_p, c_uint
import pkg_resources
#import importlib.resources as importlib_resources

### OpenGL imports
from OpenGL import GL as gl
#from OpenGL.GL import shaders
#from OpenGL import GLU as glu
#from OpenGL import GLE as gle
#from OpenGL.GL.ARB.multitexture import *#
#from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays,glBindVertexArray#

### PyOpenAL will require an OpenAL shared library
import openal

### commonz imports
from commonz import logger
from commonz.fs import pathnames
from commonz.datafiles import tsv
from commonz.ds import array
#from commonz.constants import *

### import world
from .world.resources import meshes
from .world.resources import materials
from .world.resources import textures
from .world.resources import sounds
from .world import noises
from .world import models
from .world import items
from .world import lights
from .world import eyes
from .world import ears
from .world import scenes
### import hud
from .hud.resources import bitmaps
from .hud.resources import audios
from .hud import signals
from .hud import sprites
from .hud import icons
from .hud import overlays
### import shaders
from . import shaders



MSG_FILE="data/msgs.txt"
#DATA_DIRECTORY="data"
### for the setup of sub directories additional identity can be used
### only for windows os, because currently not working on linux
#PROG_PUBLISHER= None # if set at None this feature will be ignored
VERTEX_SHADERS_FOLDER="data/shaders/vertex"
FRAGMENT_SHADERS_FOLDER="data/shaders/fragment"
SHADERS_REPERTORY_FILE="data/shaders/repertory.tsv"
GLSL_EXT="glsl"

GL_AUX_BUFFERS= "AUX_BUFFERS"
GL_ACCUM_BUFFERS_BITS= "ACCUM_BUFFERS_BITS"
GL_COLORS_BITS= "COLORS_BITS"
GL_DEPTH_BITS= "DEPTH_BITS"
GL_STENCIL_BITS= "STENCIL_BITS"
GL_MAX_TEXTURE_UNITS= "MAX_TEXTURE_UNITS"
GL_MAX_TEXTURE_SIZE= "MAX_TEXTURE_SIZE"

AL_DEVICES= "devices"
AL_DEFAULT= "default"
AL_CAPTURE= "capture"


class Interface:
	"""virtual world interface object"""
	def __init__(self,window_size=(1,1)):
		"""window_size is optional at the start"""
		
		### get the prog name for later retrieving the prog's data files
		self.name=__package__
		
		### resources libraries
		self.bitmaps_lib={}
		self.audios_lib={}
		self.meshs_lib={}
		self.textures_lib={}
		self.material_lib={}
		self.sounds_lib={}
		
		### scenes
		self.scenes={}
		self.current_scene=None
		
		### overlays
		self.overlays={}
		self.current_overlay=None
		
		### get data ready for later loading shaders
		self.shaders_repertory_file= pkg_resources.resource_filename(self.name,SHADERS_REPERTORY_FILE)
		self.vertex_shaders_folder= pkg_resources.resource_filename(self.name,VERTEX_SHADERS_FOLDER)
		self.fragment_shaders_folder= pkg_resources.resource_filename(self.name,FRAGMENT_SHADERS_FOLDER)
		self.vert_shaders_lib={}
		self.frag_shaders_lib={}
		self.combo_shaders_lib={}
		
		### add the specific messages file to the log system
		msgsfile= pkg_resources.resource_filename(self.name,MSG_FILE)
		logger.load_messages(msgsfile,context=self.name)
		
		### keep the current window size
		self.window_size=array.vector( window_size )
	
	
	def load_shaders(self):
		"""from .tsv repertory file load shaders"""
		table=tsv.get_dico(self.shaders_repertory_file)
		for row in table :
			combo_shader_name=row['#name']
			vertex_shader=row['#vertex_shader']
			fragment_shader=row['#fragment_shader']
			logger.log_info(1,[combo_shader_name],context=self.name)
			self.load_shader_vertex(vertex_shader)
			self.load_shader_fragment(fragment_shader)
			self.load_shader_combo(combo_shader_name,vertex_shader,fragment_shader)
	
	def load_shader_vertex(self,name):
		"""from a glsl file load a vertex shader"""
		if not name in self.vert_shaders_lib :
			fullname=pathnames.join_base_name_ext(name,[GLSL_EXT])
			shader_file=pathnames.join_pathname(self.vertex_shaders_folder,fullname)
			vs = shaders.Vertex_Shader(shader_file)
			log=vs.check()
			if log :
				logger.log_error(2,[name,log],context=self.name)
			else:
				self.vert_shaders_lib[name]=vs
	
	def load_shader_fragment(self,name):
		"""from a glsl file load a fragment shader"""
		if not name in self.frag_shaders_lib :
			fullname=pathnames.join_base_name_ext(name,[GLSL_EXT])
			shader_file=pathnames.join_pathname(self.fragment_shaders_folder,fullname)
			fs= shaders.Fragment_Shader(shader_file)
			log=fs.check()
			if log :
				logger.log_error(3,[name,log],context=self.name)
			else:
				self.frag_shaders_lib[name]=fs
	
	def load_shader_combo(self,name,vertex_shader_name,fragment_shader_name):
		"""compile a shader from a vertex and a fragment shader"""
		if not name in self.combo_shaders_lib :
			vert_shader= self.vert_shaders_lib[vertex_shader_name]
			frag_shader= self.frag_shaders_lib[fragment_shader_name]
			cs= shaders.Compiled_Shader(vert_shader,frag_shader)
			log= cs.check()
			if log :
				logger.log_error(4,[log],context=self.name)
			else:
				self.combo_shaders_lib[name]=cs
	
	
	def load_resource_audio(self,name,pathname):
		"""stock audio from a sound file for the icons"""
		if not name in self.audios_lib :
			logger.log_info(7,[name],context=self.name)
			self.audios_lib[name]=audios.Audio(pathname)
	
	def load_resource_bitmap(self,name,pathname):
		"""stock bitmap from a image file for the icons"""
		if not name in self.bitmaps_lib :
			logger.log_info(8,[name],context=self.name)
			self.bitmaps_lib[name]=bitmaps.Bitmap(pathname)
	
	def load_resource_sound(self,name,pathname):
		"""stock sound from a file for the items"""
		if not name in self.sounds_lib :
			logger.log_info(9,[name],context=self.name)
			self.sounds_lib[name]=sounds.Sound(pathname)
	
	def load_resource_texture_emissive(self,name,pathname):
		"""stock emissive texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(10,[name],context=self.name)
			self.textures_lib[name]= textures.Emissive_Texture(pathname)
	
	def load_resource_texture_ao(self,name,pathname):
		"""stock ao texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(11,[name],context=self.name)
			self.textures_lib[name]= textures.AO_Texture(pathname)
	
	def load_resource_texture_albedo(self,name,pathname):
		"""stock albedo texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(12,[name],context=self.name)
			self.textures_lib[name]= textures.Albedo_Texture(pathname)
	
	def load_resource_texture_smoothness(self,name,pathname):
		"""stock smoothness texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(13,[name],context=self.name)
			self.textures_lib[name]= textures.Smoothness_Texture(pathname)
	
	def load_resource_texture_metallic(self,name,pathname):
		"""stock metallic texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(14,[name],context=self.name)
			self.textures_lib[name]= textures.Metallic_Texture(pathname)
	
	def load_resource_texture_normal(self,name,pathname):
		"""stock normal texture from image file for the models"""
		if not name in self.textures_lib :
			logger.log_info(15,[name],context=self.name)
			self.textures_lib[name]= textures.Normal_Texture(pathname)
	
	def load_resource_mesh(self,name,pathname,subname=''):
		"""
		stock mesh from file for the models
		subname is for selecting a sub mesh object
		"""
		if not name in self.meshs_lib :
			self.meshs_lib[name]={}
		if not subname in self.meshs_lib[name] :
			logger.log_info(16,[name,subname],context=self.name)
			self.meshs_lib[name][subname]=meshes.Mesh(pathname,subname)
	
	def load_resource_material(self,name,pathname):
		"""stock material from file for the models"""
		if not name in self.material_lib :
			logger.log_info(17,[name],context=self.name)
			self.material_lib[name]=materials.Mat_Lib(pathname)
	
	
	def add_overlay(self,overlay_name,shader_index,blend_factor=1,position=(0,0),orientation=0,scale=(1,1)):
		"""
		append a new overlay
		blend_factor is the transparency and must be set between 0 and 1
		position orientation scale are the starting placement of the overlay icons
		"""
		shader=self.combo_shaders_lib[shader_index]
		self.overlays[overlay_name]= overlays.Overlay(shader,blend_factor,position,orientation,scale)
		logger.log_debug(20,[overlay_name],context=self.name)
	
	def set_overlay(self,overlay_name,blend_factor=None):
		"""
		change parameters of overlay
		not given parameters are ignored and will produce no changes
		blend_factor is the transparency and must be set between 0 and 1
		"""
		overlay= self.overlays[overlay_name]
		overlay.set_blend_factor(blend_factor)
		logger.log_debug(21,[overlay_name],context=self.name)
	
	def del_overlay(self,overlay_name):
		"""remove an exiting overlay"""
		### check if the overlay is the current overlay
		if self.overlays[overlay_name]==self.current_overlay :
			self.current_overlay=None
		### delete the overlay in the dico
		del self.overlays[overlay_name]
		logger.log_debug(22,[overlay_name],context=self.name)
	
	def select_overlay(self,overlay_name):
		"""select witch overlay will be display"""
		self.current_overlay= self.overlays[overlay_name]
		logger.log_debug(23,[overlay_name],context=self.name)
	
	
	def add_overlay_icon(self,overlay_name,index_list,show=True,position=(0,0),orientation=0,scale=(1,1)):
		"""
		append new icon into the specified overlay
		if show is True the icon will be enabled in the specified overlay
		position orientation scale change icon placement in the specified overlay
		"""
		icon= icons.Icon(show,position,orientation,scale)
		self.overlays[overlay_name].add_icon_child(index_list,icon)
		logger.log_debug(25,[overlay_name],context=self.name)
	
	def set_overlay_icon(self,overlay_name,index_list,activity=None,position=None,orientation=None,scale=None):
		"""
		change icon parameters of the specified scene
		not given parameters are ignored and will produce no changes
		activity change the icon status in the specified overlay
		position orientation scale change icon placement in the specified overlay
		"""
		self.overlays[overlay_name].set_icon(index_list,activity,position,orientation,scale)
		logger.log_debug(26,[overlay_name],context=self.name)
	
	def del_overlay_icon(self,overlay_name,icon_name):
		"""remove an icon from specified overlay"""
		self.overlays[overlay_name].del_icon_child(icon_name)
		logger.log_debug(27,[overlay_name],context=self.name)
	
	
	def add_overlay_icon_sprite(self,overlay_name,index_list,bitmap_index,anchor=(0.5,0.5),relative_position=False,relative_width=False,relative_height=False,color=(1,1,1)):
		"""
		append  a sprite for the specified icon in the specified overlay
		anchor is considered as starting point of the bitmap
		if relative_position is True the placement depend of the screen size
		if relative_width is True the width depend of the screen size
		if relative_height is True the height depend of the screen size
		color will be mixed with the sprite image (must be a RGB vector)
		"""
		bitmap= self.bitmaps_lib[bitmap_index]
		sprite= sprites.Sprite(self.window_size,bitmap,anchor,relative_position,relative_width,relative_height,color)
		self.overlays[overlay_name].add_icon_sprite(index_list,sprite)
		logger.log_debug(29,[overlay_name],context=self.name)
	
	def set_overlay_icon_sprite(self,overlay_name,index_list,color=None):
		"""
		change a sprite parameters for the specified icon in the specified overlay
		not given parameters are ignored and will produce no changes
		color will be mixed with the sprite image (must be a RGB vector)
		"""
		self.overlays[overlay_name].set_icon_sprite(index_list,sprite)
		logger.log_debug(30,[overlay_name],context=self.name)
		
	def del_overlay_icon_sprite(self,overlay_name,index_list):
		"""remove a sprite for the specified icon in the specified overlay"""
		self.overlays[overlay_name].del_icon_sprite(index_list)
		logger.log_debug(31,[overlay_name],context=self.name)
		
	
	def add_overlay_icon_signal(self,overlay_name,index_list,audio_index,volume=1,repeat=0):
		"""
		append  an audio signal for the specified icon in the specified overlay
		volume is the gain of sound (must be between 0 and 1 )
		repeat is the number of time that the sound will be play (-1 infinite)
		"""
		audio=self.audios_lib[audio_index]
		signal= signals.Signal(audio,volume,repeat)
		self.overlays[overlay_name].add_icon_signal(index_list,signal)
		logger.log_debug(33,[overlay_name],context=self.name)
		
	def set_overlay_icon_signal(self,overlay_name,index_list,volume=None,repeat=None):
		"""
		change audio signal parameters for the specified icon in the specified overlay
		not given parameters are ignored and will produce no changes
		volume is the gain of sound (must be between 0 and 1 )
		repeat is the number of time that the sound will be play (-1 infinite)
		"""
		self.overlays[overlay_name].set_icon_signal(index_list,volume,repeat)
		logger.log_debug(34,[overlay_name],context=self.name)
	
	def del_overlay_icon_signal(self,overlay_name,index_list):
		"""remove an audio signal for the specified icon in the specified overlay"""
		self.overlays[overlay_name].del_icon_signal(index_list)
		logger.log_debug(35,[overlay_name],context=self.name)
	
	
	def add_scene(self,scn_name,shader_index,background_color=(0,0,0,1),background_fog=(0,0,0,0),blend_factor=1.,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a new scene
		background_color set the color of where nothing is draw
		fog set the opacity color
		blend_factor set the color blending between material and textures of objects
		position orientation scale are vectors for the scene placement
		"""
		shader=self.combo_shaders_lib[shader_index]
		self.scenes[scn_name]= scenes.Scene(shader,background_color,background_fog,blend_factor,position,orientation,scale)
		logger.log_debug(38,[scn_name],context=self.name)
	
	def set_scene(self,scn_name,background=None,fog=None,blend_factor=None):
		"""
		change parameters of scene
		not given parameters are ignored and will produce no changes
		background set the color of where nothing is draw
		fog set the opacity color
		blend_factor set the color blending between material and textures of objects
		"""
		scene= self.scenes[scn_name]
		scene.set_background_color(background)
		scene.set_fog_color(fog)
		scene.set_blend_factor(blend_factor)
		logger.log_debug(39,[scn_name],context=self.name)
	
	def del_scene(self,scn_name):
		"""remove an exiting scene"""
		### check if the scene is the current scene
		if self.scenes[scn_name]==self.current_scene :
			self.current_scene=None
		### delete the scene in the dico
		del self.scenes[scn_name]
		logger.log_debug(40,[scn_name],context=self.name)
	
	def select_scene(self,scn_name):
		"""select witch scene will be display"""
		self.current_scene= self.scenes[scn_name]
		logger.log_debug(41,[scn_name],context=self.name)
	
	
	def add_scene_item(self,scn_name,index_list,show=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a new item into specified scene
		if show is True the item will be enable
		position orientation scale are vectors for the item placement
		"""
		item= items.Item(show,position,orientation,scale)
		self.scenes[scn_name].add_item_child(index_list,item)
		logger.log_debug(43,[scn_name],context=self.name)
	
	def set_scene_item(self,scn_name,index_list,activity=None,position=None,orientation=None,scale=None):
		"""
		change item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		activity change item status in the specified scene
		position orientation scale change item placement in the specified scene
		"""
		self.scenes[scn_name].set_item(index_list,activity,position,orientation,scale)
		logger.log_debug(44,[scn_name],context=self.name)
	
	def del_scene_item(self,scn_name,index_list):
		"""remove an item from a specified scene"""
		self.scenes[scn_name].del_item_child(index_list)
		logger.log_debug(45,[scn_name],context=self.name)
	
	
	def add_scene_item_model(self,scn_name,index_list,mesh_index,obj_name,emit_tex_index,ao_tex_index,albedo_tex_index,smooth_tex_index,metal_tex_index,norm_tex_index,matarials_list,group_name=''):
		"""
		append an item model for the specified scene
		mesh_index select the mesh library
		obj_name select a 3d shape from the mesh library
		group_name select the sub group of the 3d shape that will be draw on screen
		*_tex_index select all the textures needed
		matarials_list select all the material library needed
		"""
		mesh=self.meshs_lib[mesh_index][obj_name]
		emit_tex=self.textures_lib[emit_tex_index]
		ao_tex=self.textures_lib[ao_tex_index]
		albedo_tex=self.textures_lib[albedo_tex_index]
		smooth_tex=self.textures_lib[smooth_tex_index]
		metal_tex=self.textures_lib[metal_tex_index]
		norm_tex=self.textures_lib[norm_tex_index]
		matarials={}
		for matlib_name in matarials_list :
			matarials[matlib_name]=self.material_lib[matlib_name]
		model= models.Model(mesh,group_name,emit_tex,ao_tex,albedo_tex,smooth_tex,metal_tex,norm_tex,matarials)
		self.scenes[scn_name].add_item_model(index_list,model)
		logger.log_debug(47,[scn_name],context=self.name)
	
	def set_scene_item_model(self,scn_name,index_list,mesh_group=None):
		"""
		change an item model of the specified scene
		not given parameters are ignored and will produce no changes
		mesh_group is for select the sub mesh
		"""
		self.scenes[scn_name].set_item_model(index_list,mesh_group)
		logger.log_debug(48,[scn_name],context=self.name)
	
	def del_scene_item_model(self,scn_name,index_list):
		"""remove an item model of the specified scene"""
		self.scenes[scn_name].del_item_model(index_list)
		logger.log_debug(49,[scn_name],context=self.name)
	
	
	def add_scene_item_noise(self,scn_name,index_list,sound_name,volumes=(1,1),pitch=1,loop=False,angles=(0,360),rolloff_factor=1,reference_distance=1):
		"""
		append an item noise of the specified scene
		volumes is the gain of the sound
		if pitch <1 decrease the sound frequency is lowered, if >1 increase the sound frequency or no change if None
		if loop is true the sound will be played endless
		angles of sound diffusion (in radians)
		rolloff_factor for the sound calculation (see openAL doc)
		reference_distance for the sound calculation (see openAL doc)
		"""
		sound=self.sounds_lib[sound_name]
		noise= noises.Noise(sound,volumes,pitch,loop,angles,rolloff_factor,reference_distance)
		self.scenes[scn_name].add_item_noise(index_list,noise)
		logger.log_debug(51,[scn_name],context=self.name)
	
	def set_scene_item_noise(self,scn_name,index_list,volumes=None,pitch=None,playout=None):
		"""
		change a noise for the specified item in the specified scene
		not given parameters are ignored and will produce no changes
		volumes is the gain of the sound
		if pitch <1 decrease the sound frequency is lowered, if >1 increase the sound frequency or no change if 1
		if playout is True the sound will be emitted
		"""
		self.scenes[scn_name].set_item_noise(index_list,volumes,pitch,playout)
		logger.log_debug(52,[scn_name],context=self.name)
	
	def del_scene_item_noise(self,scn_name,index_list):
		"""remove an item noise of the specified scene"""
		self.scenes[scn_name].del_item_noise(index_list)
		logger.log_debug(53,[scn_name],context=self.name)
	
	
	def add_scene_light(self,scn_name,index_list,ambient=(0.1,0.1,0.1),diffuse=(1,1,1),turn=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a light item in the specified scene
		ambient is the added color surrounding objects
		diffuse is the color added to object directly exposed
		if turn is True the light will be enable
		position orientation scale are vectors for the light placement
		"""
		light= lights.Light(ambient,diffuse,turn,position,orientation,scale)
		self.scenes[scn_name].add_light(index_list,light)
		logger.log_debug(55,[scn_name],context=self.name)
	
	def set_scene_light(self,scn_name,index_list,ambient=None,diffuse=None):
		"""
		change light item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		ambient is the added color surrounding objects
		diffuse is the color added to object directly exposed
		"""
		self.scenes[scn_name].set_light(index_list,ambient,diffuse)
		logger.log_debug(56,[scn_name],context=self.name)
	
	def del_scene_light(self,scn_name,index_list):
		"""remove light item from the specified scene"""
		self.scenes[scn_name].del_light(index_list)
		logger.log_debug(57,[scn_name],context=self.name)
	
	
	def add_scene_eye(self,scn_name,index_list,frame_position=(0,0),frame_size=(1,1),size=1,scope=1,focal=1,see=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append  an eye item in the specified scene
		frame_position and frame_size are 2d vectors of the place where to draw in the window
		size is the extent of the eye in the virtual space
		scope is the view range of how far the eye can see in the virtual world
		focal is the angle of view, it need to be in radian
		if see is True the eye will be enable
		position orientation scale are placement vectors
		"""
		eye= eyes.Eye(self.window_size,frame_position,frame_size,size,scope,focal,see,position,orientation,scale)
		self.scenes[scn_name].add_eye(index_list,eye)
		logger.log_debug(59,[scn_name],context=self.name)
	
	def set_scene_eye(self,scn_name,index_list,frame_position=None,frame_size=None,focal=None):
		"""
		change eye item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		frame_position and frame_size are 2d vectors placing where to draw in the window
		focal is the angle of view and must be in radian
		"""
		self.scenes[scn_name].set_eye(index_list,self.window_size,frame_position,frame_size,focal)
		logger.log_debug(60,[scn_name],context=self.name)
	
	def del_scene_eye(self,scn_name,eye_name):
		"""remove eye item from the specified scene"""
		self.scenes[scn_name].del_eye(eye_name)
		logger.log_debug(61,[scn_name],context=self.name)
	
	
	def add_scene_ear(self,scn_name,index_list,volume=1,see=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append  ear item in the specified scene
		volume must be between 0 and 1
		if see is True the ear will be enable
		position orientation scale are placement vectors
		"""
		ear= ears.Ear(volume,see,position,orientation,scale)
		self.scenes[scn_name].add_ear(index_list,ear)
		logger.log_debug(63,[scn_name],context=self.name)
	
	def set_scene_ear(self,scn_name,index_list,volume=None):
		"""
		change ear item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		volume must be between 0 and 1
		"""
		self.scenes[scn_name].set_ear(index_list,volume)
		logger.log_debug(64,[scn_name],context=self.name)
	
	def del_scene_ear(self,scn_name,ear_name):
		"""remove a ear item from the specified scene"""
		self.scenes[scn_name].del_ear(ear_name)
		logger.log_debug(65,[scn_name],context=self.name)
	
	
	def resize(self,window_size):
		"""
		change the size of the frame where the 3d world is draw
		(window_size must be a tuple containing am horizontal and vertical size)
		"""
		self.window_size= array.vector( window_size )
		for scn_name in list(self.scenes.keys()) :
			logger.log_debug(67,[scn_name],context=self.name)
			self.scenes[scn_name].resize(self.window_size)
		for overlay_name in list(self.overlays.keys()) :
			logger.log_debug(68,[overlay_name],context=self.name)
			self.overlays[overlay_name].resize(self.window_size)
	
	
	def display(self):
		"""render previously selected scene and overlay"""
		if self.current_scene is not None :
			logger.log_debug(69,context=self.name)
			self.current_scene.display(self.window_size,log_context=self.name)
		if self.current_overlay is not None :
			logger.log_debug(70,context=self.name)
			self.current_overlay.display(self.window_size,log_context=self.name)
		
	
	def get_info_opengl(self,extensions=None):
		"""
		return OpenGL characteristics
		extensions can be a list containing the extensions that we want to check,
		or if extensions is an empty list all extenstions will be include
		but if extensions is None no extenstions at all will be include
		"""
		info={}
		
		### get gl version
		### These are available on OpenGL version 3.0 and above contexts.
		#print('OpenGL major version:',gl.glGetString(gl.GL_MAJOR_VERSION).decode())
		#print('OpenGL minor version:',gl.glGetString(gl.GL_MINOR_VERSION).decode())
		### If those are not available, you can use this instead:
		info['version']= gl.glGetString(gl.GL_VERSION).decode()
		
		### The primary version of GLSL supported by the implementation can be queried:
		info['GLSL']= gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()
		
		### This string is often the name of the GPU.
		### In the case of Mesa3d, it would be i.e "Gallium 0.4 on NVA8"
		### It might even say "Direct3D"
		info['GPU']= gl.glGetString(gl.GL_RENDERER).decode()
		
		### vendor string associated with it
		### It could be "ATI Technologies", "NVIDIA Corporation", "INTEL" and so on
		info['vendor']= gl.glGetString(gl.GL_VENDOR).decode()
		
		### Extension list
		info['extensions']=[]
		if extensions is not None :
			### Extensions need to be queried one by one.
			for index in range(gl.glGetIntegerv(gl.GL_NUM_EXTENSIONS)):
				ext=gl.glGetStringi(gl.GL_EXTENSIONS,index).decode()
				if ext in extensions or len(extensions)==0 :
					info['extensions'].append(ext)
		
		info[GL_AUX_BUFFERS]= gl.glGetIntegerv(gl.GL_AUX_BUFFERS)
		
		info[GL_ACCUM_BUFFERS_BITS]= (gl.glGetIntegerv(gl.GL_ACCUM_RED_BITS),gl.glGetIntegerv(gl.GL_ACCUM_GREEN_BITS),gl.glGetIntegerv(gl.GL_ACCUM_BLUE_BITS),gl.glGetIntegerv(gl.GL_ACCUM_ALPHA_BITS))
		info[GL_COLORS_BITS]= (gl.glGetIntegerv(gl.GL_RED_BITS),gl.glGetIntegerv(gl.GL_GREEN_BITS),gl.glGetIntegerv(gl.GL_BLUE_BITS),gl.glGetIntegerv(gl.GL_ALPHA_BITS))
		info[GL_DEPTH_BITS]= gl.glGetIntegerv(gl.GL_DEPTH_BITS)
		info[GL_STENCIL_BITS]= gl.glGetIntegerv(gl.GL_STENCIL_BITS)
		
		info[GL_MAX_TEXTURE_UNITS]= gl.glGetIntegerv(gl.GL_MAX_TEXTURE_UNITS)
		info[GL_MAX_TEXTURE_SIZE]= gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE)
		
		return info
	
	def get_info_openal(self,extensions=False):
		"""
		return OpenAL characteristics
		if extensions is True a list containing the extensions is include
		"""
		info={}
		#print("Enumeration Extension:",openal.alcIsExtensionPresent(None,openal.ALC_ENUMERATE_ALL_EXT))
		info[AL_DEVICES]= openal.alcGetString(None,openal.ALC_DEVICE_SPECIFIER)
		info[AL_DEFAULT]= openal.alcGetString(None,openal.ALC_DEFAULT_DEVICE_SPECIFIER)
		info[AL_CAPTURE]= openal.alcGetString(None,openal.ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER)
		
		return info
	
	
	def stop(self):
		"""request to stop the virtual world"""
		
		### remove all scenes
		for scn_name in list(self.scenes.keys()) :
			logger.log_info(71,[scn_name],context=self.name)
			self.del_scene(scn_name)
		
		### remove all overlays
		for overlay_name in list(self.overlays.keys()) :
			logger.log_info(72,[overlay_name],context=self.name)
			self.del_overlay(overlay_name)
		
		### release OpenAL resources
		### destroys all existing OpenAL Sources and Buffers
		openal.oalQuit()
	
	