from kivy_statecharts.system.state import State

from kivy.graphics import Color, Line
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from graphics import ConnectionLVS

from adjusting_connection import AdjustingConnection


class AddingConnection(State):
    '''The AddingConnection state is a transient state -- after connecting the
    shape, if there is a shape found on mouse-up, a working connection is made
    and bubbles appear on each end for dragging / accepting connection points,
    after a transition to AdjustingConnection, which handles finalization.
    If there is no shape found on mouse-up, there is an immediate
    transition back to the ShowingDrawingArea state, and its substate,
    WaitingForTouches.'''

    realtime_line = ObjectProperty(None, allownone=True)

    # To avoid recomputing the center of shape1, store it.
    center1 = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['AdjustingConnection'] = AdjustingConnection
        super(AddingConnection, self).__init__(**kwargs)

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_up',
                          'drawing_area_touch_move', ])
    def handle_touch(self, event, touch, context):

        if event == 'drawing_area_touch_up':

            target_shape_for_connection = None

            # Switch the order of these loops, and add condition to only do the
            # polygon search if successful?

            for shape in reversed(self.statechart.app.shapes):
                if shape.collide_point(*touch.pos):
                    print 'shape touched', shape.canvas
                    target_shape_for_connection = shape
                    break

            for shape in reversed(self.statechart.app.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    print 'polygon touched', shape.canvas
                    dist, line = shape.closest_line_segment(touch.pos[0],
                                                            touch.pos[1])
                    print 'closest line segment', dist, line
                    target_shape_for_connection = shape
                    break

            if target_shape_for_connection:
                self.connect(self.statechart.app.current_shape,
                             target_shape_for_connection)

                self.statechart.app.current_shape = target_shape_for_connection

                with self.statechart.app.drawing_area.canvas.before:
                    self.realtime_line.points = []

                self.realtime_line = None

                self.go_to_state('AdjustingConnection')
            else:
                self.go_to_state('ShowingDrawingArea')

        if event == 'drawing_area_touch_move':

            self.draw_realtime_line(Color(1.0, 1.0, 0.0, 1.0), touch)

    def draw_realtime_line(self, color, touch):

        with self.statechart.app.drawing_area.canvas.before:

            color = color

            if not self.realtime_line:
                self.center1 = list(self.statechart.app.current_shape.center())
                self.realtime_line = Line(
                        points=self.center1,
                        dash_offset=10,
                        dash_length=100,
                        width=4)
            else:
                self.realtime_line.points = self.center1 + list(touch.pos)

    def connect(self, shape1, shape2):

        point1_index = shape1.closest_cp_to_center_line(shape2)
        point2_index = shape2.closest_cp_to_center_line(shape1)

        point1 = shape1.connection_points[point1_index]
        point2 = shape2.connection_points[point2_index]

        width = point2[0] - point1[0]
        height = point2[1] - point2[1]

        with self.statechart.app.drawing_area.canvas.before:
            Color(1, 1, 0)
            connection = ConnectionLVS(
                    shape1=shape1,
                    shape2=shape2,
                    shape1_cp_index=point1_index,
                    shape2_cp_index=point2_index,
                    pos=point1,
                    size=(width, height),
                    x=point1[0],
                    y=point1[1],
                    width=width,
                    height=height,
                    text='connection',
                    label_placement='constrained',
                    label_containment='inside',
                    label_anchor='left_middle',
                    stroke_width=4.0,
                    stroke_color=[.2, .9, .2, .8],
                    fill_color=[.4, .4, .4, .4])

            self.statechart.app.connections.append(connection)
            self.statechart.app.current_connection = connection

            shape1.connections.append(connection)
            shape2.connections.append(connection)

        return point2
