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
        on_release: app.statechart.send_event('select_menu_back', self, None)
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Pick'
            on_release: app.statechart.send_event('select_menu_pick', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Marquee'
            on_release: app.statechart.send_event('select_menu_marquee', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Node'
            on_release: app.statechart.send_event('select_menu_node', self, None)

<TextSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('text_menu_back', self, None)
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Large'
            on_release: app.statechart.send_event('text_menu_large', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Medium'
            on_release: app.statechart.send_event('text_menu_medium', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Small'
            on_release: app.statechart.send_event('text_menu_small', self, None)

<LineSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('line_menu_back', self, None)
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Straight'
            on_release: app.statechart.send_event('line_menu_straight', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Arc'
            on_release: app.statechart.send_event('line_menu_arc', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Bezier'
            on_release: app.statechart.send_event('line_menu_bezier', self, None)

<ShapeSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('shape_menu_back', self, None)
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Rectangle'
            on_release: app.statechart.send_event('shape_menu_rectangle', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Ellipse'
            on_release: app.statechart.send_event('shape_menu_ellipse', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Polygon'
            on_release: app.statechart.send_event('shape_menu_polygon', self, None)

<StateSubmenu>:
    Button:
        text: '<'
        size_hint: (.15, 1)
        on_release: app.statechart.send_event('state_menu_back', self, None)
    BoxLayout:
        orientation: 'vertical'
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Rectangle'
            on_release: app.statechart.send_event('state_menu_rectangle', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Ellipse'
            on_release: app.statechart.send_event('state_menu_ellipse', self, None)
        Button:
            size_hint: (None, 1)
            width: 85
            text: 'Polygon'
            on_release: app.statechart.send_event('state_menu_polygon', self, None)
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

        self.menu_actions_and_submenus = {'show_select_submenu': SelectSubmenu(),
                                          'show_text_submenu': TextSubmenu(),
                                          'show_line_submenu': LineSubmenu(),
                                          'show_shape_submenu': ShapeSubmenu(),
                                          'show_state_submenu': StateSubmenu()}

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

    def swap_in_submenu(self, context, submenu):

        drawing_menu = context.parent.parent.parent.parent
        scrollview = context.parent.parent.parent
        boxlayout = context.parent.parent

        # Add the submenu to the BoxLayout in the menu scrollview. First check
        # to see if a submenu is present, and remove it, before adding the
        # submenu to swap in.

        if len(boxlayout.children) == 2:
            boxlayout.remove_widget(boxlayout.children[0])

        boxlayout.add_widget(submenu)

        Animation(scroll_x=1, d=.5).start(scrollview)

    @State.event_handler(['show_select_submenu',
                          'select_menu_pick',
                          'select_menu_marquee',
                          'select_menu_node',
                          'select_menu_back',
                          'show_text_submenu',
                          'text_menu_large',
                          'text_menu_medium',
                          'text_menu_small',
                          'text_menu_back',
                          'show_line_submenu',
                          'line_menu_straight',
                          'line_menu_arc',
                          'line_menu_bezier',
                          'line_menu_back',
                          'show_shape_submenu',
                          'shape_menu_rectangle',
                          'shape_menu_ellipse',
                          'shape_menu_polygon',
                          'shape_menu_back',
                          'show_state_submenu',
                          'state_menu_rectangle',
                          'state_menu_ellipse',
                          'state_menu_polygon',
                          'state_menu_back'])
    def handle_menu_touch(self, event, context, arg):

        if event.endswith('_submenu'):

            self.swap_in_submenu(context, self.menu_actions_and_submenus[event])

        elif event.endswith('back'):

            Animation(scroll_x=0, d=.5).start(context.parent.parent.parent)

        else:

            print context.text + ' selected'
