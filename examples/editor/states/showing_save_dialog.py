#!/usr/bin/env python
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy_statechart.system.state import State

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
