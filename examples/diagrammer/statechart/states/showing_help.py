from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State


class ShowingHelpScreen(State):

    def __init__(self, **kwargs):
        super(ShowingHelpScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

        if not 'Help' in self.app.screen_manager.screen_names:

            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=30)

            button = ToggleButton(text='Help',
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
After app loads, you see a blank rectangle display on the right for the drawing
area. Various parts of the app are under construction and development, so
please discuss in #kivy for current status if you really want to kick the
tires. NOTE: N.I.Y. = Not Implemented Yet, when you see it in the UI.

In the main drawing menu, only the State menu has functionality so far
(Triangle, Rectangle, Pentagon). You can try this:

Drawing Shapes

- Try out the menu to select the State menu to select different shapes to
   draw.

- Touch (or click) once in the drawing area to draw a shape.
  Touch again in another area to draw a second shape.

- Touch the perimeter of a shape and drag to move it.

- Touch and drag in the center of one rectangle to the center of another.

Drawing Connections

- On touch up, bubbles will appear on either end of the connection.  In a given
  bubble, touch and drag within the Drag button to move the connection point
  for the end (dragging out of the drag button will terminate the move,
  presently -- needs event handling in state for drawing_area -- and a better
  way of doing this generally). Repeat drag ops on the Drag button, for now to
  drag the given connection point further, clockwise (too jerky and skips for
  now). Once the connection point is ok, touch Accept.

Connecting Shapes

You can add more shapes and connections. You can move shapes with
connections, and the connections will adjust.

Shape Properties

- Touch and release on a shape's perimeter to edit its properties. For now
this is a popup, but it rather obscures what you need to see."""

            scrollview = ScrollView()
            scrollview.add_widget(
                    Label(text=state_diagram_description, markup=True))

            view.add_widget(scrollview)

            screen = Screen(name='Help')
            screen.add_widget(view)

            self.app.screen_manager.add_widget(screen)

        if self.app.screen_manager.current != 'Help':
            self.app.screen_manager.current = 'Help'

    def exit_state(self, context=None):
        pass

    def go_to_drawing_area(self, *args):
        self.go_to_state('ShowingDrawingScreen')
