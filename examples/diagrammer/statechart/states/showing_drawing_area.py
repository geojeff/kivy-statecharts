from kivy.app import App

from kivy.uix.label import Label

from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

from kivy_statecharts.system.state import State

from adding_state_shape import AddingStateShape
from moving_state_shape import MovingStateShape
from editing_state_shape import EditingStateShape
from adding_connection import AddingConnection

from views.drawing_area_screen import DrawingAreaScreen
from views.drawing_menus import GenericShapeSubmenu
from views.drawing_menus import StateShapeSubmenu


class ShowingDrawingArea(State):

    drawing_menu = ObjectProperty(None)
    drawing_area = ObjectProperty(None)

    menu_actions_and_submenus = DictProperty({})

    submenu = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):

        kwargs['AddingStateShape'] = AddingStateShape
        kwargs['MovingStateShape'] = MovingStateShape
        kwargs['EditingStateShape'] = EditingStateShape
        kwargs['AddingConnection'] = AddingConnection

        super(ShowingDrawingArea, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

        if (not 'DrawingArea'
                in self.app.screen_manager.screen_names):

            self.app.screen_manager.add_widget(
                    DrawingAreaScreen(name='DrawingArea'))

        if self.app.screen_manager.current != 'DrawingArea':
            self.app.screen_manager.current = 'DrawingArea'

        if not self.drawing_menu:
            self.drawing_menu = \
                self.app.screen_manager.current_screen.drawing_menu

        if not self.drawing_area:
            self.drawing_area = \
                self.app.screen_manager.current_screen.drawing_area

        if not self.menu_actions_and_submenus:
            self.menu_actions_and_submenus = {
                    'show_submenu_generic_shape_tool': GenericShapeSubmenu(),
                    'show_submenu_state_shape_tool': StateShapeSubmenu()}

    def exit_state(self, context=None):
        pass

    def make_justified_label(self, text, justification):

        help_label = Label(text=text, halign=justification)
        # Bind size of rendered label to text_size, for justification.
        help_label.bind(size=help_label.setter('text_size'))
        return help_label

    def go_to_help(self, *args):

        self.go_to_state('ShowingHelpScreen')

    @State.event_handler(['show_submenu_generic_shape_tool',
                          'show_submenu_state_shape_tool'])
    def handle_menu_touch(self, event, context, arg):

        if not self.submenu:
            self.submenu = self.menu_actions_and_submenus[event]

            self.submenu.pos = [context.center[0],
                                context.center[1] - self.submenu.height / 2]

            self.submenu.arrow_pos = 'left_mid'

            self.drawing_area.add_widget(self.submenu)

    @State.event_handler(['generic_shape_tool_changed',
                          'state_shape_tool_changed'])
    def handle_tool_menu_touch(self, event, context, arg):

        # Remove the submenu.

        self.drawing_area.remove_widget(self.submenu)

        self.submenu = None

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

            self.app.touch = touch

        elif event == 'drawing_area_touch_move':

            for shape in reversed(self.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    self.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.app.current_label = label
                    dispatched = True
                    self.statechart.go_to_state('MovingStateShape')
                elif shape.collide_point(*touch.pos):
                    self.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.app.current_label = label
                    dispatched = True
                    self.statechart.go_to_state('AddingConnection')

        elif event == 'drawing_area_touch_up':

            dispatched = False

            for shape in reversed(self.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    dist, line = shape.closest_edge(touch.pos[0],
                                                    touch.pos[1])
                    self.app.current_shape = shape
                    label = None
                    for c in shape.children:
                        if isinstance(c, Label):
                            label = c
                            break
                    self.app.current_label = label
                    self.app.current_anchored_label = \
                            shape.children[0]
                    shape.select()
                    dispatched = True
                    self.statechart.go_to_state('EditingStateShape')

            if not dispatched:
                if hasattr(self.app, 'touch'):
                    self.statechart.go_to_state('AddingStateShape')
