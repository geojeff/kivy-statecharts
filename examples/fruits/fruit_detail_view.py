from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.properties import StringProperty

from fixtures import fruit_data_attributes
from fixtures import fruit_data


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
