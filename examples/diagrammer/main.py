import kivy
kivy.require('1.6.0')

from kivy.app import App

from kivy.binding import DataBinding

from kivy.enums import binding_modes

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from statecharts.main.statechart import AppStatechart

from controllers.shapes import ShapesController
from controllers.current_shape import CurrentShapeController

from controllers.connections import ConnectionsController
from controllers.current_connection import CurrentConnectionController

from controllers.generic_shape_tools import GenericShapeToolsController
from controllers.current_generic_shape_tool import CurrentGenericShapeToolController

from controllers.state_shape_tools import StateShapeToolsController
from controllers.current_state_shape_tool import CurrentStateShapeToolController

from controllers.shape_tools import ShapeToolsController
from controllers.current_shape_tool import CurrentShapeToolController


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

    # Object controllers mediate for a single data item, providing a place for
    # establishing bindings to other controllers/properties, especially to the
    # single selection of an associated list controller. Object controllers may
    # also contain transformation methods of the item.

    shapes_controller = ObjectProperty(None)
    current_shape_controller = ObjectProperty(None)

    moving_shape = ObjectProperty(None)
    connecting_shape = ObjectProperty(None)

    connections_controller = ObjectProperty(None)
    current_connection_controller = ObjectProperty(None)

    tools_controller = ObjectProperty(None)
    current_tool_controller = ObjectProperty(None)

    generic_shape_tools_controller = ObjectProperty(None)
    current_generic_shape_tool_controller = ObjectProperty(None)

    state_shape_tools_controller = ObjectProperty(None)
    current_state_shape_tool_controller = ObjectProperty(None)

    shape_tools_controller = ObjectProperty(None)
    current_shape_tool_controller = ObjectProperty(None)

    def build(self):

        self.screen_manager = ScreenManager()

        return self.screen_manager

    def on_start(self):

        # Create the controllers, which are stored on the app.
        self.shapes_controller = ShapesController(
                selection_mode='single',
                allow_empty_selection=False)

        self.current_shape_controller = CurrentShapeController(
                data_binding=DataBinding(
                    source=self.shapes_controller,
                    prop='selection',
                    mode=binding_modes.FIRST_ITEM))

        self.connections_controller = ConnectionsController(
                selection_mode='multiple')

        self.current_connection_controller = CurrentConnectionController(
                data_binding=DataBinding(
                    source=self.connections_controller,
                    prop='selection',
                    mode=binding_modes.FIRST_ITEM))

        self.generic_shape_tools_controller = GenericShapeToolsController()

        self.current_generic_shape_tool_controller = CurrentGenericShapeToolController(
                data_binding = DataBinding(
                    source=self.generic_shape_tools_controller,
                    prop='selection',
                    mode=binding_modes.FIRST_ITEM))

        self.state_shape_tools_controller = StateShapeToolsController()

        self.current_state_shape_tool_controller = CurrentStateShapeToolController(
                data_binding = DataBinding(
                    source=self.state_shape_tools_controller,
                    prop='selection',
                    mode=binding_modes.FIRST_ITEM))

        self.shape_tools_controller = ShapeToolsController()

        self.current_shape_tool_controller = CurrentShapeToolController(
                data_binding = DataBinding(
                    source=self.shape_tools_controller,
                    prop='selection',
                    mode=binding_modes.FIRST_ITEM))

        self.statechart = AppStatechart()

        self.statechart.init_statechart()

if __name__ in ('__main__'):
    DiagrammerApp().run()
