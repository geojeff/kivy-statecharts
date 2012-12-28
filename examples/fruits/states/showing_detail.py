from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State

from fruit_detail_view import FruitDetailView


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

            selected_fruit = \
                    self.statechart.fruits_dict_adapter.selection[0].text
            self.detail_view = FruitDetailView(
                    fruit_name=selected_fruit,
                    size_hint=(.6, 1.0))

            view.add_widget(self.detail_view)

            screen = Screen(name='Detail')
            screen.add_widget(view)

            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'Detail':
            self.detail_view.fruit_name = \
                    self.statechart.fruits_dict_adapter.selection[0].text
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
