import re

from kivy.app import App

from kivy.adapters.dictadapter import DictAdapter

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.uix.listview import ListItemLabel
from kivy.uix.listview import CompositeListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

# ----------------------------------------------------------------------------
# A dataset of fruit category and fruit data for use in examples.
#
# Data from http://www.fda.gov/Food/LabelingNutrition/\
#                FoodLabelingGuidanceRegulatoryInformation/\
#                InformationforRestaurantsRetailEstablishments/\
#                ucm063482.htm
#
# Available items for import are:
#
#     fruit_categories
#     fruit_data_attributes
#     fruit_data_attribute_units
#     fruit_data_list_of_dicts
#     fruit_data
#
fruit_categories = \
        {'Melons': {'name': 'Melons',
                    'fruits': ['Cantaloupe', 'Honeydew', 'Watermelon'],
                    'is_selected': False},
         'Tree Fruits': {'name': 'Tree Fruits',
                         'fruits': ['Apple', 'Avocado', 'Banana', 'Nectarine',
                                    'Peach', 'Pear', 'Pineapple', 'Plum',
                                    'Cherry'],
                         'is_selected': False},
         'Citrus Fruits': {'name': 'Citrus Fruits',
                           'fruits': ['Grapefruit', 'Lemon', 'Lime', 'Orange',
                                      'Tangerine'],
                           'is_selected': False},
         'Other Fruits': {'name': 'Other Fruits',
                          'fruits': ['Grape', 'Kiwifruit',
                                     'Strawberry'],
                          'is_selected': False}}

