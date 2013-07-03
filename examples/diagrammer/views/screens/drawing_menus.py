from kivy.uix.bubble import Bubble

from kivy.lang import Builder


Builder.load_string('''
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
            adapter: app.tools_adapter

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
        adapter: app.generic_shape_tools_adapter

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
        adapter: app.state_shape_tools_adapter
''')

class DrawingMenu(Bubble):
    pass


class GenericShapeSubmenu(Bubble):
    pass


class StateShapeSubmenu(Bubble):
    pass


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
