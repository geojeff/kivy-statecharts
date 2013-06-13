from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State


class ShowingMainScreen(State):

    def __init__(self, **kwargs):
        super(ShowingMainScreen, self).__init__(**kwargs)

    def enter_state(self, context=None):

        if not 'Main' in self.statechart.app.screen_manager.screen_names:

            self.app = self.statechart.app

            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=30)

            button = ToggleButton(text='Main',
                                  color=[1.0, 1.0, 1.0, .9],
                                  bold=True,
                                  group='screen manager buttons')
            button.state = 'down'
            toolbar.add_widget(button)

            button = ToggleButton(
                    text='DrawingArea', group='screen manager buttons')
            button.bind(on_press=self.go_to_drawing_area)

            toolbar.add_widget(button)

            view.add_widget(toolbar)

            state_diagram_description = """
This example app helps with [b]drawing a statechart[/b]:

    A statechart diagram consists of shapes linked by connectors, showing the
    flow of action in an app.

        Individual states have primary shapes, such as triangles and
        rectangles.

        Connectors includ lines...

    State action methods are normal Python methods, with a signature for acting
    as proper statechart actions, servicing the events sent to the statechart.

    A state can also include normal properties and utility methods to do the
    work required by the actions."""

            scrollview = ScrollView()
            scrollview.add_widget(
                    Label(text=state_diagram_description, markup=True))

            view.add_widget(scrollview)

            screen = Screen(name='Main')
            screen.add_widget(view)

            self.app.screen_manager.add_widget(screen)

        if self.app.screen_manager.current != 'Main':
            self.app.screen_manager.current = 'Main'

    def exit_state(self, context=None):
        pass

    def go_to_drawing_area(self, *args):
        self.go_to_state('ShowingDrawingArea')