fruit_data_list_of_dicts = [
{'name':'Apple',
 'Serving Size': '1 large (242 g/8 oz)',
 'data': [130, 0, 0, 0, 0, 0, 260, 7, 34, 11, 5, 20, 25, 1, 2, 8, 2, 2],
 'is_selected': False},
{'name':'Avocado',
 'Serving Size': '1/5 medium (30 g/1.1 oz)',
 'data': [50, 35, 4.5, 7, 0, 0, 140, 4, 3, 1, 1, 4, 0, 1, 0, 4, 0, 2],
 'is_selected': False},
{'name':'Banana',
 'Serving Size': '1 medium (126 g/4.5 oz)',
 'data': [110, 0, 0, 0, 0, 0, 450, 13, 30, 10, 3, 12, 19, 1, 2, 15, 0, 2],
 'is_selected': False},
{'name':'Cantaloupe',
 'Serving Size': '1/4 medium (134 g/4.8 oz)',
 'data': [50, 0, 0, 0, 20, 1, 240, 7, 12, 4, 1, 4, 11, 1, 120, 80, 2, 2],
 'is_selected': False},
{'name':'Grapefruit',
 'Serving Size': '1/2 medium (154 g/5.5 oz)',
 'data': [60, 0, 0, 0, 0, 0, 160, 5, 15, 5, 2, 8, 11, 1, 35, 100, 4, 0],
 'is_selected': False},
{'name':'Grape',
 'Serving Size': '3/4 cup (126 g/4.5 oz)',
 'data': [90, 0, 0, 0, 15, 1, 240, 7, 23, 8, 1, 4, 20, 0, 0, 2, 2, 0],
 'is_selected': False},
{'name':'Honeydew',
 'Serving Size': '1/10 medium melon (134 g/4.8 oz)',
 'data': [50, 0, 0, 0, 30, 1, 210, 6, 12, 4, 1, 4, 11, 1, 2, 45, 2, 2],
 'is_selected': False},
{'name':'Kiwifruit',
 'Serving Size': '2 medium (148 g/5.3 oz)',
 'data': [90, 10, 1, 2, 0, 0, 450, 13, 20, 7, 4, 16, 13, 1, 2, 240, 4, 2],
 'is_selected': False},
{'name':'Lemon',
 'Serving Size': '1 medium (58 g/2.1 oz)',
 'data': [15, 0, 0, 0, 0, 0, 75, 2, 5, 2, 2, 8, 2, 0, 0, 40, 2, 0],
 'is_selected': False},
{'name':'Lime',
 'Serving Size': '1 medium (67 g/2.4 oz)',
 'data': [20, 0, 0, 0, 0, 0, 75, 2, 7, 2, 2, 8, 0, 0, 0, 35, 0, 0],
 'is_selected': False},
{'name':'Nectarine',
 'Serving Size': '1 medium (140 g/5.0 oz)',
 'data': [60, 5, 0.5, 1, 0, 0, 250, 7, 15, 5, 2, 8, 11, 1, 8, 15, 0, 2],
 'is_selected': False},
{'name':'Orange',
 'Serving Size': '1 medium (154 g/5.5 oz)',
 'data': [80, 0, 0, 0, 0, 0, 250, 7, 19, 6, 3, 12, 14, 1, 2, 130, 6, 0],
 'is_selected': False},
{'name':'Peach',
 'Serving Size': '1 medium (147 g/5.3 oz)',
 'data': [60, 0, 0.5, 1, 0, 0, 230, 7, 15, 5, 2, 8, 13, 1, 6, 15, 0, 2],
 'is_selected': False},
{'name':'Pear',
 'Serving Size': '1 medium (166 g/5.9 oz)',
 'data': [100, 0, 0, 0, 0, 0, 190, 5, 26, 9, 6, 24, 16, 1, 0, 10, 2, 0],
 'is_selected': False},
{'name':'Pineapple',
 'Serving Size': '2 slices, 3" diameter, 3/4" thick (112 g/4 oz)',
 'data': [50, 0, 0, 0, 10, 0, 120, 3, 13, 4, 1, 4, 10, 1, 2, 50, 2, 2],
 'is_selected': False},
{'name':'Plum',
 'Serving Size': '2 medium (151 g/5.4 oz)',
 'data': [70, 0, 0, 0, 0, 0, 230, 7, 19, 6, 2, 8, 16, 1, 8, 10, 0, 2],
 'is_selected': False},
{'name':'Strawberry',
 'Serving Size': '8 medium (147 g/5.3 oz)',
 'data': [50, 0, 0, 0, 0, 0, 170, 5, 11, 4, 2, 8, 8, 1, 0, 160, 2, 2],
 'is_selected': False},
{'name':'Cherry',
 'Serving Size': '21 cherries; 1 cup (140 g/5.0 oz)',
 'data': [100, 0, 0, 0, 0, 0, 350, 10, 26, 9, 1, 4, 16, 1, 2, 15, 2, 2],
 'is_selected': False},
{'name':'Tangerine',
 'Serving Size': '1 medium (109 g/3.9 oz)',
 'data': [50, 0, 0, 0, 0, 0, 160, 5, 13, 4, 2, 8, 9, 1, 6, 45, 4, 0],
 'is_selected': False},
{'name':'Watermelon',
 'Serving Size': '1/18 medium melon; 2 cups diced pieces (280 g/10.0 oz)',
 'data': [80, 0, 0, 0, 0, 0, 270, 8, 21, 7, 1, 4, 20, 1, 30, 25, 2, 4],
 'is_selected': False}]

fruit_data_attributes = ['(gram weight/ ounce weight)',
                         'Calories',
                         'Calories from Fat',
                         'Total Fat',
                         'Sodium',
                         'Potassium',
                         'Total Carbo-hydrate',
                         'Dietary Fiber',
                         'Sugars',
                         'Protein',
                         'Vitamin A',
                         'Vitamin C',
                         'Calcium',
                         'Iron']

fruit_data_attribute_units = ['(g)',
                              '(%DV)',
                              '(mg)',
                              '(%DV)',
                              '(mg)',
                              '(%DV)',
                              '(g)',
                              '(%DV)',
                              '(g)(%DV)',
                              '(g)',
                              '(g)',
                              '(%DV)',
                              '(%DV)',
                              '(%DV)',
                              '(%DV)']

attributes_and_units = dict(zip(fruit_data_attributes,
                                fruit_data_attribute_units))

fruit_data = {}
for fruit_record in fruit_data_list_of_dicts:
    fruit_data[fruit_record['name']] = {}
    fruit_data[fruit_record['name']] = \
            dict({'name': fruit_record['name'],
                  'Serving Size': fruit_record['Serving Size'],
                  'is_selected': fruit_record['is_selected']},
            **dict(zip(attributes_and_units.keys(), fruit_record['data'])))


