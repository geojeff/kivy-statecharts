from kivy.app import App

from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from states.showing_main import ShowingMainScreen
from states.showing_processes import ShowingProcessesScreen

# NOTE: The only thing that happens on entry or exit of a state is the toggling
#       of the button represening the state. Toggle buttons have their own
#       state property, which is either 'normal' or 'down' (don't confust that
#       with the use of the term state for the statechart).

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
            kwargs['ShowingProcessesScreen'] = ShowingProcessesScreen
            super(AppStatechart.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'C'
                super(AppStatechart.RootState.A, self).__init__(**kwargs)

            def enter_state(self, context=None):
                self.statechart.app.state_toggle_buttons['A'].state = 'down'

            def exit_state(self, context=None):
                self.statechart.app.state_toggle_buttons['A'].state = 'normal'

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'G'
                    super(AppStatechart.RootState.A.C, self).__init__(**kwargs)

                def enter_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['C'].state = 'down'

                def exit_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['C'].state = 'normal'

                class G(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.A.C.G,self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['G'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['G'].state = 'normal'

                class H(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.A.C.H, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['H'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['H'].state = 'normal'

            class D(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'I'
                    super(AppStatechart.RootState.A.D, self).__init__(**kwargs)

                def enter_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['D'].state = 'down'

                def exit_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['D'].state = 'normal'

                class I(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.A.D.I, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['I'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['I'].state = 'normal'

                class J(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.A.D.J, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['J'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['J'].state = 'normal'

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'E'
                super(AppStatechart.RootState.B, self).__init__(**kwargs)

            def enter_state(self, context=None):
                self.statechart.app.state_toggle_buttons['B'].state = 'down'

            def exit_state(self, context=None):
                self.statechart.app.state_toggle_buttons['B'].state = 'normal'

            class E(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'K'
                    super(AppStatechart.RootState.B.E, self).__init__(**kwargs)

                def enter_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['E'].state = 'down'

                def exit_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['E'].state = 'normal'

                class K(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.B.E.K, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['K'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['K'].state = 'normal'

                class L(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.B.E.L, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['L'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['L'].state = 'normal'

            class F(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'M'
                    super(AppStatechart.RootState.B.F, self).__init__(**kwargs)

                def enter_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['F'].state = 'down'

                def exit_state(self, context=None):
                    self.statechart.app.state_toggle_buttons['F'].state = 'normal'

                class M(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.B.F.M, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['M'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['M'].state = 'normal'

                class N(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.B.F.N, self).__init__(**kwargs)

                    def enter_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['N'].state = 'down'

                    def exit_state(self, context=None):
                        self.statechart.app.state_toggle_buttons['N'].state = 'normal'


class MainScreen(FloatLayout):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class HistoryApp(App):
    '''An app for simulation of high-level processes, each containing
    subprocesses. Serves to illustrate process interruptions and restarts.
    Restart operations will use the history state methods to resume work, using
    two approaches: shallow (starting over) and deep (picking up where
    processing stopped, at the deeper subprocess).
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


if __name__ in ('__main__'):
    HistoryApp().run()
