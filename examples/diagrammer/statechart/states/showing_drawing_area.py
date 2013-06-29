from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from kivy.lang import Builder

from kivy.properties import ObjectProperty

from kivy_statecharts.system.state import State

from adding_shape import AddingShape
from moving_shape import MovingShape
from editing_shape import EditingShape
from adding_connection import AddingConnection


Builder.load_string('''
#:import math math
#:import itertools itertools
#:import Shape graphics.Shape

<DrawingArea>:
    canvas:
        Color:
            rgba: .3, .3, .3, .3
        Rectangle:
            size: self.size
            pos: self.pos
    on_touch_down: app.statechart.send_event( \
            'drawing_area_touch_down', args[1]) \
            if self.collide_point(*args[1].pos) else None
    on_touch_move: app.statechart.send_event( \
            'drawing_area_touch_move', args[1]) \
            if self.collide_point(*args[1].pos) else None
    on_touch_up: app.statechart.send_event( \
            'drawing_area_touch_up', args[1]) \
            if self.collide_point(*args[1].pos) else None

[MenuButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'drawing_menu_root'
    on_release: app.statechart.send_event('show_drawing_submenu', self, None)
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    text: ctx.text
    Image:
        source: 'atlas://data/images/defaulttheme/tree_closed'
        size: (20, 20)
        y: self.parent.y + (self.parent.height/2) - (self.height/2)
        x: self.parent.x + (self.parent.width - self.width)

[DrawingMenuPolygonButton@BubbleButton]:

    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'drawing_menu_root'
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    height: ctx.height if hasattr(ctx, 'height') else 1
    on_release: app.statechart.send_event( \
            ctx.action, self, None)
    action: ctx.action
    text: ctx.text if hasattr(ctx, 'text') else ''
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Mesh:
            vertices: list(itertools.chain(*[ \
                       ((self.center[0]) \
                            + math.cos(i * ((2 * math.pi) / ctx.sides)) \
                                * ctx.radius, \
                        (self.center[1]) \
                            + math.sin(i * ((2 * math.pi) / ctx.sides)) \
                                * ctx.radius, \
                        math.cos(i * ((2 * math.pi) / ctx.sides)), \
                        math.sin(i * ((2 * math.pi) / ctx.sides))) \
                            for i in xrange(ctx.sides)]))
            indices: range(ctx.sides)
            mode: 'triangle_fan'

    Scatter:
        do_scale: False
        do_translation: False
        do_rotation: False
        auto_bring_to_front: False

<DrawingMenu>
    size_hint: None, None
    size: 70, 200
    pos_hint: { "center_y": 0.5 }
    padding: 5
    background_color: .2, .9, 1, .7
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    orientation: 'vertical'

    # root menu -- See submenus in waiting_for_touches.py.
    BoxLayout:
        padding: 5
        orientation: 'vertical'
        DrawingMenuPolygonButton:
            size_hint: None, None
            width: 60
            height: 60
            radius: 20
            sides: 0
            text: 'N.I.Y.'
            action: 'show_drawing_submenu_select'
        DrawingMenuPolygonButton:
            size_hint: None, None
            width: 60
            height: 60
            radius: 20
            sides: 0
            text: 'N.I.Y.'
            action: 'show_drawing_submenu_text'
        DrawingMenuPolygonButton:
            size_hint: None, None
            width: 60
            height: 60
            radius: 20
            sides: 3
            action: 'show_drawing_submenu_state'

<DrawingAreaScreen>
    drawing_area: drawing_area

    BoxLayout:
        orientation: 'vertical'
        spacing: 2

        BoxLayout:
            size_hint: 1, None
            height: 30

            ToggleButton:
                text: 'Help'
                group: 'screen manager buttons'
                on_press: app.statechart.send_event('go_to_help')

            ToggleButton:
                text: 'Drawing Area'
                color: [1.0, 1.0, 1.0, .9]
                bold: True
                group: 'screen manager buttons'
                state: 'down'

        BoxLayout:

            DrawingMenu:

            DrawingArea:
                id: drawing_area

<SelectSubmenu>:
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_select_pick'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_select_marquee'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_select_node'


<TextSubmenu>:
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_text_large'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_text_medium'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 0
        text: 'N.I.Y.'
        action: 'set_drawing_mode_text_small'

<LineSubmenu>:
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_line_straight'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_line_arc'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_line_bezier'

<ShapeSubmenu>:
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_shape_rectangle'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_shape_ellipse'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_shape_polygon'

<StateSubmenu>:
    size_hint: (None, None)
    size: (60, 180)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'left_mid'
    orientation: 'vertical'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 3
        action: 'set_drawing_mode_state_triangle'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 4
        action: 'set_drawing_mode_state_rectangle'

    DrawingMenuPolygonButton:
        size_hint: None, None
        width: 60
        height: 60
        radius: 20
        sides: 5
        action: 'set_drawing_mode_state_pentagon'
''')


