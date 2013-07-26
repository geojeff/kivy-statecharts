from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from statecharts.main.states.starting_up import StartingUp
from statecharts.main.states.showing_help import ShowingHelpScreen
from statecharts.main.states.showing_drawing_area import ShowingDrawingScreen


class AppStatechart(StatechartManager):

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState

        super(AppStatechart, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'StartingUp'
            kwargs['StartingUp'] = StartingUp
            kwargs['ShowingHelpScreen'] = ShowingHelpScreen
            kwargs['ShowingDrawingScreen'] = ShowingDrawingScreen
            super(AppStatechart.RootState, self).__init__(**kwargs)
