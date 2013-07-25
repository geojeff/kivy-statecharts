from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty


# In the spirit of Cocoa / Sproutcore, a simple idea useful for locking
# while loading or for fine control of editing user interfaces.
class Controller(EventDispatcher):

    content = ObjectProperty(None, allownone=True)

    is_editable = BooleanProperty(True)

    def update(self, *args):
        pass
