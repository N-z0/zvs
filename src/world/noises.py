#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the noises class"#information describing the purpose of this module
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
import math # for degrees radian covert
#import numpy

### PyOpenAL require an OpenAL shared library
import openal

### commonz imports
from commonz.constants import *
from commonz.ds import array



class Noise :
	"""a 3d sound for the items"""
	def __init__(self,sound,volumes,pitch,loop,angles,spreading_factor):
		"""
		spreading>1 reduce the loss of volumes
		spreading<1 increase the loss of volumes
		see openAL documentation for others the parameters
		"""
		
		### instance a source object
		self.source=openal.Source(sound.get_buffer())
		
		self.playout=False
		### need to keep loop variable for setting it again later
		self.loop=loop
		
		### set the source attributes
		self.source.set_looping(loop)
		self.source.set_gain(volumes[0])
		self.source.set_cone_outer_gain(volumes[1])
		self.source.set_pitch(pitch)
		self.source.set_cone_inner_angle(math.degrees(angles[0]))
		self.source.set_cone_outer_angle(math.degrees(angles[1]))
		self.source.set_rolloff_factor(2)
		self.source.set_reference_distance(spreading_factor)
		
		### for the absolute calculation of vectors
		self.position_vector=array.vector( 0,0,0,1 )
		self.direction_vector=array.vector( 0,0,-1,0 )
		self.old_position=None
	
	
	def render_audio(self,model_matrix):
		"""make heard the 3d sounds in the virtual world"""
		
		new_position= model_matrix.dot( self.position_vector )
		self.source.set_position( new_position[:3] )
		
		direction= model_matrix.dot( self.direction_vector )
		self.source.set_direction( direction[:3] )
		
		if self.old_position is not None :
			velocity= new_position-self.old_position
			self.source.set_velocity( velocity[:3])
		self.old_position=new_position
		
		### a source can be in one of the 4 possible states: 'Initial','Playing','Paused','Stopped'
		### source ready to start to play are in AL_INITIAL
		### a playing source have is state to AL_PLAYING.
		### When the attached buffer(s) are done playing the source state is AL_STOPPED.(need to Rewind)
		if self.playout is True :
			if not self.source.get_state() == openal.AL_PLAYING :# check if the file is playing
				self.source.set_looping(self.loop)
				self.source.play()# When called on source already playing, it restart to play from the beginning.
		elif self.playout is False :
			if self.source.looping :
				#self.source.stop() # interrupt the sound if not yet finished playing
				self.source.set_looping(False)# let finish playing the sound
		else:
			pass
	
	
	def set_playout(self,playout=None):
		"""change the playback status"""
		if playout is not None :
			self.playout=playout
	
	def set_volumes(self,volumes=None):
		"""change the gain"""
		if volumes is not None :
			self.source.set_gain(volumes[0])
			self.source.set_cone_outer_gain(volumes[1])
	
	def set_pitch(self,pitch=None):
		"""change the tone"""
		if pitch is not None :
			self.source.set_pitch(pitch)
	
	