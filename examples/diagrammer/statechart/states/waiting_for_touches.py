from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.animation import Animation

from kivy.lang import Builder

from kivy.properties import ObjectProperty

from kivy_statecharts.system.state import State

# Menu touches involve swapping submenus out and animation.

Builder.load_string('''
<SelectSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('hide_drawing_submenu', self, 'select')
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Pick'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'select_pick')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Marquee'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'select_marquee')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Node'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'select_node')

<TextSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('hide_drawing_submenu', self, 'text')
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Large'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'text_large')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Medium'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'text_medium')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Small'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'text_small')

<LineSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('hide_drawing_submenu', self, 'line')
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Straight'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'line_straight')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Arc'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'line_arc')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Bezier'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'line_bezier')

<ShapeSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('hide_drawing_submenu', self, 'shape')
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Rectangle'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'shape_rectangle')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Ellipse'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'shape_ellipse')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Polygon'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'shape_polygon')

<StateSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('hide_drawing_submenu', self, 'state')
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Triangle'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'state_triangle')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Rectangle'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'state_rectangle')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Pentagon'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'state_pentagon')
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Ellipse'
            on_release: app.statechart.send_event('set_drawing_mode', self, 'state_ellipse')
''')


class SelectSubmenu(BoxLayout):
    pass


class TextSubmenu(BoxLayout):
    pass


class LineSubmenu(BoxLayout):
    pass


class ShapeSubmenu(BoxLayout):
    pass


class StateSubmenu(BoxLayout):
    pass


class WaitingForTouches(State):
    '''The WaitingForTouches state dispatches to transient states for adding,
    moving, and connecting shapes, based on touches analyzed.
    '''

    def __init__(self, **kwargs):
        super(WaitingForTouches, self).__init__(**kwargs)

    def enter_state(self, context=None):

        self.menus_and_submenus = {'select': SelectSubmenu(),
                                   'text': TextSubmenu(),
                                   'line': LineSubmenu(),
                                   'shape': ShapeSubmenu(),
                                   'state': StateSubmenu()}

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_move',
                          'drawing_area_touch_up'])
    def handle_drawing_area_touch(self, event, touch, context):

        if event == 'drawing_area_touch_down':

            self.statechart.app.touch = touch

        elif event == 'drawing_area_touch_move':

            for shape in reversed(self.statechart.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    print 'move on polygon edge', shape.canvas
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    print 'closest line segment', dist, line
                    self.statechart.app.current_shape = shape
                    dispatched = True
                    self.statechart.go_to_state('MovingShape')
                elif shape.collide_point(*touch.pos):
                    print 'move on shape internal area', shape.canvas
                    self.statechart.app.current_shape = shape
                    dispatched = True
                    self.statechart.go_to_state('AddingConnection')

        elif event == 'drawing_area_touch_up':

            dispatched = False

            for shape in reversed(self.statechart.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    print 'polygon touched', shape.canvas
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    print 'closest line segment', dist, line
                    self.statechart.app.current_shape = shape
                    shape.select()
                    dispatched = True
                    self.statechart.go_to_state('EditingShape')

            if not dispatched:
                self.statechart.go_to_state('AddingShape')

    @State.event_handler(['show_drawing_submenu',
                          'hide_drawing_submenu',
                          'set_drawing_mode'])
    def handle_menu_touch(self, event, context, arg):

        if event == 'show_drawing_submenu':

            menu = context.text.lower()
            self.statechart.app.swap_in_submenu(
                    context, self.menus_and_submenus[menu])

        elif event == 'hide_drawing_submenu':

            # context.parent.parent.parent is the scrollview.
            Animation(scroll_x=0, d=.5).start(context.parent.parent.parent)

        else:

            print context.text + ' selected'
            self.statechart.app.drawing_mode = arg
