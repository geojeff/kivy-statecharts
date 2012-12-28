from kivy.adapters.dictadapter import DictAdapter

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemLabel
from kivy.uix.textinput import TextInput

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


class ShowingSearchScreen(State):

    def enter_state(self, context=None):
        print 'ShowingSearchScreen/enter_state'

        if not 'Search' in self.statechart.app.sm.screen_names:

            self.search_results = []

            self.app = self.statechart.app

            self.search_criteria = {}

            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            button = Button(text='Lists')
            button.bind(on_press=self.go_to_lists)
            toolbar.add_widget(button)

            label = Label(text='Search', color=[.8, .8, .8, .8], bold=True)
            toolbar.add_widget(label)

            button = Button(text='Data')
            button.bind(on_press=self.go_to_data)
            toolbar.add_widget(button)

            button = Button(text='Detail')
            button.bind(on_press=self.go_to_detail)
            toolbar.add_widget(button)

            view.add_widget(toolbar)

            body_view = BoxLayout()

            left_view = BoxLayout(size_hint=(0.7, 1.0), orientation='vertical')

            left_view.add_widget(Label(size_hint=(1.0, 0.2),
                                       text="""[b]Search Criteria:[/b]

    Enter the lower and upper bounds of search criteria in the text
    entry boxes. Each time you hit the [i]ENTER[/i] key in a text entry box,
    the search results shown in the list on the right will be updated.""",
                                       markup=True))

            search_criteria_view = BoxLayout(orientation='vertical')

            props = [prop for prop in self.statechart.data['Apple']
                         if prop != 'name']

            for prop in sorted(props):
                search_box_view = BoxLayout(size_hint=(1.0, None), height=40)

                text_input = TextInput(text='', multiline=False)
                text_input.id = "<: {0}".format(prop)
                text_input.bind(
                    on_text_validate=self.criterion_entered)
                search_box_view.add_widget(text_input)

                search_box_view.add_widget(Label(text="> {0} <".format(prop)))

                text_input = TextInput(text='', multiline=False)
                text_input.id = ">: {0}".format(prop)
                text_input.bind(
                    on_text_validate=self.criterion_entered)
                search_box_view.add_widget(text_input)

                search_criteria_view.add_widget(search_box_view)

            left_view.add_widget(search_criteria_view)

            body_view.add_widget(left_view)

            right_view = BoxLayout(size_hint=(0.3, 1.0),
                                   orientation='vertical')

            right_view.add_widget(Label(size_hint=(1.0, 0.2),
                                        text="Search Results (red):"))

            self.all_fruits = sorted(self.statechart.data.keys())

            self.results_fruits_dict_adapter = DictAdapter(
                sorted_keys=self.all_fruits,
                data=self.statechart.data,
                args_converter=self.list_item_args_converter,
                selection_mode='none',
                allow_empty_selection=True,
                cls=ListItemLabel)

            right_view.add_widget(
                    ListView(size_hint=(1.0, 0.8),
                             adapter=self.results_fruits_dict_adapter))

            body_view.add_widget(right_view)

            view.add_widget(body_view)

            screen = Screen(name='Search')
            screen.add_widget(view)

            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Search':
            self.app.sm.current = 'Search'

    def list_item_args_converter(self, row_index, record):
        return {'text': record['name'],
                'size_hint_y': None,
                'color': [1, 0, 0, 1]
                              if record['name'] in self.search_results
                              else [1, 1, 1, .2],
                'height': 25}

    def criterion_entered(self, text_input):
        # text_input.id is set to be the form of:
        #
        #     ">: Protein"
        #
        # so, we can get the direction of the criterion comparison
        # from the first char. The property name is [3:].
        #
        direction = '<' if text_input.id[0] == '<' else '>'
        prop = text_input.id[3:]

        if text_input.text.isdigit():
            target_value = int(text_input.text)

            if not prop in self.search_criteria:
                self.search_criteria[prop] = {}

            self.search_criteria[prop][direction] = target_value
        else:
            if len(text_input.text.strip()) > 0:
                text_input.text = 'Fix me:' + text_input.text
            del self.search_criteria[prop][direction]

        self.search()

    def search(self):
        search_results = []
        for fruit in self.statechart.data:
            matches = True
            for prop in self.search_criteria:
                for direction in self.search_criteria[prop]:
                    target_value = self.search_criteria[prop][direction]
                    actual_value = self.statechart.data[fruit][prop]
                    if direction == '<':
                        if not actual_value >= target_value:
                            matches = False
                            break
                    else:
                        if not actual_value <= target_value:
                            matches = False
                            break
            if matches:
                search_results.append(fruit)

        self.search_results = list(set(search_results))

        # Force update of listview, which always contains all fruits, but
        # only the ones currently in self.search_results are highlighted.
        self.results_fruits_dict_adapter.sorted_keys = []
        self.results_fruits_dict_adapter.sorted_keys = self.all_fruits

    def exit_state(self, context=None):
        print 'ShowingSearchScreen/exit_state'

    def go_to_lists(self, *args):
        self.go_to_state('ShowingListsScreen')

    def go_to_data(self, *args):
        self.go_to_state('ShowingDataScreen')

    def go_to_detail(self, *args):
        self.go_to_state('ShowingDetailScreen')
