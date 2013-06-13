from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

from kivy.properties import ObjectProperty

from kivy_statecharts.system.state import State

from kivy.uix.screenmanager import Screen

from kivy.uix.image import Image

from waiting_for_touches import WaitingForTouches
from adding_shape import AddingShape
from moving_shape import MovingShape
from connecting_shapes import ConnectingShapes


class DrawingArea(Image):

    statechart = ObjectProperty(None)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event('drawing_area_touch_down', touch)
        else:
            return super(DrawingArea, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event('drawing_area_touch_move', touch)
        #return super(DrawingArea, self).on_touch_move(touch)

    def on_touch_up(self, touch):

        self.statechart.send_event('drawing_area_touch_up', touch)

        return super(DrawingArea, self).on_touch_up(touch)


class ShowingDrawingArea(State):

    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'WaitingForTouches'
        kwargs['WaitingForTouches'] = WaitingForTouches
        kwargs['AddingShape'] = AddingShape
        kwargs['MovingShape'] = MovingShape
        kwargs['ConnectingShapes'] = ConnectingShapes
        super(ShowingDrawingArea, self).__init__(**kwargs)

    def enter_state(self, context=None):

        if (not 'DrawingArea'
                in self.statechart.app.screen_manager.screen_names):

            # Convenience references:

            self.app = self.statechart.app

            view = GridLayout(cols=1, spacing=20)

            toolbar = BoxLayout(size_hint=(1.0, None), height=30)

            button = ToggleButton(text='Main', group='screen manager buttons')
            button.bind(on_press=self.go_to_main)
            toolbar.add_widget(button)

            button = ToggleButton(text='DrawingArea',
                                  color=[1.0, 1.0, 1.0, .9],
                                  bold=True,
                                  group='screen manager buttons')

            button.state = 'down'

            toolbar.add_widget(button)

            view.add_widget(toolbar)

            self.statechart.app.drawing_area = DrawingArea(
                    statechart=self.statechart,
                    source='design/images/rect.png')

            view.add_widget(self.statechart.app.drawing_area)

            # Finally, add to this screen to the screen manager.
            screen = Screen(name='DrawingArea')
            screen.add_widget(view)
            self.app.screen_manager.add_widget(screen)

        if self.app.screen_manager.current != 'DrawingArea':
            self.app.screen_manager.current = 'DrawingArea'

    def exit_state(self, context=None):
        pass

    def make_justified_label(self, text, justification):
        help_label = Label(text=text, halign=justification)
        # Bind size of rendered label to text_size, for justification.
        help_label.bind(size=help_label.setter('text_size'))
        return help_label

    def go_to_main(self, *args):
        self.go_to_state('ShowingMainScreen')
