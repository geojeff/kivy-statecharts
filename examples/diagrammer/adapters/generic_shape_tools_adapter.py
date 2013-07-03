from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.adapters.dictadapter import DictAdapter

from views.buttons.shape_bubble_button import ShapeBubbleButton

from graphics import PolygonVectorShape


data = \
    {'generic_shape_triangle': {
         'tool': 'generic_shape_triangle',
         'radius': 20,
         'sides': 3,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False},
     'generic_shape_rectangle': {
         'tool': 'generic_shape_rectangle',
         'radius': 20,
         'sides': 4,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False},
     'generic_shape_pentagon': {
         'tool': 'generic_shape_pentagon',
         'radius': 20,
         'sides': 5,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False}}

args_converter = lambda row_index, rec: {
                     'size_hint': (None, None),
                     'size': (60, 60),
                     'shape': PolygonVectorShape(
                                  radius=rec['radius'],
                                  sides=rec['sides'],
                                  stroke_width=rec['stroke_width'],
                                  stroke_color=rec['stroke_color'],
                                  fill_color=rec['fill_color']),
                     'adapter': None,
                     'action': 'generic_shape_tool_changed'}


class GenericShapeToolsAdapter(DictAdapter):

    # This is like an object controller.
    tool = OptionProperty('generic_shape_triangle',
                          options=('generic_shape_triangle',
                                   'generic_shape_rectangle',
                                   'generic_shape_pentagon'))

    current_shape = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):

        kwargs['sorted_keys'] = ['generic_shape_triangle',
                                 'generic_shape_rectangle',
                                 'generic_shape_pentagon']
        kwargs['data'] = data
        kwargs['args_converter'] = args_converter
        kwargs['selection_mode'] = 'single'
        kwargs['allow_empty_selection'] = False
        kwargs['cls'] = ShapeBubbleButton

        super(GenericShapeToolsAdapter, self).__init__(**kwargs)

        self.bind(on_selection_change=self.generic_shape_tool_changed)

        self.generic_shape_tool_changed(self)

    def generic_shape_tool_changed(self, adapter, *args):

        self.tool = self.sorted_keys[self.selection[0].index]

        self.current_shape = self.get_view(self.selection[0].index).shape
