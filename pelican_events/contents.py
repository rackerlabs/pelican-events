from pelican.contents import Page

class Event(Page):
    """
    An Event is meeting, conference, or other occurrence which can be displayed
    and indexed on a static site generation. It is intended to be used with the
    JSON generator and custom templates.
    """
    base_properties = ('starts','ends','title','event_type','description','location')
    mandatory_properties = ('starts','ends','title','event_type','location')
    default_template = 'event'