class DrawingAreaScreen(Screen):
    pass


class DrawingMenu(Bubble):
    pass


class DrawingArea(Widget):

    pass


class SelectSubmenu(Bubble):
    pass


class TextSubmenu(Bubble):
    pass


class LineSubmenu(Bubble):
    pass


class ShapeSubmenu(Bubble):
    pass


class StateSubmenu(Bubble):
    pass


class ShowingDrawingArea(State):

    drawing_area = ObjectProperty(None)

    def __init__(self, **kwargs):

        kwargs['AddingShape'] = AddingShape
        kwargs['MovingShape'] = MovingShape
        kwargs['EditingShape'] = EditingShape
        kwargs['AddingConnection'] = AddingConnection

        super(ShowingDrawingArea, self).__init__(**kwargs)

    def enter_state(self, context=None):

        if (not 'DrawingArea'
                in self.statechart.app.screen_manager.screen_names):

            self.statechart.app.screen_manager.add_widget(
                    DrawingAreaScreen(name='DrawingArea'))

        if self.statechart.app.screen_manager.current != 'DrawingArea':
            self.statechart.app.screen_manager.current = 'DrawingArea'

        self.drawing_area = \
                self.statechart.app.screen_manager.current_screen.drawing_area

        self.menus_and_submenus = {'select': SelectSubmenu(),
                                   'text': TextSubmenu(),
                                   'line': LineSubmenu(),
                                   'shape': ShapeSubmenu(),
                                   'state': StateSubmenu()}

    def exit_state(self, context=None):
        pass

    def make_justified_label(self, text, justification):

        help_label = Label(text=text, halign=justification)
        # Bind size of rendered label to text_size, for justification.
        help_label.bind(size=help_label.setter('text_size'))
        return help_label

    def go_to_help(self, *args):

        self.go_to_state('ShowingHelpScreen')

    @State.event_handler(['show_drawing_submenu_select',
                          'show_drawing_submenu_text',
                          'show_drawing_submenu_state',
                          'set_drawing_mode_select_pick',
                          'set_drawing_mode_select_marquee',
                          'set_drawing_mode_select_node',
                          'set_drawing_mode_text_large',
                          'set_drawing_mode_text_medium',
                          'set_drawing_mode_text_small',
                          'set_drawing_mode_line_straight',
                          'set_drawing_mode_line_arc',
                          'set_drawing_mode_line_bezier',
                          'set_drawing_mode_shape_rectangle',
                          'set_drawing_mode_shape_ellipse',
                          'set_drawing_mode_shape_polygon',
                          'set_drawing_mode_state_triangle',
                          'set_drawing_mode_state_rectangle',
                          'set_drawing_mode_state_pentagon'])
    def handle_menu_touch(self, event, context, arg):

        if event.startswith('show_drawing_submenu'):

            self.submenu = self.menus_and_submenus[event[21:]]

            self.submenu.pos = [context.center[0],
                                context.center[1] - self.submenu.height / 2]

            self.drawing_area.add_widget(self.submenu)

        else:

            self.statechart.app.drawing_mode = event[17:]

            self.drawing_area.remove_widget(self.submenu)

            self.submenu = None


    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_move',
                          'drawing_area_touch_up'])
    def handle_drawing_area_touch(self, event, touch, context):

        # Perform click-away pop-down for submenu, if there is a touch on the
        # drawing area while the submenu is up.
        #
        # TODO: The bottom button, and perhaps others, has some problems,
        # depending on where you click, relative to the drawing area and the
        # main menu.  The new shape type is not always selected (no shape is,
        # iirc).
        #
        if hasattr(self, 'submenu') and self.submenu:
            if not self.submenu.collide_point(*touch.pos):
                self.drawing_area.remove_widget(self.submenu)
                # TODO: Something else to do here?
                return
            else:
                return

        if event == 'drawing_area_touch_down':

            self.statechart.app.touch = touch

        elif event == 'drawing_area_touch_move':

            for shape in reversed(self.statechart.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    self.statechart.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.statechart.app.current_label = label
                    dispatched = True
                    self.statechart.go_to_state('MovingShape')
                elif shape.collide_point(*touch.pos):
                    self.statechart.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.statechart.app.current_label = label
                    dispatched = True
                    self.statechart.go_to_state('AddingConnection')

        elif event == 'drawing_area_touch_up':

            dispatched = False

            for shape in reversed(self.statechart.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    self.statechart.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.statechart.app.current_label = label
                    self.statechart.app.current_anchored_label = \
                            shape.children[0]
                    shape.select()
                    dispatched = True
                    self.statechart.go_to_state('EditingShape')

            if not dispatched:
                if hasattr(self.statechart.app, 'touch'):
                    self.statechart.go_to_state('AddingShape')
