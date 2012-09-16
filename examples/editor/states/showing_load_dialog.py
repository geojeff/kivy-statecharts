#!/usr/bin/env python
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy_statecharts.system.state import State

############################
# LoadDialog and its state
#
class LoadDialog(FloatLayout):
    statechart = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SHOWING_LOAD_DIALOG(State):
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['name'] = 'SHOWING_LOAD_DIALOG'
        super(SHOWING_LOAD_DIALOG, self).__init__(**kwargs)

    def enterState(self, context=None):
        print 'SHOWING_LOAD_DIALOG/enterState'
        content = LoadDialog(load=self.load, cancel=self.cancel, statechart=self.statechart)
        self._popup = Popup(title="load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
        
    def exitState(self, context=None):
        print 'SHOWING_LOAD_DIALOG/exitState'
        self._popup.dismiss()
         
    def load(self, *l):
        path = filechooser.path
        filename = filechooser.selection
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.statechart.gotoState('SHOWING_MAIN')

    def cancel(self, *l):
        self.statechart.gotoState('SHOWING_MAIN')
