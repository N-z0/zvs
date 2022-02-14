#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the signals class"#information describing the purpose of this module
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

### commonz imports
#from commonz.constants import *
#from commonz.ds import array



class Signal :
	"""audio for hud icons"""
	def __init__(self,audio,volume,repeat):
		"""all parameters are necessary"""
		self.audio=audio
		self.repeat=repeat
		self.set_volume(volume)
	
	
	def play(self):
		"""output audio if suitable"""
		state=self.audio.player.get_state(0)
		state_name= self.audio.player.state_get_name(state[1])
		playing= state_name=='PLAYING' or state_name=='READY'
		if not playing and (self.repeat>0 or self.repeat<0) :
			self.repeat-=1
			self.audio.play()
	
	
	def set_volume(self,volume=None):
		"""change the audio gain"""
		if volume is not None :
			self.audio.set_volume(volume)
	
	
	def set_repeat(self,repeat=None):
		"""change the play loop number"""
		if repeat is not None :
			self.repeat= repeat

