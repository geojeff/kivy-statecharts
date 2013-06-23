from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.bubble import Bubble
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from kivy.lang import Builder

from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivy_statecharts.system.state import State

from waiting_for_touches import WaitingForTouches
from adding_shape import AddingShape
from moving_shape import MovingShape
from adding_connection import AddingConnection

# The context menu is modified from qua-non's context menu:
#
#     http://wiki.kivy.org/Contextual%20Menus
#
Builder.load_string('''
[MenuButton@ActionButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'drawing_menu_root'
    on_release: app.statechart.send_event(self.action, self, None)
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    text: ctx.text
    action: ctx.action
    Image:
        source: 'atlas://data/images/defaulttheme/tree_closed'
        size: (20, 20)
        y: self.parent.y + (self.parent.height/2) - (self.height/2)
        x: self.parent.x + (self.parent.width - self.width)

<DrawingMenu>
    size_hint: None, None
    size: 120, 450
    pos_hint: { "center_y": 0.5 }
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

                # root menu -- See submenus in waiting_for_touches.py.
                BoxLayout:
                    orientation: 'vertical'
                    MenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Select'
                        action: 'show_select_submenu'
                    MenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Text'
                        action: 'show_text_submenu'
                    MenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Line'
                        action: 'show_line_submenu'
                    MenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'Shape'
                        action: 'show_shape_submenu'
                    MenuButton:
                        size_hint: (None, 1)
                        width: 100
                        text: 'State'
                        action: 'show_state_submenu'
''')


class ActionButton(ToggleButton):

    action = StringProperty('')


class DrawingMenu(Bubble):

    statechart = ObjectProperty(None)


class DrawingArea(Image):

    statechart = ObjectProperty(None)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event('drawing_area_touch_down', touch)

        return super(DrawingArea, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event('drawing_area_touch_move', touch)

        return super(DrawingArea, self).on_touch_move(touch)

    def on_touch_up(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event('drawing_area_touch_up', touch)

        return super(DrawingArea, self).on_touch_up(touch)


class ShowingDrawingArea(State):

    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'WaitingForTouches'
        kwargs['WaitingForTouches'] = WaitingForTouches
        kwargs['AddingShape'] = AddingShape
        kwargs['MovingShape'] = MovingShape
        kwargs['AddingConnection'] = AddingConnection
        super(ShowingDrawingArea, self).__init__(**kwargs)

    def enter_state(self, context=None):

        if (not 'DrawingArea'
                in self.statechart.app.screen_manager.screen_names):

            page_view = GridLayout(cols=1, spacing=20)

            toolbar = BoxLayout(size_hint=(1.0, None), height=30)

            button = ToggleButton(text='Help', group='screen manager buttons')
            button.bind(on_press=self.go_to_help)
            toolbar.add_widget(button)

            button = ToggleButton(text='Drawing Area',
                                  color=[1.0, 1.0, 1.0, .9],
                                  bold=True,
                                  group='screen manager buttons')

            button.state = 'down'

            toolbar.add_widget(button)

            page_view.add_widget(toolbar)

            drawing_view = BoxLayout(size_hint=(1.0, 1.0))

            self.statechart.app.drawing_menu = DrawingMenu()

            drawing_view.add_widget(self.statechart.app.drawing_menu)

            self.statechart.app.drawing_area = DrawingArea(
                    statechart=self.statechart,
                    source='design/images/rect.png')

            drawing_view.add_widget(self.statechart.app.drawing_area)

            page_view.add_widget(drawing_view)

            # Finally, add to this screen to the screen manager.
            screen = Screen(name='DrawingArea')
            screen.add_widget(page_view)
            self.statechart.app.screen_manager.add_widget(screen)

        if self.statechart.app.screen_manager.current != 'DrawingArea':
            self.statechart.app.screen_manager.current = 'DrawingArea'

    def exit_state(self, context=None):
        pass

    def make_justified_label(self, text, justification):
        help_label = Label(text=text, halign=justification)
        # Bind size of rendered label to text_size, for justification.
        help_label.bind(size=help_label.setter('text_size'))
        return help_label

    def go_to_help(self, *args):
        self.go_to_state('ShowingHelpScreen')
