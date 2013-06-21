from kivy_statecharts.system.state import State


class MovingShape(State):
    '''The MovingShape state is a transient state -- after moving the shape,
    there is an immediate transition back to the ShowingDrawingArea state, and
    its substate, WaitingForTouches.'''

    def __init__(self, **kwargs):
        super(MovingShape, self).__init__(**kwargs)

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_move',
                          'drawing_area_touch_up', ])
    def handle_touch(self, event, touch, context):

        if event == 'drawing_area_touch_move':

            self.statechart.app.current_shape.x += touch.dx
            self.statechart.app.current_shape.y += touch.dy
            self.statechart.app.current_shape.recalculate_points()
            for cp in self.statechart.app.current_shape.connection_points:
                cp[0] += touch.dx
                cp[1] += touch.dy
            self.statechart.app.current_shape.adjust_connections(touch.dx,
                                                                 touch.dy)

        elif event == 'drawing_area_touch_up':

            self.go_to_state('ShowingDrawingArea')
