from kivy_statecharts.system.state import State

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.animation import Animation

from kivy.graphics import Color

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.uix.bubble import Bubble

from state_graphics import StateTriangleLVS
from state_graphics import StateRectangleLVS
from state_graphics import StatePentagonLVS

from kivy.lang import Builder


Builder.load_string('''
[EditingShapeMenuButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'editing_shape_menu_root'
    on_release: app.statechart.send_event('show_editing_shape_submenu', self, None)
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    text: ctx.text
    Image:
        source: 'atlas://data/images/defaulttheme/tree_closed'
        size: (20, 20)
        y: self.parent.y + (self.parent.height/2) - (self.height/2)
        x: self.parent.x + (self.parent.width - self.width)

<EditingShapeMenu>
    size_hint: None, None
    size: 340, 260
    pos: (5, 50)
    padding: 5
    background_color: .2, .9, 1, .7
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    orientation: 'vertical'
    BoxLayout:
        padding: 5
        ScrollView:
            BoxLayout:
                size_hint: None, 1
                width: root.width * 2 - 40

                BoxLayout:
                    orientation: 'vertical'
                    EditingShapeMenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Label'
                    EditingShapeMenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Fill'
                    EditingShapeMenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Stroke'
                    EditingShapeMenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Scale'
                    EditingShapeMenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Connect'

[AnchorButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'anchor_buttons'
    on_release: app.statechart.send_event('shape_label_anchor_changed', self.text, None)
    size_hint: None, None
    size: 40, 40
    text: ctx.text

<Selector>:
    grid: _grid
    orientation: 'vertical'
    BoxLayout:
        padding: [5, 5, 5, 5]
        spacing: 5
        size_hint_y: None
        height: 30
        Label:
            text: 'Label:'
            size_hint: None, None
            size: 50, 30
        TextInput:
            size_hint_y: None
            height: 30
            multiline: False
            font_size: 16
            text: app.current_shape.label_text
            on_text_validate: app.statechart.send_event('shape_label_edited', self.text)
    BoxLayout:
        GridLayout:
            id: _grid
            rows: 3
            cols: 3
            spacing: 10
            padding: 10
            size_hint_y: None
            height: 150
            AnchorButton:
                text: 'NW'
            AnchorButton:
                text: 'N'
            AnchorButton:
                text: 'NE'
            AnchorButton:
                text: 'W'
            AnchorButton:
                text: 'C'
            AnchorButton:
                text: 'E'
            AnchorButton:
                text: 'SW'
            AnchorButton:
                text: 'S'
            AnchorButton:
                text: 'SE'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Label Layout X'
            Slider:
                value: app.current_shape.label_anchor_layout_x
                on_value: app.current_shape.label_anchor_layout_x = float(args[1])
                min: 0.5
                max: 2.
            Label:
                text: 'Label Layout Y'
            Slider:
                value: app.current_shape.label_anchor_layout_y
                on_value: app.current_shape.label_anchor_layout_y = float(args[1])
                min: 0.5
                max: 2.
    BoxLayout:
        padding: [5, 5, 5, 5]
        spacing: 5
        size_hint_y: None
        height: 30
        Label:
            text: 'halign:'
            size_hint: None, None
            size: (50, 30)
        Spinner:
            text: app.current_shape.label_halign
            values: 'left', 'center', 'right'
            size_hint: None, None
            size: (50, 30)
            on_text: app.statechart.send_event('shape_label_halign_edited', self.text)
        Label:
            text: 'valign:'
            size_hint: None, None
            size: (50, 30)
        Spinner:
            text: app.current_shape.label_valign
            values: 'top', 'middle', 'bottom'
            size_hint: None, None
            size: (60, 30)
            on_text: app.statechart.send_event('shape_label_valign_edited', self.text)

<EditingShapeSubmenu>:
    selector: selector
    Button:
        text: '<'
        size_hint_x: None
        width: 25
        on_release: app.statechart.send_event('hide_editing_shape_submenu', self, 'state')
    Selector:
        id: selector
        pos: self.pos
        size: self.size
''')


class EditingShapeSubmenu(BoxLayout):
    statechart = ObjectProperty(None)


class EditingShapeMenu(Bubble):
    pass


class BoundedLabel(Label):
    pass


class Selector(BoxLayout):
    grid = ObjectProperty(None)


class EditingShape(State):
    '''
    '''

    edit_panel = ObjectProperty(None)

    shape = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EditingShape, self).__init__(**kwargs)

    def enter_state(self, context=None):

        ess = EditingShapeSubmenu(statechart=self.statechart)

        self.selector = ess.selector

        self.menus_and_submenus = {
                'label': ess,
                'fill': None,
                'stroke': None,
                'scale': None,
                'connect': None}

        self.shape = self.statechart.app.current_shape

        self.edit_menu = EditingShapeMenu()
        self.statechart.app.drawing_area.add_widget(self.edit_menu)
        self.edit_menu.pos = self.shape.pos[0]+ self.shape.width, self.shape.pos[1]

    def exit_state(self, context=None):
        pass

    def shape_label_edited(self, text, *args):
        '''An action method associated with the text input. There is a
        binding to fire this action on_text_validate.'''

        self.shape.label.text = text

    def shape_label_anchor_changed(self, text, *args):
        '''An action method associated with the text input. There is a
        binding to fire this action on_text_validate.'''

        if text == 'NW':
            anchor_x = 'left'
            anchor_y = 'top'
        elif text == 'N':
            anchor_x = 'center'
            anchor_y = 'top'
        elif text == 'NE':
            anchor_x = 'right'
            anchor_y = 'top'
        elif text == 'W':
            anchor_x = 'left'
            anchor_y = 'center'
        elif text == 'C':
            anchor_x = 'center'
            anchor_y = 'center'
        elif text == 'E':
            anchor_x = 'right'
            anchor_y = 'center'
        elif text == 'SW':
            anchor_x = 'left'
            anchor_y = 'bottom'
        elif text == 'S':
            anchor_x = 'center'
            anchor_y = 'bottom'
        elif text == 'SE':
            anchor_x = 'right'
            anchor_y = 'bottom'

        self.shape.label_anchor_x = anchor_x
        self.shape.label_anchor_y = anchor_y

        print 'ANCHORS', self.shape.label_anchor_x, self.shape.label_anchor_y

    def shape_label_halign_edited(self, text, *args):
        '''An action method associated with the halign spinner,
        bound to fire this action on_text.'''

        self.shape.label.halign = text

    def shape_label_valign_edited(self, text, *args):
        '''An action method associated with the valign spinner,
        bound to fire this action on_text.'''

        self.shape.label.valign = text

    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_move',
                          'drawing_area_touch_up',
                          'show_editing_shape_submenu',
                          'hide_editing_shape_submenu'])
    def handle_menu_touch(self, event, context, arg):

        if event == 'show_editing_shape_submenu':

            if context.text == 'Label':

                self.selector.grid.bind(
                        minimum_size=self.selector.grid.setter('size'))

                menu = context.text.lower()
                self.statechart.app.swap_in_submenu(
                        context, self.menus_and_submenus[menu])

        elif event == 'hide_editing_shape_submenu':

            # context.parent.parent.parent is the scrollview.
            Animation(scroll_x=0, d=.5).start(context.parent.parent.parent)
