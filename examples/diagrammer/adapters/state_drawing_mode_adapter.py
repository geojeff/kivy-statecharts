from kivy.adapters.dictadapter import DictAdapter

from views.shape_bubble_button import ShapeBubbleButton

from graphics import PolygonVectorShape

#try:
#    triangle_vector_shape = PolygonVectorShape(sides=3)
#except KeyError:
#    import sys, pdb
#    pdb.post_mortem(sys.exc_info()[2])

triangle_vector_shape = PolygonVectorShape(sides=3)
rectangle_vector_shape = PolygonVectorShape(sides=4)
pentagon_vector_shape = PolygonVectorShape(sides=5)


data = \
    {'drawing_mode_state_triangle': {
         'name': 'drawing_mode_state_triangle',
         'radius': 30,
         'sides': 3,
         'shape': triangle_vector_shape,
         'action': 'set_drawing_mode_state_triangle',
         'is_selected': False},
     'drawing_mode_state_rectangle': {
         'name': 'drawing_mode_state_rectangle',
         'radius': 30,
         'sides': 4,
         'shape': rectangle_vector_shape,
         'action': 'set_drawing_mode_state_rectangle',
         'is_selected': False},
     'drawing_mode_state_pentagon': {
         'name': 'drawing_mode_state_pentagon',
         'radius': 30,
         'sides': 5,
         'shape': pentagon_vector_shape,
         'action': 'set_drawing_mode_state_pentagon',
         'is_selected': False}}

args_converter = lambda row_index, rec: {'name': rec['name'],
                                         'radius': rec['radius'],
                                         'sides': rec['sides'],
                                         'action': rec['action']}


class StateDrawingModeAdapter(DictAdapter):

    def __init__(self, **kwargs):

        kwargs['sorted_keys'] = data.keys()
        kwargs['data'] = data
        kwargs['args_converter'] = args_converter
        kwargs['selection_mode'] = 'single'
        kwargs['allow_empty_selection'] = False,
        kwargs['cls'] = ShapeBubbleButton

        super(StateDrawingModeAdapter, self).__init__(**kwargs)

    def state_drawing_mode_changed(self, adapter, *args):
        if len(adapter.selection) == 0:
            self.data = {}
            return

        self.mode = self.data[adapter.selection[0].text]

        #self.sorted_keys = category['fruits']
