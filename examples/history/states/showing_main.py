from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


class ShowingMainScreen(State):

    def enter_state(self, context=None):

        if not 'Main' in self.statechart.app.sm.screen_names:

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
                    text='Processes', group='screen manager buttons')
            button.bind(on_press=self.go_to_processes)

            toolbar.add_widget(button)

            view.add_widget(toolbar)

            history_state_description = """
This example illustrates [b]history states[/b]:

    First, for this example, imagine a multi-step process that can be
    interrupted.

        For example, in a game, there could be an activity to search for a
        series of hidden items required to finish a task. If the game allows
        the player to break out of the search activity to do something else,
        but to return at will, there needs to be a way to reestablish the state
        of gameplay for the task.

        For another example, consider an application for controlling testing of
        a product. Perhaps testing is dependent on available tools, which vary
        at random, such that a worker must be able to stop and start different
        parts of the testing process. User interface panels for each specific
        test would need to show the state of testing when a given test is
        resumed.

        For one more example, imagine a questionnaire for realtime problem
        reporting that has just a few questions in sequence, but each main
        question could have subquestions (1, 2, 3, ...) and each of these
        subquestions could have parts A, B, C, D, etc. From any question or
        subquestion in a deep hierarchy, the answer could result in an exit
        altogether, if during the process a solution is realized.  Or, at any
        point there could be a transition triggered to go to an analysis step
        that would take multiple factors about the current environment into
        account, and would return to the questionnaire, passing the results of
        the analysis upon re-entry, and depending on that result, processing
        could be reestablished as it was, or there could be a conditional
        transition to one of several states previously unvisited.

    A history state is something like a marker state, marking a position within
    a sequence of state transitions in a self-contained process.

    History states allow returning to a process at the place where processing
    was interrupted ([i]deep[/i] history transition, back to the specific place
    where the process left off), or to restart the process altogether
    ([i]shallow[/i] history transition, back to the initial state of the entire
    process), or a more complex return path determined by analysis of partial
    results or conditions."""

            scrollview = ScrollView()
            scrollview.add_widget(
                    Label(text=history_state_description, markup=True))

            view.add_widget(scrollview)

            screen = Screen(name='Main')
            screen.add_widget(view)

            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Main':
            self.app.sm.current = 'Main'

    def exit_state(self, context=None):
        pass

    def go_to_processes(self, *args):
        self.go_to_state('ShowingProcessesScreen')
