from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.bubble import Bubble
from kivy.uix.listview import SelectableView

from views.graphics.shapes import PolygonVectorShape
from views.buttons.shape_bubble_button import ShapeBubbleButton


class ShapeToolButton(ShapeBubbleButton):

    index = NumericProperty(0)
    data_item = ObjectProperty(None)

    def __init__(self, **kwargs):
        if 'item_args' in kwargs:
            kwargs['index'] = kwargs['item_args']['index']
            kwargs['data_item'] = kwargs['item_args']['data_item']
            kwargs['shape'] = kwargs['data_item'].shape
            kwargs['action'] = kwargs['data_item'].action
        super(ShapeToolButton, self).__init__(**kwargs)
        print self.shape.fill_color

    def args_converter(self, index, data_item):
        print 'ARGS_CONVERTER', data_item.shape, data_item.action
        return {'shape': data_item.shape,
                'action': data_item.action}

Builder.load_string('''
#:import ShapeBubbleButton views.buttons.shape_bubble_button.ShapeBubbleButton

#<ShapeToolButton@ShapeBubbleButton>:
<ShapeToolButton>:
    size_hint: None, None
    size: 60, 60
#    args_converter: lambda index, data_item: {'shape': data_item.shape, 'action': data_item.action}

<DrawingMenu>
    size_hint: None, None
    size: 70, 200
    pos_hint: {"center_y": 0.5}
    padding: 5
    background_color: .2, .9, 1, .7
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    orientation: 'vertical'

    BoxLayout:
        padding: 5
        orientation: 'vertical'

        ListView:
            list_item_class: 'ShapeToolButton'
            DataBinding:
                source: app.shape_tools_controller

<GenericShapeSubmenu>:
    # TODO: size is hard-coded.
    size_hint: None, None
    size: (60, 60 * 3 + 12)
    pos_hint: {'center_x': .5, 'y': .6}
    #background_color: .2, .9, 1, .7
    background_color: .1, .2, .4, 1
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    ListView:
        list_item_class: 'ShapeToolButton'
        DataBinding:
            source: app.generic_shape_tools_controller

<StateShapeSubmenu>:
    # TODO: size is hard-coded.
    size_hint: None, None
    size: (60, 60 * 3 + 12)
    pos_hint: {'center_x': .5, 'y': .6}
    #background_color: .2, .9, 1, .7
    background_color: .1, .2, .4, 1
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    ListView:
        list_item_class: 'ShapeToolButton'
        DataBinding:
            source: app.state_shape_tools_controller
''')


class DrawingMenu(SelectableView, Bubble):

    def args_converter(self, row_index, data_item):
        app = App.app()
        return {'size_hint': (None, None),
                'size': (60, 60),
                'shape': app.current_tool_controller.data,
                'action': data_item.action}


class GenericShapeSubmenu(SelectableView, Bubble):

    def args_converter(self, row_index, data_item):
        app = App.app()
        return {'size_hint': (None, None),
                'size': (60, 60),
                'shape': app.current_generic_shape_tool_controller.data,
                'action': 'generic_shape_tool_changed'}


class StateShapeSubmenu(SelectableView, Bubble):

    def args_converter(self, row_index, data_item):
        app = App.app()
        return {'size_hint': (None, None),
                'size': (60, 60),
                'shape': app.current_state_shape_tool_controller.data,
                'action': 'state_shape_tool_changed'}


# TODO: other menus:
#
#        action: 'set_tool_select_pick'
#        action: 'set_tool_select_marquee'
#        action: 'set_tool_select_node'

#        action: 'set_tool_text_large'
#        action: 'set_tool_text_medium'
#        action: 'set_tool_text_small'

#        action: 'set_tool_line_straight'
#        action: 'set_tool_line_arc'
#        action: 'set_tool_line_bezier'
