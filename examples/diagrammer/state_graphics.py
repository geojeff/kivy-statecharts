from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from graphics import PolygonVectorShape


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

        kwargs['sides'] = 4

        super(StateRectangleVectorShape, self).__init__(**kwargs)


class StatePentagonVectorShape(StateShape, PolygonVectorShape):

    def __init__(self, **kwargs):

        kwargs['sides'] = 5

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
