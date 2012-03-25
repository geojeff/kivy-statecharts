#!/usr/bin/env python
from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

from states.showing_main_view import MainView
from states.showing_main_view import SHOWING_MAIN
from states.showing_load_dialog import SHOWING_LOAD_DIALOG
from states.showing_save_dialog import SHOWING_SAVE_DIALOG

###########################
# RootState of statechart
#
class RootState(State):
    def __init__(self, **kwargs):
        super(RootState, self).__init__(**kwargs)
    
    initialSubstate = 'SHOWING_MAIN'
    
    SHOWING_MAIN = SHOWING_MAIN
    SHOWING_LOAD_DIALOG  = SHOWING_LOAD_DIALOG
    SHOWING_SAVE_DIALOG  = SHOWING_SAVE_DIALOG

    # Not used at the moment. An event handler can handle multiple events
    # for the state. Compare this to having discrete methods, e.g. show_load
    # in SHOWING_MAIN state.
    @State.eventHandler(['print initial substate', 'print states'])
    def printInfo(self, infoType):
        if infoType is 'print initial substate':
            print 'INFO:', self.initialSubstate
        elif infoType is 'print states':
            print 'INFO:', (self[key].name for key in dir(self) if issubclass(self[key], State))

##############
# Statechart
#
class AppStatechart(StatechartManager):
    def __init__(self, app, **kw):
        self.app = app
        self.trace = True
        self.rootState = RootState
        super(AppStatechart, self).__init__(**kw)

#######
# App
#
class Editor(App):
    statechart = ObjectProperty(None)

    def build(self):
        return MainView(app=self)

if __name__ == '__main__':
    app = Editor()
    statechart = AppStatechart(app)
    app.run()

