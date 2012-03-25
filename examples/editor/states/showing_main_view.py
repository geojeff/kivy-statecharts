#!/usr/bin/env python
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.statechart.system.state import State

###############################
# MainView and the main state
#
class MainView(FloatLayout):
    app = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

class SHOWING_MAIN(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'SHOWING_MAIN'
        super(SHOWING_MAIN, self).__init__(**kwargs)

    def enterState(self, context=None):
        print 'SHOWING_MAIN/enterState'
        setattr(self.statechart.app, 'statechart', self.statechart) # hacky?
                
    def exitState(self, context=None):
        print 'SHOWING_MAIN/exitState'

    def show_load(self, *l):
        self.statechart.gotoState('SHOWING_LOAD_DIALOG')

    def show_save(self, *l):
        self.statechart.gotoState('SHOWING_SAVE_DIALOG')
