from kivy.app import App

from kivy.properties import DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.adapters.dictadapter import DictAdapter

from views.shape_bubble_button import ShapeBubbleButton

from graphics import PolygonVectorShape


data = \
    {'generic_shape_tool': {
         'tool': 'generic_shape_tool',
         'action': 'show_submenu_generic_shape_tool',
         'is_selected': False},
     'state_shape_tool': {
         'tool': 'state_shape_tool',
         'action': 'show_submenu_state_shape_tool',
         'is_selected': False}}


class ToolsAdapter(DictAdapter):

    tool = OptionProperty('state_shape_tool',
                          options=('generic_shape_tool',
                                   'state_shape_tool'))

    current_shape = ObjectProperty(None, allownone=True)

    adapters = DictProperty({})

    def __init__(self, **kwargs):

        app = App.get_running_app()

        self.adapters = {'generic_shape_tool': app.generic_shape_tools_adapter,
                         'state_shape_tool': app.state_shape_tools_adapter}

        kwargs['sorted_keys'] = ['generic_shape_tool',
                                 'state_shape_tool']
        kwargs['data'] = data
        kwargs['args_converter'] = self.args_converter
        kwargs['selection_mode'] = 'single'
        kwargs['allow_empty_selection'] = False
        kwargs['cls'] = ShapeBubbleButton

        super(ToolsAdapter, self).__init__(**kwargs)

        self.bind(on_selection_change=self.tool_changed)

        self.tool_changed(self)

    def args_converter(self, row_index, rec):

        adapter = self.adapters[rec['tool']]

        return {'size_hint': (None, None),
                'size': (60, 60),
                'shape': adapter.current_shape,
                'adapter': adapter,
                'action': rec['action']}

    def tool_changed(self, adapter, *args):

        self.tool = self.sorted_keys[self.selection[0].index]

        self.current_shape = self.get_view(self.selection[0].index).shape
