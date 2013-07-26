from kivy.app import App

from kivy_statecharts.system.state import State

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.animation import Animation

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from kivy.lang import Builder

Builder.load_string('''
#:import ListItemButton kivy.uix.listview.ListItemButton
#:import ListAdapter kivy.adapters.listadapter.ListAdapter

[EditingStateShapeMenuButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'editing_shape_menu_root'
    on_release: app.statechart.send_event( \
            'show_editing_shape_submenu', self, None)
    size_hint: (None, 1)
    width: 100
    text: ctx.text
    Image:
        source: 'atlas://data/images/defaulttheme/tree_closed'
        size: (20, 20)
        y: self.parent.y + (self.parent.height/2) - (self.height/2)
        x: self.parent.x + (self.parent.width - self.width)

<EditingStateShapeMenu>
    size_hint: None, None
    size: 380, 580
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
                    EditingStateShapeMenuButton:
                        text: 'Labels'
                    EditingStateShapeMenuButton:
                        text: 'Fill'
                    EditingStateShapeMenuButton:
                        text: 'Stroke'
                    EditingStateShapeMenuButton:
                        text: 'Scale'
                    EditingStateShapeMenuButton:
                        text: 'Connections'

[AnchorButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'anchor_buttons'
    on_release: app.statechart.send_event( \
             'do_quick_spot', self.text, None)
    size_hint: None, None
    size: 40, 40
    text: ctx.text

<EditingStateShapeLabelsSubmenu>:
    spacing: '5sp'

    Button:
        text: '<'
        size_hint_x: None
        width: 25
        on_release: app.statechart.send_event( \
                'hide_editing_shape_submenu', self, 'state')

    StackLayout:
        orientation: 'tb-lr'
        #size_hint_y: None if root.width < root.height else 1
        #height: sp(99 + 33 + 2 + 99 + 33 + 150 + 99) \
        #       if root.width < root.height else self.height
        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '99sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'All labels:'

            ListView:
                canvas:
                    Color:
                        rgba: .3, .3, .3, .3
                    Rectangle:
                        size: self.size
                        pos: self.pos
                adapter:
                    ListAdapter(data=root.labels, \
                            cls=ListItemButton, \
                            args_converter=lambda rowindex, obj: { \
                                        'text': obj.text, \
                                        'size_hint_y': None, \
                                        'height': 25}, \
                            allow_empty_selection=False, \
                            on_selection_change=app.statechart.send_event( \
                                'shape_label_selected'))

        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'Label actions:'

            BoxLayout:

                Button:
                    text: 'Add'
                    on_release: app.statechart.send_event('add_shape_label')
                Button:
                    text: 'Delete'
                    on_release: app.statechart.send_event('delete_shape_label')

        BoxLayout:
            size_hint_y: None
            height: '2sp' if root.width < root.height else self.height
            #size_hint_x: .5 if root.width < root.height else 1

            canvas:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '99sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'Selected Label:'

            AnchorLayout:

                TextInput:
                    size_hint_y: None
                    height: '99sp'
                    #multiline: False
                    text: app.current_label.text
                    on_text: app.statechart.send_event( \
                            'shape_label_edited', self.text)

        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'halign / valign:'

            BoxLayout:

                Spinner:
                    text: app.current_label.halign
                    values: 'left', 'center', 'right'
                    on_text: app.statechart.send_event( \
                            'shape_label_halign_edited', self.text)

                Spinner:
                    text: app.current_label.valign
                    values: 'top', 'middle', 'bottom'
                    on_text: app.statechart.send_event( \
                            'shape_label_valign_edited', self.text)

        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '150sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'Quick spot:'

            GridLayout:
                id: _grid
                rows: 3
                cols: 3
                spacing: 10
                padding: 10

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
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '99sp' if root.width < root.height else self.height
            spacing: '2sp'

            Label:
                text: 'x / y:'

            GridLayout:
                cols: 2

                Slider:
                    size_hint: None, None
                    size: 99, 99
                    value: app.current_label.pos[0]
                    on_value: app.statechart.send_event( \
                            'set_x', float(args[1]))
                    min: app.current_shape.pos[0] - \
                            app.current_shape.width
                    max: app.current_shape.pos[0] + \
                            app.current_shape.width * 1.2

                Slider:
                    orientation: 'vertical'
                    size_hint: None, None
                    size: 90, 90
                    value: app.current_label.pos[1]
                    on_value: app.statechart.send_event( \
                            'set_y', float(args[1]))
                    min: app.current_shape.pos[1] - \
                            app.current_shape.height
                    max: app.current_shape.pos[1] + \
                            app.current_shape.height * 1.2

        BoxLayout:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            spacing: '2sp'

            Button:
                text: 'Done'
                on_release: app.statechart.send_event('done')

<EditingStateShapeFillSubmenu>:
    Button:
        text: '<'
        #size_hint: (.15, 1)
        size_hint_x: None
        width: 25
        on_release: app.statechart.send_event( \
                'hide_editing_shape_submenu', self, 'state')

    BoxLayout:
        spacing: '2sp'
        orientation: 'vertical'

        Label:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            text: 'Fill Color'

        ColorPicker:
            color: app.current_shape.fill_color
            on_color: app.statechart.send_event('fill_color_changed', self.color)

        Button:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            text: 'Done'
            on_release: app.statechart.send_event('done')

<EditingStateShapeStrokeSubmenu>:
    Button:
        text: '<'
        #size_hint: (.15, 1)
        size_hint_x: None
        width: 25
        on_release: app.statechart.send_event( \
                'hide_editing_shape_submenu', self, 'state')

    BoxLayout:
        spacing: '2sp'
        orientation: 'vertical'

        Label:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            text: 'Fill Color'

        ColorPicker:
            color: app.current_shape.stroke_color
            on_color: app.statechart.send_event('stroke_color_changed', self.color)

        Button:
            size_hint_y: None if root.width < root.height else 0.125
            #size_hint_x: .5 if root.width < root.height else 1
            height: '33sp' if root.width < root.height else self.height
            text: 'Done'
            on_release: app.statechart.send_event('done')
''')


