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
from pelican import signals as core_signals
import os

from pelican.generators import Generator
from pelican import readers
from pelican import settings

from pelican.utils import pelican_open

from .generators import EventsGenerator
from .signals import *

class EventReader(readers.BaseReader):
	enabled = bool(json)
	file_extensions = ["event"]
	def read(self, source_path):
		with pelican_open(source_path) as text:
			data = {}
			pre_data = json.loads(text)
		for k,v in pre_data.items():
			data[k.lower()] = v
		return ("",data)


def add_reader(readers):
	readers.reader_classes['event'] = EventReader

def initEvents(generator):
	events_dict = {}
	try:
		events = generator.context['events']
	except KeyError:
		generator.context['events'] = events = {}

def get_generators(generators):
	return EventsGenerator

def register():
	core_signals.readers_init.connect(add_reader)
	core_signals.get_generators.connect(get_generators)

