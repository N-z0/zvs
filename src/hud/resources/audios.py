#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module for the audios resources"#information describing the purpose of this module
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
import os

### external moduls
#import numpy
import pyogg
import wave

### PyOpenAL require an OpenAL shared library
import openal

### commonz imports
#from commonz.constants import *
#from commonz.ds import array
#from commonz.animasnd import audio



class Audio :
	"""store an audio resource for hud icons"""
	def __init__(self,audio_path):
		"""
		load an audio file in a openal buffer that can be use by many openal sources
		files types: WAVE / Ogg Vorbis / Ogg Opus / FLAC
		"""

		ext= os.path.splitext(audio_path)[1] # work only if not more than 1 .ext
		
		if ext=='.wav' :
			### Read a wav file to obtain PCM data
			sound_file = wave.open(audio_path,"rb")
			
			### Extract the wav's specification
			channels = sound_file.getnchannels()
			bit_rate = sound_file.getsampwidth() * 8
			sample_rate = sound_file.getframerate()
			num_frames = sound_file.getnframes()
			data = sound_file.readframes(num_frames)
			duration= num_frames / float(sample_rate)
			all_fmt= {
				(1, 8): openal.AL_FORMAT_MONO8,
				(2, 8): openal.AL_FORMAT_STEREO8,
				(1, 16): openal.AL_FORMAT_MONO16,
				(2, 16): openal.AL_FORMAT_STEREO16,
				}
			fmt= all_fmt[(channels,bit_rate)]
			
			### fill the buffer with the data
			self.bufer= openal.Buffer(fmt, data, len(data), sample_rate)
		
		elif ext=='.opus' :
			sound_file = pyogg.OpusFile(audio_path)
			
			### get information about the audio
			#sample= sound_file.bytes_per_sample
			#channels= sound_file.channels
			#frequency= sound_file.frequency
			#buffer_length= sound_file.buffer_length
			#data = sound_file.as_array()
			
			self.bufer= openal.Buffer(sound_file)
			
		elif ext=='.ogg' :
			sound_file = pyogg.VorbisFile(audio_path)
			self.bufer= openal.Buffer(sound_file)
		elif ext=='.flac' :
			sound_file = pyogg.FlacFile(audio_path)
			self.bufer= openal.Buffer(sound_file)
		else :
			raise Error
	
	
	def get_buffer(self):
		return self.bufer
