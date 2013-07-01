from kivy.properties import OptionProperty
from kivy.adapters.dictadapter import DictAdapter

from views.polygon_bubble_button import PolygonBubbleButton

from graphics import PolygonVectorShape


data = \
    {'state_triangle': {
         'mode': 'state_triangle',
         'radius': 20,
         'sides': 3,
         'is_selected': False},
     'state_rectangle': {
         'mode': 'state_rectangle',
         'radius': 20,
         'sides': 4,
         'is_selected': False},
     'state_pentagon': {
         'mode': 'state_pentagon',
         'radius': 20,
         'sides': 5,
         'is_selected': False}}

args_converter = lambda row_index, rec: {'value': rec['mode'],
                                         'size_hint': (None, None),
                                         'size': (60, 60),
                                         'shape_cls': PolygonVectorShape,
                                         'radius': rec['radius'],
                                         'sides': rec['sides'],
                                         'action': 'state_drawing_mode_changed'}


class StateDrawingModeAdapter(DictAdapter):

    # This is like an object controller.
    mode = OptionProperty('state_triangle',
                          options=('state_triangle',
                                   'state_rectangle',
                                   'state_pentagon'))

    def __init__(self, **kwargs):

        kwargs['sorted_keys'] = data.keys()
        kwargs['data'] = data
        kwargs['args_converter'] = args_converter
        kwargs['selection_mode'] = 'single'
        kwargs['allow_empty_selection'] = False,
        kwargs['cls'] = PolygonBubbleButton

        super(StateDrawingModeAdapter, self).__init__(**kwargs)

        self.bind(on_selection_change=self.state_drawing_mode_changed)

    def state_drawing_mode_changed(self, adapter, *args):
        if len(adapter.selection) == 0:
            self.data = {}
            return

        self.mode = adapter.selection[0].value
        print 'mode changed', self.mode
