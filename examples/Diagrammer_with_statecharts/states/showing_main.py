from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


class ShowingMainScreen(State):

    def enter_state(self, context=None):

        if not 'Main' in self.statechart.app.sm.screen_names:

            self.app = self.statechart.app

            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            label = Label(text='Main', color=[.8, .8, .8, .8], bold=True)
            toolbar.add_widget(label)

            button = Button(text='Drawing Area')
            button.bind(on_press=self.go_to_drawingarea)
            toolbar.add_widget(button)

            view.add_widget(toolbar)

            diagrammer_state_description = """
            State diagrams are used to give an abstract 
            description of the behavior of a system. This behavior 
            is analyzed and represented in series of events, that 
            could occur in one or more possible states. Hereby "each 
            diagram usually represents objects of a single class and 
            track the different states of its objects through the system.
"""

            view.add_widget(Label(text=diagrammer_state_description, color=[.6,.7,.1,1],font_size='18dp',markup=True))

            screen = Screen(name='Main')
            screen.add_widget(view)

            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Main':
            self.app.sm.current = 'Main'

    def exit_state(self, context=None):
        pass

    def go_to_drawingarea(self, *args):
        self.go_to_state('ShowingDrawingAreaScreen')
