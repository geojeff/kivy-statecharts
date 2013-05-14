from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView
from kivy.uix.treeview import TreeViewNode

from kivy.properties import DictProperty

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


class TreeViewToggleButton(ToggleButton, TreeViewNode):
    pass


class TreeViewLabel(Label, TreeViewNode):
    pass


class ShowingProcessesScreen(State):

    history_labels = DictProperty({})

    def enter_state(self, context=None):

        if not 'Processes' in self.statechart.app.sm.screen_names:

            # Convenience references:
            self.app = self.statechart.app

            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            button = Button(text='Main')
            button.bind(on_press=self.go_to_main)
            toolbar.add_widget(button)

            label = Label(text='Processes', color=[.8, .8, .8, .8], bold=True)
            toolbar.add_widget(label)

            # Process A toolbar

            view.add_widget(toolbar)

            view.add_widget(Label(
                text=('Process A Hierarchy -- Click buttons to call '
                      'go_to_history_state(A,... calls:'),
                size_hint=(1.0, None), height=30))

            history_toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            for state_name in ['A', 'C', 'G', 'H', 'D', 'I', 'J']:
                button = Button(text=state_name)
                button.bind(on_press=self.history_button_clicked)
                history_toolbar.add_widget(button)

            view.add_widget(history_toolbar)

            # Process B toolbar

            view.add_widget(Label(
                text=('Process B Hierarchy -- Click buttons to '
                      'call go_to_history_state(B,... calls:'),
                size_hint=(1.0, None), height=30))

            history_toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            for state_name in ['B', 'E', 'K', 'L', 'F', 'M', 'N']:
                button = Button(text=state_name)
                button.bind(on_press=self.history_button_clicked)
                history_toolbar.add_widget(button)

            view.add_widget(history_toolbar)

            # Lower panel for the state tree, history labels, and help text.

            lower_panel = BoxLayout()

            # State tree

            tree_view = TreeView(
                    root_options=dict(text='Steps in Processes A and B'),
                    hide_root=True,
                    indent_level=40)

            self.populate_tree_view(
                    tree_view, None, self.statechart.get_state('A'))

            self.populate_tree_view(
                    tree_view, None, self.statechart.get_state('B'))

            lower_panel.add_widget(tree_view)

            # History labels (for each state in tree)

            history_labels_list = BoxLayout(orientation='vertical',
                    pos_hint={'x': 1.0, 'y': .2})
            self.populate_history_labels_list(
                    history_labels_list, self.statechart.get_state('A'))
            self.populate_history_labels_list(
                    history_labels_list, self.statechart.get_state('B'))
            lower_panel.add_widget(history_labels_list)

            # Help text

            lower_panel.add_widget(Label(text="""The state hierarchies for
Processes A and B are shown
at left. Along the side, in
parentheses, are the history
states of each state. Click
on a state directly to
simulate performing steps in
the process.

Click the history buttons
in the toolbars above to go
to the history state of a
state. If a state doesn't
yet have a history state,
it will simply be visited.

View the terminal console to
follow the action, and see
current state."""))

            view.add_widget(lower_panel)

            # Finally, add to this screen to the screen manager.

            screen = Screen(name='Processes')
            screen.add_widget(view)
            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Processes':
            self.app.sm.current = 'Processes'

    def exit_state(self, context=None):
        pass

    def populate_tree_view(self, tree_view, parent, state):

        if parent is None:
            button = TreeViewToggleButton(text=state.__class__.__name__,
                                    size_hint=(None, None),
                                    width=30,
                                    height=30,
                                    is_open=True)
            tree_node = tree_view.add_node(button)
        else:
            button = TreeViewToggleButton(text=state.__class__.__name__,
                                    size_hint=(None, None),
                                    width=30,
                                    height=30,
                                    is_open=True)
            tree_node = tree_view.add_node(button, parent)

        button.bind(on_press=self.state_button_clicked)
        self.statechart.app.state_toggle_buttons[state.__class__.__name__] = button

        for substate in state.substates:
            self.populate_tree_view(tree_view, tree_node, substate)

    def populate_history_labels_list(self, history_labels_list, state):

        label = Label(text='( )',
                      size_hint=(None, None),
                      width=30,
                      height=30)

        history_labels_list.add_widget(label)

        state.bind(history_state=self.update_history_label)
        self.history_labels[state.__class__.__name__] = label

        for substate in state.substates:
            self.populate_history_labels_list(history_labels_list, substate)

    def go_to_main(self, *args):
        self.go_to_state('ShowingMainScreen')

    def state_button_clicked(self, *args):
        self.statechart.go_to_state(args[0].text)

    def update_history_label(self, *args):
        state, history_state = args
        label = self.history_labels[state.__class__.__name__]
        label.text = "({0})".format(history_state.__class__.__name__)

    def history_button_clicked(self, *args):
        target_state = args[0].text

        self.statechart.go_to_history_state(
                target_state,
                from_current_state=self.statechart.current_states[-1],
                recursive=False)
