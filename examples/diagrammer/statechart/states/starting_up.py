from kivy_statecharts.system.state import State

from adapters.state_drawing_mode_adapter import StateDrawingModeAdapter


class StartingUp(State):

    def __init__(self, **kwargs):
        super(StartingUp, self).__init__(**kwargs)

    def enter_state(self, context=None):

        # Initialize adapters.

        self.statechart.app.state_drawing_mode_adapter = \
                StateDrawingModeAdapter()

        self.go_to_showing_help()

    def exit_state(self, context=None):
        pass

    def go_to_showing_help(self, *args):
        self.go_to_state('ShowingHelpScreen')
