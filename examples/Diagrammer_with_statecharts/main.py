from kivy.app import App

from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from states.showing_main import ShowingMainScreen
from states.showing_drawingarea import ShowingDrawingAreaScreen


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState

        super(AppStatechart, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'ShowingMainScreen'
            kwargs['ShowingMainScreen'] = ShowingMainScreen
            kwargs['ShowingDrawingAreaScreen'] = ShowingDrawingAreaScreen
            super(AppStatechart.RootState, self).__init__(**kwargs)

        class DiagramState(State):
            def __init__(self, **kwargs):
                super(AppStatechart.RootState.DiagramState, self).__init__(**kwargs)

            def enter_state(self, context=None):
                pass
            def exit_state(self, context=None):
                pass

class MainScreen(FloatLayout):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DiagrammerApp(App):
    '''An app for creating statechart diagrams.
    '''

    statechart = ObjectProperty(None)
    sm = ObjectProperty(None)
    main_screen = ObjectProperty(None)
    state_toggle_buttons = DictProperty({})

    def build(self):

        self.sm = ScreenManager()
        return self.sm

        self.root = MainScreen(app=self)
        self.main_screen = self.root

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.init_statechart()
	
	def on_stop(self):
		print '\nThanks using DiagrammerApp\n'


if __name__ in ('__main__'):
    DiagrammerApp().run()