class EditingStateShapeLabelsSubmenu(BoxLayout):
    statechart = ObjectProperty(None)
    labels = ListProperty([])


class EditingStateShapeFillSubmenu(BoxLayout):
    statechart = ObjectProperty(None)


class EditingStateShapeStrokeSubmenu(BoxLayout):
    statechart = ObjectProperty(None)


class EditingStateShapeMenu(BoxLayout):
    pass


class BoundedLabel(Label):
    pass


class Selector(BoxLayout):
    grid = ObjectProperty(None)


class EditingStateShape(State):
    '''
    '''

    editing_shape_menu = ObjectProperty(None)

    shape = ObjectProperty(None)
    labels = ListProperty([])

    def __init__(self, **kwargs):
        super(EditingStateShape, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

        drawing_area = \
                self.app.screen_manager.current_screen.drawing_area

        self.shape = self.app.current_shape

        self.labels = [c for c in self.shape.children if isinstance(c, Label)]

        self.menus_and_submenus = {
            'labels': EditingStateShapeLabelsSubmenu(statechart=self.statechart,
                                                labels=self.labels),
            'fill': EditingStateShapeFillSubmenu(statechart=self.statechart),
            'stroke': EditingStateShapeStrokeSubmenu(statechart=self.statechart),
            'scale': None,
            'connections': None}

        if not self.editing_shape_menu:
            self.editing_shape_menu = Popup(
                    size_hint=(None, None),
                    size=(400, 640),
                    attach_to=drawing_area,
                    title='Editing Shape',
                    content=EditingStateShapeMenu())

        self.editing_shape_menu.open()

    def exit_state(self, context=None):
        '''Tear down current widgets associated with this state.'''

        self.editing_shape_menu.dismiss()

    def shape_label_selected(self, adapter, *args):

        # TODO: Why is this guard condition needed?
        if adapter:
            self.app.current_label = adapter.selection[0]

    def shape_label_edited(self, text, *args):
        '''An action method associated with the text input. There is a
        binding to fire this action on_text_validate.'''

        self.app.current_label.text = text

    def fill_color_changed(self, color, *args):

        self.app.current_shape.fill_color = color

    def stroke_color_changed(self, color, *args):

        self.app.current_shape.stroke_color = color

    def do_quick_spot(self, spot, *args):
        '''Change the pos of the label to one of the following "spots":
        NW, N, NE, W, C, E, SW, S, SE.'''

        spots = {
                'NW': {'x_offset_factor': 0,  'y_offset_factor': 1},
                'N':  {'x_offset_factor': .5, 'y_offset_factor': 1},
                'NE': {'x_offset_factor': 1,  'y_offset_factor': 1},
                'W':  {'x_offset_factor': 0,  'y_offset_factor': .5},
                'C':  {'x_offset_factor': .5, 'y_offset_factor': .5},
                'E':  {'x_offset_factor': 1,  'y_offset_factor': .5},
                'SW': {'x_offset_factor': 0,  'y_offset_factor': 0},
                'S':  {'x_offset_factor': .5, 'y_offset_factor': 0},
                'SE': {'x_offset_factor': 1,  'y_offset_factor': 0}}

        self.app.current_label.pos = (
                self.app.current_shape.pos[0] +
                    spots[spot]['x_offset_factor']
                        * self.app.current_shape.size[0],
                self.app.current_shape.pos[1] +
                    spots[spot]['y_offset_factor']
                        * self.app.current_shape.size[1])

    def set_x(self, x, *args):
        '''Set the x value of the label from the slider.'''

        self.app.current_label.pos = (
                x,
                self.app.current_shape.pos[1])

    def set_y(self, y, *args):
        '''Set the y value of the label from the slider.'''

        self.app.current_label.pos = (
                self.app.current_shape.pos[0],
                y)

    def shape_label_halign_edited(self, text, *args):
        '''An action method associated with the halign spinner,
        bound to fire this action on_text.'''

        self.app.current_label.halign = text

    def shape_label_valign_edited(self, text, *args):
        '''An action method associated with the valign spinner,
        bound to fire this action on_text.'''

        self.app.current_label.valign = text

    def done(self, *args):

        self.statechart.go_to_state('ShowingDrawingScreen')

    def swap_in_submenu(self, context, submenu):

        scrollview = context.parent.parent.parent
        boxlayout = context.parent.parent

        # Add the submenu to the BoxLayout in the menu scrollview. First check
        # to see if a submenu is present, and remove it, before adding the
        # submenu to swap in.

        if len(boxlayout.children) == 2:
            boxlayout.remove_widget(boxlayout.children[0])

        boxlayout.add_widget(submenu)

        Animation(scroll_x=1, d=.5).start(scrollview)

    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_move',
                          'drawing_area_touch_up',
                          'show_editing_shape_submenu',
                          'hide_editing_shape_submenu'])
    def handle_menu_touch(self, event, context, arg):

        # TODO: What about the drawing_area events? Are they "consumed" by
        #       their simple inclusion in this handler?

        if event in ['show_editing_shape_submenu',
                     'show_editing_shape_submenu']:

            menu_name = context.text.lower()

            submenu = self.menus_and_submenus[menu_name]

            # TODO: Write scale and connections widgets.
            if not menu_name in ['scale', 'connections']:
                self.swap_in_submenu(context, submenu)

        elif event in ['hide_editing_shape_submenu',
                       'hide_editing_shape_submenu']:

            # context.parent.parent.parent is the scrollview.
            Animation(scroll_x=0, d=.5).start(context.parent.parent.parent)
