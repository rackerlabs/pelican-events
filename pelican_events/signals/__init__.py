
from blinker import signal
event_generator_init = signal('event_generator_init')
event_generator_finalized = signal('event_generator_finalized')
event_generator_preread = signal('event_generator_preread')
event_generator_context = signal('event_generator_context')

