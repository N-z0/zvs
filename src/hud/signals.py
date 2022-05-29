#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the signals class"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.1"# version number,date or about last modification made compared to the previous version
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

### PyOpenAL require an OpenAL shared library
import openal

### commonz imports
#from commonz.constants import *
#from commonz.ds import array



class Signal :
	"""audio for hud icons"""
	def __init__(self,audio,volume,pitch,loop):
		"""see openAL documentation about the parameters"""
		
		### instance a source object
		self.source=openal.Source(audio.get_buffer())
		
		self.playout=None
		### need to keep loop variable for setting it again later
		self.loop=loop
		
		### set the source attributes
		self.source.set_looping(loop)
		self.source.set_pitch(pitch)
		self.source.set_gain(volume)
		self.source.set_cone_outer_gain(1)
		self.source.set_cone_inner_angle(0)
		self.source.set_cone_outer_angle(360)
		self.source.set_rolloff_factor(2)
		self.source.set_reference_distance(1)
		self.source.set_source_relative(True)
		
		### calculation error can append if distance is set to zero
		self.source.set_position( [0,0,1] )
	
	
	def render_audio(self):
		"""make heard the audio in the overlay"""
		
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
				#self.source.stop() # interrupt the audio if not yet finished playing
				self.source.set_looping(False)# let finish playing the audio
		else:
			pass
	
	
	def set_playout(self,playout=None):
		"""change the playback status"""
		if playout is not None :
			self.playout=playout
	
	def set_volume(self,volume=None):
		"""change the gain"""
		if volume is not None :
			self.source.set_gain(volume)
	
	def set_pitch(self,pitch=None):
		"""change the tone"""
		if pitch is not None :
			self.source.set_pitch(pitch)
	
	