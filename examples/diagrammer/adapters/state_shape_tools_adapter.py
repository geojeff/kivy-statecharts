from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.adapters.dictadapter import DictAdapter

from views.buttons.shape_bubble_button import ShapeBubbleButton

from views.graphics.shapes import PolygonVectorShape


data = \
    {'state_shape_triangle': {
         'tool': 'state_shape_triangle',
         'radius': 20,
         'sides': 3,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False},
     'state_shape_rectangle': {
         'tool': 'state_shape_rectangle',
         'radius': 20,
         'sides': 4,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False},
     'state_shape_pentagon': {
         'tool': 'state_shape_pentagon',
         'radius': 20,
         'sides': 5,
         'stroke_width': 1.0,
         'stroke_color': [.2, .9, .2, .8],
         'fill_color': [.4, .4, .4, 1],
         'is_selected': False}}

# TODO: A generic shape adapter can have a shape_cls key to whatever shape
#       class is to be used. This one specifically uses PolygonVectorShape.

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
                     'action': 'state_shape_tool_changed'}


class StateShapeToolsAdapter(DictAdapter):

    # This is like an object controller.
    tool = OptionProperty('state_shape_triangle',
                          options=('state_shape_triangle',
                                   'state_shape_rectangle',
                                   'state_shape_pentagon'))

    current_shape = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):

        kwargs['sorted_keys'] = ['state_shape_triangle',
                                 'state_shape_rectangle',
                                 'state_shape_pentagon']
        kwargs['data'] = data
        kwargs['args_converter'] = args_converter
        kwargs['selection_mode'] = 'single'
        kwargs['allow_empty_selection'] = False
        kwargs['cls'] = ShapeBubbleButton

        super(StateShapeToolsAdapter, self).__init__(**kwargs)

        self.bind(on_selection_change=self.state_shape_tool_changed)

        # TODO (IMPORTANT): Adapters should dispatch on initial selection?
        self.state_shape_tool_changed(self)

    def state_shape_tool_changed(self, adapter, *args):

        self.tool = self.sorted_keys[self.selection[0].index]

        self.current_shape = self.get_view(self.selection[0].index).shape
