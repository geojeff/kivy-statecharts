from kivy.app import App

from kivy_statecharts.system.state import State

from kivy.uix.label import Label


class MovingStateShape(State):
    '''The MovingStateShape state is a transient state -- after moving the shape,
    there is an immediate transition back to the ShowingDrawingArea state.'''

    def __init__(self, **kwargs):
        super(MovingStateShape, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_move',
                          'drawing_area_touch_up', ])
    def handle_touch(self, event, touch, context):

        if event == 'drawing_area_touch_move':

            shape = self.app.current_shape

            shape.x += touch.dx
            shape.y += touch.dy

            labels = [c for c in shape.children if isinstance(c, Label)]

            for label in labels:
                label.x += touch.dx
                label.y += touch.dy

            shape.recalculate_points()

            for cp in shape.connection_points:
                cp[0] += touch.dx
                cp[1] += touch.dy

            shape.adjust_connections(touch.dx, touch.dy)

        elif event == 'drawing_area_touch_up':

            self.go_to_state('ShowingDrawingArea')
