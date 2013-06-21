from kivy_statecharts.system.state import State


class WaitingForTouches(State):
    '''The WaitingForTouches state dispatches to transient states for adding,
    moving, and connecting shapes, based on touches analyzed.
    '''

    def __init__(self, **kwargs):
        super(WaitingForTouches, self).__init__(**kwargs)

    @State.event_handler(['drawing_area_touch_down', 'drawing_area_touch_move', 'drawing_area_touch_up'])
    def handle_touch(self, event, touch, context):

        if event == 'drawing_area_touch_down':

            self.statechart.app.touch = touch

        elif event == 'drawing_area_touch_move':

            print 'touch', touch.pos, 'shapes = ', len(self.statechart.app.shapes)
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

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass
