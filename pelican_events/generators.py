# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import logging
from itertools import chain
from pelican.contents import is_valid_content
from pelican.utils import process_translations
from pelican import signals
from pelican.generators import CachingGenerator

from .contents import Event
from .signals import *

logger = logging.getLogger(__name__)



# In order for the bits below to work we need to define various signals. I'm
# not sure about the details because docs on blinker and how it is used here
# are hazy at best. It appears you simply define them here and use them in the
# code below. YMMV.


class EventsGenerator(CachingGenerator):
    """
    Generate Events

    This is the code responsible for finding and reading in the JSON files,
    ending with ".event" and turning them into objects for Pelican to use in
    generating HTML for them.
    """

    def __init__(self, *args, **kwargs):
        self.events = []
        self.hidden_events = []
        self.hidden_translations = []
        super(EventsGenerator, self).__init__(*args, **kwargs)
        event_generator_init.send(self)
        self.content_name="Events"

    def generate_report(self):
        """
        This will report to stdout the number of events and hidden events processed.
        """
        print( "Process {0} events and {1} hidden events".format( len(self.events), len(self.hidden_events) ) )

    def generate_context(self):
        """
        Here is the meat of the class - where the heavy lifting occurs.  It
        generates a list of events and places them in the context object so we
        can access them in templates.

        Some of this is leftover from the stock Article class. Ideally those aspect
        will be removed as it is shown they can be safely done away with.
        However, this works.
        """

        all_events = []
        hidden_events = []
        for f in self.get_files(
                self.settings['EVENT_DIR'],
                exclude=self.settings['EVENT_EXCLUDES']):
            event = self.get_cached_data(f, None)
            if event is None:
                try:
                    event = self.readers.read_file(
                        base_path=self.path, path=f, content_class=Event,
                        context=self.context,
                        preread_signal=event_generator_preread,
                        preread_sender=self,
                        context_signal=event_generator_context,
                        context_sender=self)
                except Exception as e:
                    logger.warning('Could not process {}\n{}'.format(f, e))
                    continue

                if not is_valid_content(event, f):
                    continue

                self.cache_data(f, event)

            self.add_source_path(event)

            if event.status == "published":
                all_events.append(event)
            elif event.status == "hidden":
                hidden_events.append(event)
            else:
                logger.warning("Unknown status %s for file %s, skipping it." %
                               (repr(event.status),
                                repr(f)))

        self.events, self.translations = process_translations(all_events)
        self.hidden_events, self.hidden_translations = (
            process_translations(hidden_events))

        self._update_context(('events', ))
        self.context['EVENTS'] = self.events

        self.save_cache()
        self.readers.save_cache()
        event_generator_finalized.send(self)

    def generate_output(self, writer):
        """
        Here we generate the HTML page form the event(s).
        """
        for event in chain(self.translations, self.events,
                          self.hidden_translations, self.hidden_events):
            writer.write_file(
                event.save_as, self.get_template(event.template),
                self.context, event=event,
                relative_urls=self.settings['RELATIVE_URLS'],
                override_output=hasattr(event, 'override_save_as'))


