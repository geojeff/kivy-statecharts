from kivy_statecharts.system.state import State

from kivy.graphics import Color, Line

from graphics import RectangleLIS
from graphics import TriangleLIS
from graphics import TriangleLVS


class StateRectangleLIS(RectangleLIS):

    def __init__(self, **kwargs):

        super(StateRectangleLIS, self).__init__(**kwargs)

        if 'state' in kwargs:
            self.label.text = kwargs['state']


class StateTriangleLIS(TriangleLIS):

    def __init__(self, **kwargs):

        self.label_data['in_center'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_top_middle'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_bottom_middle'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_left_middle'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_right_middle'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_nw_corner'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_ne_corner'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_se_corner'] = (0.5, 0.2, 'center', 'middle')
        self.label_data['in_sw_corner'] = (0.5, 0.2, 'center', 'middle')

        self.label_data['out_center'] = (0.5, -0.1, 'center', 'top')
        self.label_data['out_top_middle'] = (0.5, 1.0, 'center', 'bottom')
        self.label_data['out_bottom_middle'] = (0.5, -0.1, 'center', 'top')
        self.label_data['out_left_middle'] = (0.25, 0.5, 'right', 'middle')
        self.label_data['out_right_middle'] = (0.75, 0.5, 'left', 'middle')
        self.label_data['out_nw_corner'] = (0.4, 0.8, 'right', 'middle')
        self.label_data['out_ne_corner'] = (0.6, 0.8, 'left', 'middle')
        self.label_data['out_se_corner'] = (0.0, 0.1, 'right', 'middle')
        self.label_data['out_sw_corner'] = (1.0, 0.1, 'left', 'middle')

        super(StateTriangleLIS, self).__init__(**kwargs)

        if 'state' in kwargs:
            self.label.text = kwargs['state']
        else:
            self.label.text = 'unknown'


class StateTriangleLVS(TriangleLVS):

    def __init__(self, **kwargs):

        super(StateTriangleLVS, self).__init__(**kwargs)

        if 'state' in kwargs:
            self.label.text = kwargs['state']
        else:
            self.label.text = 'unknown'

    def on_touch_down(self, touch):
        print 'triangle touch', touch.pos
        return super(StateTriangleLVS, self).on_touch_down(touch)
#        if self.collide_point(touch.pos[0], touch.pos[1]):
#            for i, p in enumerate(zip(self.statechart.app.points[::2],
#                                      self.statechart.app.points[1::2])):
#                if (
#                        abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
#                        abs(touch.pos[1] - self.pos[1] - p[1]) < self.d):
#                    self.current_point = i + 1
#                    return True
#            return super(BezierTest, self).on_touch_down(touch)
#


class AddingShape(State):
    '''The AddingShape state is a transient state -- after adding the shape,
    there is an immediate transition back to the ShowingDrawingArea state, and
    its substate, WaitingForTouches.'''

    def __init__(self, **kwargs):
        super(AddingShape, self).__init__(**kwargs)

    def enter_state(self, context=None):

        touch = self.statechart.app.touch

        with self.statechart.app.drawing_area.canvas.after:
            Color(1, 1, 0)
            d = 100.
            #RectangleLIS(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d),
                    #x=touch.x, y=touch.y, width=100.0, height=100.0,
                    #line_color=[1.0, .3, .2, .5], fill_color=[.4, .4, .4, .4])
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            shape = StateTriangleLVS(pos=(touch.x - d / 2, touch.y - d / 2),
                                     size=(d, d),
                    x=touch.x, y=touch.y, width=200.0, height=200.0,
                    state="Triangle State",
                    label_placement='constrained', label_containment='inside',
                    label_anchor='left_middle', stroke_width=5.0,
                    stroke_color=[.2, .9, .2, .8], fill_color=[.4, .4, .4, .4])

            print 'shape added at', shape.pos, shape.points

            shape.generate_connection_points(10)

#            for cp in shape.connection_points:
#                Line(circle=(cp[0], cp[1], 5))

            self.statechart.app.shapes.append(shape)

#            line = Line(points=touch.pos, width=4)
#
#            if len(self.statechart.app.points):
#                line.points += self.statechart.app.points[-1]

            self.statechart.app.points.append(touch.pos)

            self.statechart.app.selected_shape = shape

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drawing_area_touch_up', ])
    def handle_touch(self, event, touch, context):

        # event == 'drawing_area_touch_up':

        self.go_to_state('ShowingDrawingArea')
