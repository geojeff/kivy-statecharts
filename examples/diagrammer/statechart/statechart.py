from kivy.properties import ObjectProperty

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from states.starting_up import StartingUp
from states.showing_help import ShowingHelpScreen
from states.showing_drawing_area import ShowingDrawingArea


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState

        super(AppStatechart, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'StartingUp'
            kwargs['StartingUp'] = StartingUp
            kwargs['ShowingHelpScreen'] = ShowingHelpScreen
            kwargs['ShowingDrawingArea'] = ShowingDrawingArea
            super(AppStatechart.RootState, self).__init__(**kwargs)
