from kivy.app import App

from kivy_statecharts.system.state import State

from adapters.tools_adapter import ToolsAdapter
from adapters.generic_shape_tools_adapter import GenericShapeToolsAdapter
from adapters.state_shape_tools_adapter import StateShapeToolsAdapter


class StartingUp(State):

    def __init__(self, **kwargs):

        super(StartingUp, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

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
