from kivy_statecharts.system.state import State

from kivy.graphics import Color, Line
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from graphics import LabeledVectorShape


class ConnectorLVS(LabeledVectorShape):
    shape = ListProperty([.9, .9])
    points = ListProperty([0]*2)
    shape1 = ObjectProperty(None)
    shape2 = ObjectProperty(None)

    def __init__(self, **kwargs):

        super(LabeledVectorShape, self).__init__(**kwargs)

        if 'text' in kwargs:
            self.label.text = kwargs['text']
        else:
            self.label.text = 'unknown'

    def on_touch_down(self, touch):
        print 'connector touch', touch.pos
        return super(LabeledVectorShape, self).on_touch_down(touch)

    def move_with_shape(self, shape, dx, dy):
        if shape == self.shape1:
            self.points[2] += dx
            self.points[3] += dy

            self.width = self.points[2] - self.points[0]
            self.height = self.points[3] - self.points[1]

            self.size = (self.width, self.height)
        else:
            self.pos[0] += dx
            self.pos[1] += dy
            self.x += dx
            self.y += dy
            self.points[0] += dx
            self.points[1] += dy

    def recalculate_points(self, *args):

        self.points[0] = self.pos[0] + int(float(self.size[0]) * self.shape[0])
        self.points[1] = self.pos[1] + int(float(self.size[1]) * self.shape[1])


class ConnectingShapes(State):
    '''The ConnectingShape state is a transient state -- after connecting the
    shape, if there is a shape found on mouse-up, there is an immediate
    transition back to the ShowingDrawingArea state, and its substate,
    WaitingForTouches.'''

    def __init__(self, **kwargs):
        super(ConnectingShapes, self).__init__(**kwargs)

    def enter_state(self, context=None):
        pass

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_up', ])
    def handle_touch(self, event, touch, context):

        # event == 'drawing_area_touch_up':

        target_shape_for_connection = None

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
            self.connect(self.statechart.app.selected_shape,
                         target_shape_for_connection)

        self.statechart.app.selected_shape = target_shape_for_connection

        self.go_to_state('ShowingDrawingArea')

    def connect(self, shape1, shape2):
        point1, point2 = shape1.find_connection(shape2)

        print 'connection found', point1, point2
        points = [point1[0], point1[1], point2[0], point2[1]]
        width = point2[0] - point1[0]
        height = point2[1] - point2[1]
        with self.statechart.app.drawing_area.canvas.after:
            Color(1, 1, 0)
            connection = ConnectorLVS(
                    shape1=shape1,
                    shape2=shape2,
                    points=points,
                    pos=point1,
                    size=(width, height),
                    x=point1[0],
                    y=point1[1],
                    width=width,
                    height=height,
                    text='connector',
                    label_placement='constrained',
                    label_containment='inside',
                    label_anchor='left_middle',
                    stroke_width=4.0,
                    stroke_color=[.2, .9, .2, .8],
                    fill_color=[.4, .4, .4, .4])

            self.statechart.app.shapes.append(connection)

            shape1.connections.append(connection)
            shape2.connections.append(connection)
