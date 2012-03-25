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

############################
# SaveDialog and its state
#
class SaveDialog(FloatLayout):
    statechart = ObjectProperty(None)
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SHOWING_SAVE_DIALOG(State):
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['name'] = 'SHOWING_SAVE_DIALOG'
        super(SHOWING_SAVE_DIALOG, self).__init__(**kwargs)

    def enterState(self, context=None):
        print 'SHOWING_SAVE_DIALOG/enterState'
        content = SaveDialog(save=self.save, cancel=self.cancel, statechart=self.statechart)
        self._popup = Popup(title="save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def exitState(self, context=None):
        print 'SHOWING_SAVE_DIALOG/exitState'
        self._popup.dismiss()
         
    def save(self, *l):
        path = filechooser.path
        filename = text_input.text
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.statechart.gotoState('SHOWING_MAIN')

    def cancel(self, *l):
        self.statechart.gotoState('SHOWING_MAIN')

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

