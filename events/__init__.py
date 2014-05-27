#!/usr/bin/env python

from __future__ import print_function
try:
	import json
except ImportError:
	try:
		import simplejson as json
	except ImportError:
		json = None

import six
import hashlib
from pelican import signals
from pprint import pprint
import os

from pelican.generators import Generator
from pelican import readers
from pelican import settings

from pelican.utils import pelican_open

from blinker import signal
event_generator_init = signal('event_generator_init')
event_generator_finalized = signal('event_generator_finalized')

from .generators import EventsGenerator

class EventReader(readers.BaseReader):
	enabled = bool(json)
	file_extensions = ["event"]
	def read(self, source_path):
		print( "Reading event from {}".format(source_path) )
		with pelican_open(source_path) as text:
			print( text )
			data = {}
			pre_data = json.loads(text)
		for k,v in pre_data.items():
			data[k.lower()] = v
		print("got data:")
		pprint(data)
		return ("",data)


def add_reader(readers):
	readers.reader_classes['event'] = EventReader

def showData(sender,metadata,**kwargs):
	print("showData called")
	print( "kwargs:", kwargs.keys() )
	print( "context:", sender.context.keys() )

def initEvents(generator):
	events_dict = {}
	try:
		events = generator.context['events']
	except KeyError:
		generator.context['events'] = events = {}
	print( "events initialized as:" )
	pprint(events)

def get_generators(generators):
	return EventsGenerator

def register():
	print( "Registering event reader" )
	signals.readers_init.connect(add_reader)
	print ("registering generator")
	signals.get_generators.connect(get_generators)
	#print( "registering events initializer" )
	#signals.page_generator_init.connect(initEvents)

