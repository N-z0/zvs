#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "interface module for managing the virtual world"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
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
		self.meshes_lib={}
		self.textures_lib={}
		self.materials_lib={}
		self.sounds_lib={}
		
		### scenes
		self.scenes_list=[]
		self.current_scene=None
		
		### overlays
		self.overlays_list=[]
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
	
	
	def load_resource_audio(self,pathname):
		"""stock audio from a sound file for the icons"""
		if pathname in self.audios_lib :
			audio= self.audios_lib[pathname]
		else :
			logger.log_info(7,[pathname],context=self.name)
			audio= audios.Audio(pathname)
			self.audios_lib[pathname]= audio
		audios_list= list(self.audios_lib.values())
		return audios_list.index(audio)
	
	
	def load_resource_bitmap(self,pathname):
		"""stock bitmap from a image file for the icons"""
		if pathname in self.bitmaps_lib :
			bitmap= self.bitmaps_lib[pathname]
		else :
			logger.log_info(8,[pathname],context=self.name)
			bitmap= bitmaps.Bitmap(pathname)
			self.bitmaps_lib[pathname]= bitmap
		bitmaps_list= list(self.bitmaps_lib.values())
		return bitmaps_list.index(bitmap)
	
	
	def load_resource_sound(self,pathname):
		"""stock sound from a file for the items"""
		if pathname in self.sounds_lib :
			sound= self.sounds_lib[pathname]
		else :
			logger.log_info(9,[pathname],context=self.name)
			sound= sounds.Sound(pathname)
			self.sounds_lib[pathname]= sound
		sounds_list= list(self.sounds_lib.values())
		return sounds_list.index(sound)
	
	
	def load_resource_texture_emissive(self,pathname):
		"""stock emissive texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(10,[pathname],context=self.name)
			texture= textures.Emissive_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_texture_ao(self,pathname):
		"""stock ao texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(11,[pathname],context=self.name)
			texture= textures.AO_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_texture_albedo(self,pathname):
		"""stock albedo texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(12,[pathname],context=self.name)
			texture= textures.Albedo_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_texture_smoothness(self,pathname):
		"""stock smoothness texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(13,[pathname],context=self.name)
			texture= textures.Smoothness_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_texture_metallic(self,pathname):
		"""stock metallic texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(14,[pathname],context=self.name)
			texture= textures.Metallic_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_texture_normal(self,pathname):
		"""stock normal texture from image file for the models"""
		if pathname in self.textures_lib :
			texture= self.textures_lib[pathname]
		else :
			logger.log_info(15,[pathname],context=self.name)
			texture= textures.Normal_Texture(pathname)
			self.textures_lib[pathname]= texture
		textures_list= list(self.textures_lib.values())
		return textures_list.index(texture)
	
	
	def load_resource_mesh(self,pathname):
		"""stock mesh from file for the models"""
		if pathname in self.meshes_lib :
			mesh= self.meshes_lib[pathname]
		else :
			logger.log_info(16,[pathname],context=self.name)
			mesh= meshes.Mesh(pathname)
			self.meshes_lib[pathname]= mesh
		meshes_list= list(self.meshes_lib.values())
		return meshes_list.index(mesh)
	
	
	def load_resource_material(self,pathname):
		"""stock material from file for the models"""
		if pathname in self.materials_lib :
			material= self.materials_lib[pathname]
		else :
			logger.log_info(17,[pathname],context=self.name)
			material= materials.Mat_Lib(pathname)
			self.materials_lib[pathname]= material
		materials_list= list(self.materials_lib.values())
		return materials_list.index(material)
	
	
	def add_overlay(self,shader_name,blend_factor=1,position=(0,0),orientation=0,scale=(1,1)):
		"""
		append a new overlay
		blend_factor is the transparency and must be set between 0 and 1
		position orientation scale are the starting placement of the overlay icons
		"""
		shader=self.combo_shaders_lib[shader_name]
		
		overlay= overlays.Overlay(shader,blend_factor,position,orientation,scale)
		if None in self.overlays_list :
			overlay_index= self.overlays_list.index(None)
			self.overlays_list[overlay_index]=overlay
		else :
			overlay_index= len(self.overlays_list)
			self.overlays_list.append(overlay)
		logger.log_debug(20,[str(overlay_index)],context=self.name)
		
		return overlay_index
	
	
	def set_overlay(self,overlay_index,blend_factor=None):
		"""
		change parameters of overlay
		not given parameters are ignored and will produce no changes
		blend_factor is the transparency and must be set between 0 and 1
		"""
		overlay= self.overlays_list[overlay_index]
		overlay.set_blend_factor(blend_factor)
		logger.log_debug(21,[str(overlay_index)],context=self.name)
	
	def del_overlay(self,overlay_index):
		"""remove an exiting overlay"""
		### check if the overlay is the current overlay
		if self.overlays_list[overlay_index]==self.current_overlay :
			self.current_overlay=None
		### delete the overlay in the dico
		self.overlays_list[overlay_index]=None
		logger.log_debug(22,[str(overlay_index)],context=self.name)
	
	def select_overlay(self,overlay_index):
		"""select witch overlay will be display"""
		self.current_overlay= self.overlays_list[overlay_index]
		logger.log_debug(23,[str(overlay_index)],context=self.name)
	
	
	def add_overlay_icon(self,overlay_index,parent_index,show=True,position=(0,0),orientation=0,scale=(1,1)):
		"""
		append new icon into the specified overlay
		if show is True the icon will be enabled in the specified overlay
		position orientation scale change icon placement in the specified overlay
		"""
		icon= icons.Icon(show,position,orientation,scale)
		icon_index=self.overlays_list[overlay_index].add_icon(parent_index,icon)
		logger.log_debug(25,[str(overlay_index)],context=self.name)
		return icon_index
	
	def set_overlay_icon(self,overlay_index,icon_index,activity=None,position=None,orientation=None,scale=None):
		"""
		change icon parameters of the specified scene
		not given parameters are ignored and will produce no changes
		activity change the icon status in the specified overlay
		position orientation scale change icon placement in the specified overlay
		"""
		self.overlays_list[overlay_index].set_icon(icon_index,activity,position,orientation,scale)
		logger.log_debug(26,[str(overlay_index)],context=self.name)
	
	def del_overlay_icon(self,overlay_index,parent_index,icon_index):
		"""remove an icon from specified overlay"""
		self.overlays_list[overlay_index].del_icon_child(parent_index,icon_index)
		logger.log_debug(27,[str(overlay_index)],context=self.name)
	
	
	def add_overlay_icon_sprite(self,overlay_index,icon_index,bitmap_index,anchor=(0.5,0.5),relative_position=False,relative_width=False,relative_height=False,color=(1,1,1)):
		"""
		append  a sprite for the specified icon in the specified overlay
		anchor is considered as starting point of the bitmap
		if relative_position is True the placement depend of the screen size
		if relative_width is True the width depend of the screen size
		if relative_height is True the height depend of the screen size
		color will be mixed with the sprite image (must be a RGB vector)
		"""
		bitmap= list(self.bitmaps_lib.values())[bitmap_index]
		sprite= sprites.Sprite(self.window_size,bitmap,anchor,relative_position,relative_width,relative_height,color)
		self.overlays_list[overlay_index].add_icon_sprite(icon_index,sprite)
		logger.log_debug(29,[str(overlay_index)],context=self.name)
	
	
	def set_overlay_icon_sprite(self,overlay_index,icon_index,color=None):
		"""
		change a sprite parameters for the specified icon in the specified overlay
		not given parameters are ignored and will produce no changes
		color will be mixed with the sprite image (must be a RGB vector)
		"""
		self.overlays_list[overlay_index].set_icon_sprite(icon_index,color)
		logger.log_debug(30,[str(overlay_index)],context=self.name)
	
	
	def del_overlay_icon_sprite(self,overlay_index,icon_index):
		"""remove a sprite for the specified icon in the specified overlay"""
		self.overlays_list[overlay_index].del_icon_sprite(icon_index)
		logger.log_debug(31,[str(overlay_index)],context=self.name)
	
	
	def add_overlay_icon_signal(self,overlay_index,icon_index,audio_index,volume=1,pitch=1,loop=False):
		"""
		append  an audio signal for the specified icon in the specified overlay
		volume is the gain of sound (must be between 0 and 1 )
		repeat is the number of time that the sound will be play (-1 infinite)
		"""
		audio=list(self.audios_lib.values())[audio_index]
		signal= signals.Signal(audio,volume,pitch,loop)
		self.overlays_list[overlay_index].add_icon_signal(icon_index,signal)
		logger.log_debug(33,[str(overlay_index)],context=self.name)
	
	
	def set_overlay_icon_signal(self,overlay_index,icon_index,volume=None,pitch=None,playout=None):
		"""
		change audio signal parameters for the specified icon in the specified overlay
		not given parameters are ignored and will produce no changes
		volume is the gain of sound (must be between 0 and 1 )
		repeat is the number of time that the sound will be play (-1 infinite)
		"""
		self.overlays_list[overlay_index].set_icon_signal(icon_index,volume,pitch,playout)
		logger.log_debug(34,[str(overlay_index)],context=self.name)
	
	
	def del_overlay_icon_signal(self,overlay_index,icon_index):
		"""remove an audio signal for the specified icon in the specified overlay"""
		self.overlays_list[overlay_index].del_icon_signal(icon_index)
		logger.log_debug(35,[str(overlay_index)],context=self.name)
	
	
	def add_scene(self,shader_name,background_color=(0,0,0,1),background_fog=(0,0,0,0),blend_factor=1.,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a new scene
		background_color set the color of where nothing is draw
		fog set the opacity color
		blend_factor set the color blending between material and textures of objects
		position orientation scale are vectors for the scene placement
		"""
		shader=self.combo_shaders_lib[shader_name]
		
		scene= scenes.Scene(shader,background_color,background_fog,blend_factor,position,orientation,scale)
		if None in self.scenes_list :
			scn_index= self.scenes_list.index(None)
			self.scenes_list[scn_index]=scene
		else :
			scn_index= len(self.scenes_list)
			self.scenes_list.append(scene)
		logger.log_debug(38,[str(scn_index)],context=self.name)
		
		return scn_index
	
	
	def set_scene(self,scn_index,background=None,fog=None,blend_factor=None):
		"""
		change parameters of scene
		not given parameters are ignored and will produce no changes
		background set the color of where nothing is draw
		fog set the opacity color
		blend_factor set the color blending between material and textures of objects
		"""
		scene= self.scenes_list[scn_index]
		scene.set_background_color(background)
		scene.set_fog_color(fog)
		scene.set_blend_factor(blend_factor)
		logger.log_debug(39,[str(scn_index)],context=self.name)
	
	def del_scene(self,scn_index):
		"""remove an exiting scene"""
		### check if the scene is the current scene
		if self.scenes_list[scn_index]==self.current_scene :
			self.current_scene=None
		### remove the scene from the list
		self.scenes_list[scn_index]=None
		logger.log_debug(40,[str(scn_index)],context=self.name)
	
	def select_scene(self,scn_index):
		"""select witch scene will be display"""
		self.current_scene= self.scenes_list[scn_index]
		logger.log_debug(41,[str(scn_index)],context=self.name)
	
	
	def add_scene_item(self,scn_index,parent_index,show=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a new item into specified scene
		if show is True the item will be enable
		position orientation scale are vectors for the item placement
		"""
		item= items.Item(show,position,orientation,scale)
		item_index=self.scenes_list[scn_index].add_item(parent_index,item)
		logger.log_debug(43,[str(scn_index)],context=self.name)
		return item_index
	
	def set_scene_item(self,scn_index,item_index,activity=None,position=None,orientation=None,scale=None,cumulative=False):
		"""
		change item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		activity change item status in the specified scene
		position orientation scale change item placement in the specified scene
		"""
		self.scenes_list[scn_index].set_item(item_index,activity,position,orientation,scale,cumulative)
		logger.log_debug(44,[str(scn_index)],context=self.name)
	
	def del_scene_item(self,scn_index,parent_index,item_index):
		"""remove an item from a specified scene"""
		self.scenes_list[scn_index].del_item(parent_index,item_index)
		logger.log_debug(45,[str(scn_index)],context=self.name)
	
	
	def add_scene_item_model(self,scn_index,item_index,mesh_index,obj_name,emit_tex_index,ao_tex_index,albedo_tex_index,smooth_tex_index,metal_tex_index,norm_tex_index,matarials,group_name=''):
		"""
		append an item model for the specified scene
		mesh_index select the mesh library
		obj_name select a 3d shape from the mesh library
		group_name select the sub group of the 3d shape that will be draw on screen
		*_tex_index select all the textures needed
		matarials_list select all the material library needed
		"""
		mesh= list(self.meshes_lib.values())[mesh_index]
		emit_tex=list(self.textures_lib.values())[emit_tex_index]
		ao_tex=list(self.textures_lib.values())[ao_tex_index]
		albedo_tex=list(self.textures_lib.values())[albedo_tex_index]
		smooth_tex=list(self.textures_lib.values())[smooth_tex_index]
		metal_tex=list(self.textures_lib.values())[metal_tex_index]
		norm_tex=list(self.textures_lib.values())[norm_tex_index]
		for matlib_name in matarials :
			matlib_index=matarials[matlib_name]
			matarials[matlib_name]=list(self.materials_lib.values())[matlib_index]
		model= models.Model(mesh,obj_name,group_name,emit_tex,ao_tex,albedo_tex,smooth_tex,metal_tex,norm_tex,matarials)
		self.scenes_list[scn_index].add_item_model(item_index,model)
		logger.log_debug(47,[str(scn_index)],context=self.name)
	
	
	def set_scene_item_model(self,scn_index,item_index,mesh_group=None):
		"""
		change an item model of the specified scene
		not given parameters are ignored and will produce no changes
		mesh_group is for select the sub mesh
		"""
		self.scenes_list[scn_index].set_item_model(item_index,mesh_group)
		logger.log_debug(48,[str(scn_index)],context=self.name)
	
	def del_scene_item_model(self,scn_index,item_index):
		"""remove an item model of the specified scene"""
		self.scenes_list[scn_index].del_item_model(item_index)
		logger.log_debug(49,[str(scn_index)],context=self.name)
	
	
	def add_scene_item_noise(self,scn_index,item_index,sound_index,volumes=(1,1),pitch=1,loop=False,angles=(0,360),spreading_factor=1):
		"""
		append an item noise of the specified scene
		volumes is the gain of the sound
		if pitch <1 decrease the sound frequency is lowered, if >1 increase the sound frequency or no change if None
		if loop is true the sound will be played endless
		angles of sound diffusion (in radians)
		rolloff_factor for the sound calculation (see openAL doc)
		reference_distance for the sound calculation (see openAL doc)
		"""
		sound= list(self.sounds_lib.values())[sound_index]
		noise= noises.Noise(sound,volumes,pitch,loop,angles,spreading_factor)
		self.scenes_list[scn_index].add_item_noise(item_index,noise)
		logger.log_debug(51,[str(scn_index)],context=self.name)
	
	def set_scene_item_noise(self,scn_index,item_index,volumes=None,pitch=None,playout=None):
		"""
		change a noise for the specified item in the specified scene
		not given parameters are ignored and will produce no changes
		volumes is the gain of the sound
		if pitch <1 decrease the sound frequency is lowered, if >1 increase the sound frequency or no change if 1
		if playout is True the sound will be emitted
		"""
		self.scenes_list[scn_index].set_item_noise(item_index,volumes,pitch,playout)
		logger.log_debug(52,[str(scn_index)],context=self.name)
	
	def del_scene_item_noise(self,scn_index,item_index):
		"""remove an item noise of the specified scene"""
		self.scenes_list[scn_index].del_item_noise(item_index)
		logger.log_debug(53,[str(scn_index)],context=self.name)
	
	
	def add_scene_light(self,scn_index,parent_index,ambient=(0.1,0.1,0.1),diffuse=(1,1,1),turn=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append a light item in the specified scene
		ambient is the added color surrounding objects
		diffuse is the color added to object directly exposed
		if turn is True the light will be enable
		position orientation scale are vectors for the light placement
		"""
		light= lights.Light(ambient,diffuse,turn,position,orientation,scale)
		light_index=self.scenes_list[scn_index].add_light(parent_index,light)
		logger.log_debug(55,[str(scn_index)],context=self.name)
		return light_index
	
	def set_scene_light(self,scn_index,light_index,ambient=None,diffuse=None):
		"""
		change light item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		ambient is the added color surrounding objects
		diffuse is the color added to object directly exposed
		"""
		self.scenes_list[scn_index].set_light(light_index,ambient,diffuse)
		logger.log_debug(56,[str(scn_index)],context=self.name)
	
	def del_scene_light(self,scn_index,parent_index,light_index):
		"""remove light item from the specified scene"""
		self.scenes_list[scn_index].del_light(parent_index,light_index)
		logger.log_debug(57,[str(scn_index)],context=self.name)
	
	
	def add_scene_eye(self,scn_index,parent_index,frame_position=(0,0),frame_size=(1,1),size=1,scope=1,focal=1,see=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
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
		eye_index=self.scenes_list[scn_index].add_eye(parent_index,eye)
		logger.log_debug(59,[str(scn_index)],context=self.name)
		return eye_index
	
	def set_scene_eye(self,scn_index,eye_index,frame_position=None,frame_size=None,focal=None):
		"""
		change eye item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		frame_position and frame_size are 2d vectors placing where to draw in the window
		focal is the angle of view and must be in radian
		"""
		self.scenes_list[scn_index].set_eye(eye_index,self.window_size,frame_position,frame_size,focal)
		logger.log_debug(60,[str(scn_index)],context=self.name)
	
	def del_scene_eye(self,scn_index,parent_index,eye_index):
		"""remove eye item from the specified scene"""
		self.scenes_list[scn_index].del_eye(parent_index,eye_index)
		logger.log_debug(61,[str(scn_index)],context=self.name)
	
	
	def add_scene_ear(self,scn_index,parent_index,volume=1,see=True,position=(0,0,0),orientation=(1,0,0,0),scale=(1,1,1)):
		"""
		append  ear item in the specified scene
		volume must be between 0 and 1
		if see is True the ear will be enable
		position orientation scale are placement vectors
		"""
		ear= ears.Ear(volume,see,position,orientation,scale)
		ear_index=self.scenes_list[scn_index].add_ear(parent_index,ear)
		logger.log_debug(63,[str(scn_index)],context=self.name)
		return ear_index
	
	def set_scene_ear(self,scn_index,ear_index,volume=None):
		"""
		change ear item parameters of the specified scene
		not given parameters are ignored and will produce no changes
		volume must be between 0 and 1
		"""
		self.scenes_list[scn_index].set_ear(ear_index,volume)
		logger.log_debug(64,[str(scn_index)],context=self.name)
	
	def del_scene_ear(self,scn_index,parent_index,ear_index):
		"""remove a ear item from the specified scene"""
		self.scenes_list[scn_index].del_ear(parent_index,ear_index)
		logger.log_debug(65,[str(scn_index)],context=self.name)
	
	
	def resize(self,window_size):
		"""
		change the size of the frame where the 3d world is draw
		(window_size must be a tuple containing am horizontal and vertical size)
		"""
		self.window_size= array.vector( window_size )
		for scn_index in range(len(self.scenes_list)) :
			logger.log_debug(67,[str(scn_index)],context=self.name)
			self.scenes_list[scn_index].resize(self.window_size)
		for overlay_index in range(len(self.overlays_list)) :
			logger.log_debug(68,[str(overlay_index)],context=self.name)
			self.overlays_list[overlay_index].resize(self.window_size)
	
	def reckon(self):
		"""calculation of previously selected scene and overlay"""
		if self.current_scene is not None :
			logger.log_debug(69,context=self.name)
			self.current_scene.reckon(log_context=self.name)
		if self.current_overlay is not None :
			logger.log_debug(70,context=self.name)
			self.current_overlay.reckon(log_context=self.name)
	
	def display(self):
		"""render previously selected scene and overlay"""
		if self.current_scene is not None :
			logger.log_debug(69,context=self.name)
			self.current_scene.render(self.window_size,log_context=self.name)
		if self.current_overlay is not None :
			logger.log_debug(70,context=self.name)
			self.current_overlay.render(self.window_size,log_context=self.name)
		
	
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
		for scn_index in range(len(self.scenes_list)) :
			logger.log_info(71,[str(scn_index)],context=self.name)
			self.del_scene(scn_index)
		
		### remove all overlays
		for overlay_index in range(len(self.overlays_list)) :
			logger.log_info(72,[str(overlay_index)],context=self.name)
			self.del_overlay(overlay_index)
		
		### release OpenAL resources
		### destroys all existing OpenAL Sources and Buffers
		openal.oalQuit()
	
	
