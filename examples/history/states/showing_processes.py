from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView
from kivy.uix.treeview import TreeViewNode

from kivy.properties import BooleanProperty
from kivy.properties import DictProperty
from kivy.properties import StringProperty

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


class TreeViewToggleButton(ToggleButton, TreeViewNode):
    pass


class TreeViewLabel(Label, TreeViewNode):
    pass


class StatesTreeView(TreeView):

    allow_collapse = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(StatesTreeView, self).__init__(**kwargs)

    def toggle_node(self, node):
        '''Toggle the state of the node (open/collapse).
        '''
        if not self.allow_collapse and node.is_open:
            return
        node.is_open = not node.is_open
        if node.is_open:
            if self.load_func and not node.is_loaded:
                self._do_node_load(node)
            self.dispatch('on_node_expand', node)
        else:
            if self.allow_collapse:
                self.dispatch('on_node_collapse', node)

        self._trigger_layout()


class ShowingProcessesScreen(State):

    history_labels = DictProperty({})

    history_traversal_method = StringProperty('shallow')

    def enter_state(self, context=None):

        if not 'Processes' in self.statechart.app.sm.screen_names:

            # Convenience references:

            self.app = self.statechart.app

            view = GridLayout(cols=1, spacing=20)

            toolbar = BoxLayout(size_hint=(1.0, None), height=30)

            button = ToggleButton(text='Main', group='screen manager buttons')
            button.bind(on_press=self.go_to_main)
            toolbar.add_widget(button)

            button = ToggleButton(text='Processes',
                                  color=[1.0, 1.0, 1.0, .9],
                                  bold=True,
                                  group='screen manager buttons')
            button.state = 'down'
            toolbar.add_widget(button)

            view.add_widget(toolbar)

            # Radio buttons for shallow vs. deep history state traversal.

            history_traversal_toolbar = BoxLayout(
                    size_hint=(1.0, None), height=40)
            history_traversal_toolbar.add_widget(
                    Label(text="History Traversal Method:"))
            shallow_button = ToggleButton(
                    text='Shallow (non-recursive)',
                    size_hint=(1.0, None),
                    height=30,
                    group='history state traversal')
            deep_button = ToggleButton(
                    text='Deep (recursive)',
                    size_hint=(1.0, None),
                    height=30,
                    group='history state traversal')
            history_traversal_toolbar.add_widget(shallow_button)
            history_traversal_toolbar.add_widget(deep_button)

            shallow_button.bind(on_press=self.update_history_traversal_method)
            deep_button.bind(on_press=self.update_history_traversal_method)

            shallow_button.state = 'down'

            view.add_widget(history_traversal_toolbar)

            # go_to_history_state buttons

            buttons_box = GridLayout(
                    rows=2, cols=2, size_hint=(1.0, None), height=90)
            buttons_box.add_widget(Label(
                    text='Click buttons to call go_to_history_state():',
                    size_hint=(1.0, None), height=30))
            buttons_box.add_widget(Label(text=''))

            buttons_box.add_widget(Label(text=''))
            go_to_buttons_grid = GridLayout(
                    cols=7, size_hint=(1.0, None), height=60, spacing=10)
            for state_name in ['A', 'C', 'G', 'H', 'D', 'I', 'J',
                               'B', 'E', 'K', 'L', 'F', 'M', 'N']:
                button = Button(text=state_name,
                                size_hint=(None, None),
                                size=(35, 30))
                button.bind(on_press=self.history_button_clicked)
                go_to_buttons_grid.add_widget(button)

            buttons_box.add_widget(go_to_buttons_grid)

            view.add_widget(buttons_box)

            # Lower panel for the state tree, history labels, and help text.

            lower_panel = GridLayout(cols=3,
                                     padding=[20, 0, 20, 0],
                                     size_hint=(1.0, None),
                                     height=480,
                                     spacing=20,
                                     minimum=200)

            # State tree

            tree_view_panel = GridLayout(cols=1)
            tree_view_panel.add_widget(Label(text='Statechart',
                                             size_hint=(None, None),
                                             width=30,
                                             height=30))
            tree_view = StatesTreeView(
                    root_options=dict(text='Steps in Processes A and B'),
                    hide_root=True,
                    indent_level=40)

            self.populate_tree_view(
                    tree_view, None, self.statechart.get_state('A'))

            self.populate_tree_view(
                    tree_view, None, self.statechart.get_state('B'))

            tree_view_panel.add_widget(tree_view)
            lower_panel.add_widget(tree_view_panel)

            # History labels (for each state in tree)

            history_labels_list = GridLayout(cols=1)
            history_labels_list.add_widget(Label(text='History States',
                                                 size_hint=(None, None),
                                                 width=30,
                                                 height=30))
            self.populate_history_labels_list(
                    history_labels_list, self.statechart.get_state('A'))
            self.populate_history_labels_list(
                    history_labels_list, self.statechart.get_state('B'))
            lower_panel.add_widget(history_labels_list)

            # Help text

            help_text_panel = GridLayout(cols=1)
            help_text_panel.add_widget(Label(text="Instructions"))

            help_text = GridLayout(
                    cols=1, size_hint=(1.0, None), height=450)

            help_text.add_widget(self.make_justified_label(
                ("The state hierarchies for Processes A and B are shown at "
                 "left. Along the side, in parentheses, are the history "
                 "states of each state. Click on a state directly to "
                 "simulate performing steps in the process."), 'justify'))
            help_text.add_widget(self.make_justified_label(
                ("Click the history buttons in the toolbars above to go to "
                 "the history state of a state. If a state doesn't yet have "
                 "a history state, it will simply be visited."), 'justify'))
            help_text.add_widget(self.make_justified_label(
                ("View the terminal console to follow the action, and see "
                 "current state."), 'justify'))
            help_text_panel.add_widget(help_text)

            lower_panel.add_widget(help_text_panel)

            view.add_widget(lower_panel)

            # Finally, add to this screen to the screen manager.

            screen = Screen(name='Processes')
            screen.add_widget(view)
            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Processes':
            self.app.sm.current = 'Processes'

    def exit_state(self, context=None):
        pass

    def make_justified_label(self, text, justification):
        help_label = Label(text=text, halign=justification)
        # Bind size of rendered label to text_size, for justification.
        help_label.bind(size=help_label.setter('text_size'))
        return help_label

    def populate_tree_view(self, tree_view, parent, state):

        state_name = state.__class__.__name__

        if parent is None:
            button = TreeViewToggleButton(text=state_name,
                                    size_hint=(None, None),
                                    width=30,
                                    height=30,
                                    is_open=True)
            tree_node = tree_view.add_node(button)
        else:
            button = TreeViewToggleButton(text=state_name,
                                    size_hint=(None, None),
                                    width=30,
                                    height=30,
                                    is_open=True)
            tree_node = tree_view.add_node(button, parent)

        button.bind(on_press=self.state_button_clicked)
        self.statechart.app.state_toggle_buttons[state_name] = button

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

        recursive = \
                False if self.history_traversal_method == 'shallow' else True

        self.statechart.go_to_history_state(
                target_state,
                # Comments say that from_current_state is needed (probably)
                # when there are concurrent states. Otherwise, not.
                #from_current_state=self.statechart.current_states[-1],
                from_current_state=None,
                recursive=recursive)

    def update_history_traversal_method(self, *args):
        if args[0].text.startswith('Shallow'):
            self.history_traversal_method = 'shallow'
        else:
            self.history_traversal_method = 'deep'
