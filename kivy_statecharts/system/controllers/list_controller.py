from kivy.properties import OpObservableList
from kivy.properties import ListProperty

from kivy_statecharts.system.controllers.controller import Controller
from kivy_statecharts.system.controllers.list_ops import \
        ControllerListOpHandler
from kivy_statecharts.system.controllers.selection import ObjectSelection


class ListController(Controller, ObjectSelection):

    content = ListProperty([], cls=OpObservableList)

    __events__ = ('on_data_change', )

    def __init__(self, **kwargs):

        super(ListController, self).__init__(**kwargs)

        self.list_op_handler = \
                ControllerListOpHandler(source_list=self.content,
                                        duplicates_allowed=True)

        self.bind(content=self.list_op_handler.data_changed)

    def on_data_change(self, *args):
        '''on_data_change() is the default handler for the
        on_data_change event.
        '''
        pass

    def update(self, *args):
        # args:
        #
        #     controller args[0]
        #     value      args[1]
        #     op_info    args[2]

        value = args[1]

        if isinstance(value, list):
            self.content = value
        else:
            if value:
                self.content = [value]

    # TODO: examples of filtering and alias properties. There can
    # also be an order_by or other aid for sorting.
