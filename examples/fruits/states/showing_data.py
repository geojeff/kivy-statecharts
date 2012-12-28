from kivy.adapters.dictadapter import DictAdapter

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemLabel
from kivy.uix.listview import CompositeListItem

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen


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

            props = [prop for prop in self.statechart.data['Apple']
                         if prop != 'name']

            sorted_fruits = sorted(self.statechart.data.keys())
            data = {'Fruits': {'prop': 'Fruits', 'values': sorted_fruits}}
            for prop in sorted(props):
                data[prop] = \
                    dict({'prop': prop,
                          'values': [self.statechart.data[fruit][prop]
                                         for fruit in sorted_fruits]})
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