class FruitDetailView(GridLayout):
    fruit_name = StringProperty('', allownone=True)

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        self.fruit_name = kwargs.get('fruit_name', '')
        super(FruitDetailView, self).__init__(**kwargs)
        if self.fruit_name:
            self.redraw()

    def redraw(self, *args):
        self.clear_widgets()
        if self.fruit_name:
            self.add_widget(Label(text="Name:", halign='right'))
            self.add_widget(Label(text=self.fruit_name))
            for attribute in fruit_data_attributes:
                self.add_widget(Label(text="{0}:".format(attribute),
                                      halign='right'))
                self.add_widget(
                    Label(text=str(fruit_data[self.fruit_name][attribute])))


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kw):
        self.trace = True
        self.root_state_class = self.RootState

        self.categories = sorted(fruit_categories.keys())

        self.create_searchable_data()

        self.create_adapters()

        super(AppStatechart, self).__init__(**kw)

    def create_searchable_data(self):
        properties = ['Calories', 'Calories from Fat', 'Total Fat',
                      'Sodium', 'Potassium', 'Total Carbo-hydrate',
                      'Dietary Fiber', 'Sugars', 'Protein',
                      'Vitamin A', 'Vitamin C', 'Calcium', 'Iron']

        self.data = {}
        for fruit in fruit_data:
            g_oz_str = re.search('\((.*?)\)',
                                    fruit_data[fruit]['Serving Size'])
            g_oz_str = g_oz_str.group()[1:-1]
            g_str, oz_str = \
                [s.split()[0] for s in g_oz_str.split('/')]

            self.data[fruit] = {}
            self.data[fruit]['name'] = fruit
            self.data[fruit]['Serving Size, g'] = int(g_str)
            self.data[fruit]['Serving Size, oz'] = int(float(oz_str))

            for prop in properties:
                self.data[fruit][prop] = fruit_data[fruit][prop]

    def create_adapters(self):
        self.list_item_args_converter = \
                lambda row_index, rec: {'text': rec['name'],
                                        'size_hint_y': None,
                                        'height': 25}

        self.fruit_categories_dict_adapter = DictAdapter(
                sorted_keys=self.categories,
                data=fruit_categories,
                args_converter=self.list_item_args_converter,
                selection_mode='single',
                allow_empty_selection=False,
                cls=ListItemButton)

        fruits = fruit_categories[self.categories[0]]['fruits']

        self.fruits_dict_adapter = DictAdapter(
                sorted_keys=fruits,
                data=fruit_data,
                args_converter=self.list_item_args_converter,
                selection_mode='single',
                allow_empty_selection=False,
                cls=ListItemButton)

    class RootState(State):
        initial_substate_key = 'ShowingListsScreen'

        class ShowingListsScreen(State):
            '''Implementation of a cascading style display, with a scrollable
            list of fruit categories on the left, a list of fruits for the
            selected category in the middle, and a fruit detail view on the
            right.
            '''

            def enter_state(self, context=None):
                print 'ShowingListsScreen/enter_state'

                if not 'Lists' in self.statechart.app.sm.screen_names:

                    # Convenience references:
                    self.app = self.statechart.app

                    view = BoxLayout(orientation='vertical', spacing=10)

                    toolbar = BoxLayout(size_hint=(1.0, None), height=50)

                    label = Label(text='Lists', color=[.8, .8, .8, .8], bold=True)
                    toolbar.add_widget(label)

                    button = Button(text='Search')
                    button.bind(on_press=self.go_to_search)
                    toolbar.add_widget(button)

                    button = Button(text='Data')
                    button.bind(on_press=self.go_to_data)
                    toolbar.add_widget(button)

                    button = Button(text='Detail')
                    button.bind(on_press=self.go_to_detail)
                    toolbar.add_widget(button)

                    view.add_widget(toolbar)

                    lists_view = GridLayout(cols=3, size_hint=(1.0, 1.0))

                    lists_view.add_widget(ListView(
                        adapter=self.statechart.fruit_categories_dict_adapter,
                        size_hint=(.2, 1.0)))

                    lists_view.add_widget(ListView(
                        adapter=self.statechart.fruits_dict_adapter,
                        size_hint=(.2, 1.0)))

                    self.detail_view = \
                            FruitDetailView(fruit_name=self.statechart.fruits_dict_adapter.selection[0].text,
                                            size_hint=(.6, 1.0))

                    lists_view.add_widget(self.detail_view)

                    view.add_widget(lists_view)

                    self.create_adapter_bindings()

                    screen = Screen(name='Lists')
                    screen.add_widget(view)
                    self.app.sm.add_widget(screen)

                if self.app.sm.current != 'Lists':
                    self.app.sm.current = 'Lists'

            def exit_state(self, context=None):
                print 'ShowingListsScreen/exit_state'

            def create_adapter_bindings(self):
                # Create bindings from selection in adapters to
                # action callback functions here:
                self.statechart.fruit_categories_dict_adapter.bind(
                        on_selection_change=self.fruit_category_changed)

                self.statechart.fruits_dict_adapter.bind(
                        on_selection_change=self.fruit_changed)

            def fruit_category_changed(self, fruit_categories_adapter, *args):
                if len(fruit_categories_adapter.selection) == 0:
                    self.statechart.fruits_dict_adapter.data = {}
                    return

                key = str(fruit_categories_adapter.selection[0])
                category = fruit_categories[key]
                self.statechart.fruits_dict_adapter.sorted_keys = category['fruits']

            def fruit_changed(self, list_adapter, *args):
                if len(list_adapter.selection) == 0:
                    self.detail_view.fruit_name = None
                else:
                    selected_object = list_adapter.selection[0]

                    if type(selected_object) is str:
                        self.detail_view.fruit_name = selected_object
                    else:
                        self.detail_view.fruit_name = str(selected_object)

                    self.detail_view.redraw()

            def go_to_search(self, *args):
                self.go_to_state('ShowingSearchScreen')

            def go_to_data(self, *args):
                self.go_to_state('ShowingDataScreen')

            def go_to_detail(self, *args):
                self.go_to_state('ShowingDetailScreen')

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

                    body_view = BoxLayout() #size_hint=(1.0, None), height=0.8)

                    left_view = BoxLayout(size_hint=(0.7, 1.0), orientation='vertical')

                    left_view.add_widget(Label(size_hint=(1.0, 0.2), text="""[b]Search Criteria:[/b]

    Enter the lower and upper bounds of search criteria in the text
    entry boxes. Each time you hit the [i]ENTER[/i] key in a text entry box,
    the search results shown in the list on the right will be updated.""", markup=True))

                    search_criteria_view = BoxLayout(orientation='vertical')

                    props = [prop for prop in self.statechart.data['Apple'] if prop != 'name']

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

                    right_view = BoxLayout(size_hint=(0.3, 1.0), orientation='vertical')

                    right_view.add_widget(Label(size_hint=(1.0, 0.2), text="Search Results (red):"))

                    self.all_fruits = sorted(self.statechart.data.keys())

                    self.results_fruits_dict_adapter = DictAdapter(
                        sorted_keys=self.all_fruits,
                        data=self.statechart.data,
                        args_converter=self.list_item_args_converter,
                        selection_mode='none',
                        allow_empty_selection=True,
                        cls=ListItemLabel)

                    right_view.add_widget(ListView(size_hint=(1.0, 0.8),
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
                        'color': [1,0,0,1] if record['name'] in self.search_results else [1,1,1,.2],
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
                            if direction == '<':
                                if not self.statechart.data[fruit][prop] >= target_value:
                                    matches = False
                                    break
                            else:
                                if not self.statechart.data[fruit][prop] <= target_value:
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

        class ShowingDataScreen(State):

            def enter_state(self, context=None):
                print 'ShowingDataScreen/enter_state'

                if not 'Data' in self.statechart.app.sm.screen_names:

                    self.app = self.statechart.app

                    view = BoxLayout(orientation='vertical', spacing=10)

                    toolbar = BoxLayout(size_hint=(1.0, None), height=50)

                    button = Button(text='Lists')
                    button.bind(on_press=self.go_to_lists)
                    toolbar.add_widget(button)

                    button = Button(text='Search')
                    button.bind(on_press=self.go_to_search)
                    toolbar.add_widget(button)

                    label = Label(text='Data', color=[.8, .8, .8, .8], bold=True)
                    toolbar.add_widget(label)

                    button = Button(text='Detail')
                    button.bind(on_press=self.go_to_detail)
                    toolbar.add_widget(button)

                    view.add_widget(toolbar)

                    props = [prop for prop in self.statechart.data['Apple'] if prop != 'name']

                    sorted_fruits = sorted(self.statechart.data.keys())
                    data = {'Fruits': {'prop': 'Fruits', 'values': sorted_fruits}}
                    for prop in sorted(props):
                        data[prop] = \
                            dict({'prop': prop,
                                  'values': [self.statechart.data[fruit][prop] for fruit in sorted_fruits]})
                    props = sorted(props)
                    props.insert(0, 'Fruits')

                    args_converter = \
                        lambda row_index, rec: \
                            {'size_hint': (None, None),
                             'height': 75,
                             'cls_dicts': [{'cls': ListItemLabel,
                                            'kwargs': {'halign': 'left',
                                                       'size_hint': (None, None),
                                                       'width': 200,
                                                       'text_size': (200, None),
                                                       'text': str(rec['prop'])}},
                                           {'cls': ListItemLabel,
                                            'kwargs': {'halign': 'right',
                                                       'size_hint': (None, None),
                                                       'text_size': (500, None),
                                                       'width': 500,
                                                       'text': str(rec['values'])}}]}

                    dict_adapter = DictAdapter(sorted_keys=props,
                                               data=data,
                                               args_converter=args_converter,
                                               selection_mode='none',
                                               allow_empty_selection=True,
                                               cls=CompositeListItem)

                    view.add_widget(ListView(adapter=dict_adapter))

                    screen = Screen(name='Data')
                    screen.add_widget(view)

                    self.app.sm.add_widget(screen)

                if self.app.sm.current != 'Data':
                    self.app.sm.current = 'Data'

            def exit_state(self, context=None):
                print 'ShowingDataScreen/exit_state'

            def go_to_lists(self, *args):
                self.go_to_state('ShowingListsScreen')

            def go_to_search(self, *args):
                self.go_to_state('ShowingSearchScreen')

            def go_to_detail(self, *args):
                self.go_to_state('ShowingDetailScreen')

        class ShowingDetailScreen(State):

            def enter_state(self, context=None):
                print 'ShowingDetailScreen/enter_state'

                if not 'Detail' in self.statechart.app.sm.screen_names:

                    self.app = self.statechart.app

                    view = BoxLayout(orientation='vertical', spacing=10)

                    toolbar = BoxLayout(size_hint=(1.0, None), height=50)

                    button = Button(text='Lists')
                    button.bind(on_press=self.go_to_lists)
                    toolbar.add_widget(button)

                    button = Button(text='Search')
                    button.bind(on_press=self.go_to_search)
                    toolbar.add_widget(button)

                    button = Button(text='Data')
                    button.bind(on_press=self.go_to_data)
                    toolbar.add_widget(button)

                    label = Label(text='Detail', color=[.8, .8, .8, .8], bold=True)
                    toolbar.add_widget(label)

                    view.add_widget(toolbar)

                    self.detail_view = FruitDetailView(
                            fruit_name=self.statechart.fruits_dict_adapter.selection[0].text,
                            size_hint=(.6, 1.0))

                    view.add_widget(self.detail_view)

                    screen = Screen(name='Detail')
                    screen.add_widget(view)

                    self.app.sm.add_widget(screen)

                if self.app.sm.current != 'Detail':
                    self.detail_view.fruit_name = self.statechart.fruits_dict_adapter.selection[0].text
                    self.detail_view.redraw()
                    self.app.sm.current = 'Detail'

            def exit_state(self, context=None):
                print 'ShowingDetailScreen/exit_state'

            def go_to_lists(self, *args):
                self.go_to_state('ShowingListsScreen')

            def go_to_search(self, *args):
                self.go_to_state('ShowingSearchScreen')

            def go_to_data(self, *args):
                self.go_to_state('ShowingDataScreen')


class FruitsApp(App):
    statechart = ObjectProperty(None)
    sm = ObjectProperty(None)

    def build(self):

        self.sm = ScreenManager()
        return self.sm

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.init_statechart()


if __name__ in ('__android__', '__main__'):
    FruitsApp().run()
