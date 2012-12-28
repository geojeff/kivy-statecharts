from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen

from fruit_detail_view import FruitDetailView

from fixtures import fruit_categories


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

            selected_fruit = \
                    self.statechart.fruits_dict_adapter.selection[0].text
            self.detail_view = FruitDetailView(fruit_name=selected_fruit,
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
