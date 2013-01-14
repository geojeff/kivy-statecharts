import re

from kivy.app import App

from kivy.adapters.dictadapter import DictAdapter

from kivy.uix.listview import ListItemButton

from kivy.properties import ObjectProperty

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

from kivy.uix.screenmanager import ScreenManager

from states.showing_lists import ShowingListsScreen
from states.showing_search import ShowingSearchScreen
from states.showing_data import ShowingDataScreen
from states.showing_detail import ShowingDetailScreen

from fixtures import fruit_categories
from fixtures import fruit_data


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState

        self.create_searchable_data()
        self.create_adapters()

        super(AppStatechart, self).__init__(**kwargs)

    @classmethod
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

    @classmethod
    def create_adapters(self):
        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['name'],
                                        'size_hint_y': None,
                                        'height': 25}

        categories = sorted(fruit_categories.keys())

        self.fruit_categories_dict_adapter = DictAdapter(
                sorted_keys=categories,
                data=fruit_categories,
                args_converter=list_item_args_converter,
                selection_mode='single',
                allow_empty_selection=False,
                cls=ListItemButton)

        fruits = fruit_categories[categories[0]]['fruits']

        self.fruits_dict_adapter = DictAdapter(
                sorted_keys=fruits,
                data=fruit_data,
                args_converter=list_item_args_converter,
                selection_mode='single',
                allow_empty_selection=False,
                cls=ListItemButton)

    # In this example, state classes are declared in their own files in states
    # package, e.g.  states/showing_lists/ShowingListsScreen. They are imported
    # above, so are available by their class names, e.g. ShowingListsScreen.
    #
    # They need to be declared here in RootState, in one of several ways. You
    # may prefer to use an __init__() method and kwargs as shown here, or you
    # may declare them in shorter fashion:
    #
    # class RootState(State):
    #     initial_substate_key = 'ShowingListsScreen'
    #
    #     ShowingListsScreen = ShowingListsScreen
    #     ShowingSearchScreen = ShowingSearchScreen
    #     ShowingDataScreen = ShowingDataScreen
    #     ShowingDetailScreen = ShowingDetailScreen
    #
    # Regardless of state declaration style, if we were to have more deeply
    # nested substates, we would declare them in the same fashion to build a
    # hierarchy.
    #
    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'ShowingListsScreen'

            kwargs['ShowingListsScreen'] = ShowingListsScreen
            kwargs['ShowingSearchScreen'] = ShowingSearchScreen
            kwargs['ShowingDataScreen'] = ShowingDataScreen
            kwargs['ShowingDetailScreen'] = ShowingDetailScreen

            super(AppStatechart.RootState, self).__init__(**kwargs)


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
