from kivy.app import App

from kivy_statecharts.system.state import State

from kivy.uix.label import Label


class MovingStateShape(State):
    '''The MovingStateShape state is a transient state -- after moving the
    shape, there is an immediate transition back to the ShowingDrawingScreen
    state.
    '''

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

            # TODO: What is the cost of using a local shape var, vs. self.app.ref?
            self.app.moving_shape.x += touch.dx
            self.app.moving_shape.y += touch.dy

            # TODO: For now, blindly move all children.
            for wid in [c for c in self.app.moving_shape.children]:
                wid.x += touch.dx
                wid.y += touch.dy

#            labels = [c for c in self.app.moving_shape.children if isinstance(c, Label)]
#
#            for label in labels:
#                label.x += touch.dx
#                label.y += touch.dy

            self.app.moving_shape.recalculate_points()

            for cp in self.app.moving_shape.connection_points:
                cp[0] += touch.dx
                cp[1] += touch.dy

            self.app.moving_shape.adjust_connections(touch.dx, touch.dy)

        elif event == 'drawing_area_touch_up':

            self.go_to_state('ShowingDrawingScreen')
