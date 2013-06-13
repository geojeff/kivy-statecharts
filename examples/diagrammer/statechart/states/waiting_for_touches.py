from kivy_statecharts.system.state import State


class WaitingForTouches(State):
    '''The WaitingForTouches state dispatches to transient states for adding,
    moving, and connecting shapes, based on touches analyzed.
    '''

    def __init__(self, **kwargs):
        super(WaitingForTouches, self).__init__(**kwargs)

    def establish_drawing_mode(self):

        touch = self.statechart.app.touch

        dispatched = False

        print
        print 'touch', touch.pos, 'shapes = ', len(self.statechart.app.shapes)
        for shape in reversed(self.statechart.app.shapes):
            if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                print 'polygon touched', shape.canvas
                dist, line = shape.closest_line_segment(touch.pos[0],
                                                        touch.pos[1])
                print 'closest line segment', dist, line
                self.statechart.app.selected_shape = shape
                dispatched = True
                self.statechart.go_to_state('MovingShape')
            elif shape.collide_point(*touch.pos):
                print 'shape touched', shape.canvas
                self.statechart.app.selected_shape = shape
                dispatched = True
                self.statechart.go_to_state('ConnectingShapes')

        if not dispatched:

            self.statechart.go_to_state('AddingShape')

    @State.event_handler(['drawing_area_touch_down', ])
    def handle_touch(self, event, touch, context):

        # event == 'drawing_area_touch_down':

        self.statechart.app.touch = touch
        self.establish_drawing_mode()

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass
