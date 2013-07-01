from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from graphics import RectangleImageShape
from graphics import TriangleImageShape
from graphics import PolygonVectorShape


class StateRectangleImageShape(RectangleImageShape):

    def __init__(self, **kwargs):

        super(StateRectangleImageShape, self).__init__(**kwargs)

        if 'state' in kwargs:
            self.label.text = kwargs['state']


class StateTriangleImageShape(TriangleImageShape):

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

        super(StateTriangleImageShape, self).__init__(**kwargs)

class StateShape(object):

    state = ObjectProperty(None)

    def __init__(self, **kwargs):

        super(StateShape, self).__init__(**kwargs)


class StateTriangleVectorShape(StateShape, PolygonVectorShape):

    def __init__(self, **kwargs):

        kwargs['sides'] = 3

        super(StateTriangleVectorShape, self).__init__(**kwargs)


class StateRectangleVectorShape(StateShape, PolygonVectorShape):

    def __init__(self, **kwargs):

        kwargs['sides'] = 3

        super(StateRectangleVectorShape, self).__init__(**kwargs)


class StatePentagonVectorShape(StateShape, PolygonVectorShape):

    def __init__(self, **kwargs):

        kwargs['sides'] = 3

        super(StatePentagonVectorShape, self).__init__(**kwargs)


#    def on_touch_down(self, touch):
#        print 'triangle touch', touch.pos
#        return super(StateTriangleVectorShape, self).on_touch_down(touch)
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
