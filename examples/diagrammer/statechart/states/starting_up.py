from kivy.app import App

from kivy_statecharts.system.state import State

from controllers.shapes_controller import ShapesController
from controllers.current_shape_controller import CurrentShapeController
from controllers.connections_controller import ConnectionsController
from controllers.current_connection_controller \
        import CurrentConnectionController

from adapters.tools_adapter import ToolsAdapter
from adapters.generic_shape_tools_adapter import GenericShapeToolsAdapter
from adapters.state_shape_tools_adapter import StateShapeToolsAdapter


class StartingUp(State):

    def __init__(self, **kwargs):

        super(StartingUp, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

        # Initialize controllers (When shapes are stored in files, there
        # will be a "LoadingData" state, from which we would come after the
        # data is loaded -- and we would be setting the shapes, points, and
        # other data into controllers here).
        self.app.shapes_controller = ShapesController(
                selection_mode='single',
                allow_empty_selection=False)

        self.app.connections_controller = ConnectionsController(
                selection_mode='multiple')

        self.app.current_shape_controller = CurrentShapeController()

        self.app.current_connection_controller = CurrentConnectionController()

        # Set up bindings between object controllers and the selection in their
        # associated list controllers.
        self.app.shapes_controller.bind(
                selection=self.app.current_shape_controller.update)

        self.app.connections_controller.bind(
                selection=self.app.current_connection_controller.update)

        # Initialize adapters.
        self.app.generic_shape_tools_adapter = GenericShapeToolsAdapter()
        self.app.state_shape_tools_adapter = StateShapeToolsAdapter()

        # Do the tool adapter last, because it has bindings to the others.
        self.app.tools_adapter = ToolsAdapter()

        self.go_to_showing_help()

    def exit_state(self, context=None):
        pass

    def go_to_showing_help(self, *args):
        self.go_to_state('ShowingHelpScreen')
