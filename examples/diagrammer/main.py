import kivy
kivy.require('1.6.0')

from kivy.app import App

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from statechart.statechart import AppStatechart

from controllers.shapes_controller import ShapesController
from controllers.connections_controller import ConnectionsController
from controllers.current_shape_controller import CurrentShapeController
from controllers.current_connection_controller import CurrentConnectionController


class RootWidget(GridLayout):

    bg = ObjectProperty(None)
    connector = ObjectProperty(None)
    connector_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.bg.bind(points=self.points_added)

    def points_added(self, *args):
        #print self.bg.points
        pass


class MainScreen(FloatLayout):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DiagrammerApp(App):
    '''An app for drawing statechart diagrams, serving to illustrate lower
    level graphics operations and statecharts, as well as the normal higher
    level states.
    '''

    statechart = ObjectProperty(None)
    screen_manager = ObjectProperty(None)
    main_screen = ObjectProperty(None)

    drawing_area = ObjectProperty(None, allownone=True)

    # List controllers mediate for a list of data and offer filtering, and
    # a place to have alias properties and the like.
    shapes_controller = ObjectProperty(None)
    connections_controller = ObjectProperty(None)

    # Object controllers mediate for a single data item, providing a place for
    # establishing bindings to other controllers/properties, especially to the
    # single selection of an associated list controller. Object controllers may
    # also contain transformation methods of the content item.
    current_shape_controller = ObjectProperty(None)
    current_connection_controller = ObjectProperty(None)

    # Adapters mediate data and create/cache views for parent collection views.
    tools_adapter = ObjectProperty(None)
    generic_shape_tools_adapter = ObjectProperty(None)
    state_shape_tools_adapter = ObjectProperty(None)

    def build(self):

        self.screen_manager = ScreenManager()

        return self.screen_manager

    def on_start(self):
        self.statechart = AppStatechart()
        self.statechart.init_statechart()


if __name__ in ('__main__'):
    DiagrammerApp().run()
