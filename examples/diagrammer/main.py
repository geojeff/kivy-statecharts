import kivy
kivy.require('1.6.0')

import random

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

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
#            for i, p in enumerate(zip(self.points[::2], self.points[1::2])):
#                if (
#                        abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
#                        abs(touch.pos[1] - self.pos[1] - p[1]) < self.d):
#                    self.current_point = i + 1
#                    return True
#            return super(BezierTest, self).on_touch_down(touch)
#

class RootWidget(GridLayout):

    bg = ObjectProperty(None)
    connector = ObjectProperty(None)
    connector_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.bg.bind(points=self.points_added)

    def points_added(self, *args):
        #print self.bg.points
        pass


class DrawingArea(Image):

    points = ListProperty()
    shapes = ListProperty()
    connections = ListProperty()

    connecting_shape = ObjectProperty(None, allownone=True)
    moving_shape = ObjectProperty(None, allownone=True)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):

            shape_selected = False

            print
            print 'touch', touch.pos, 'shapes = ', len(self.shapes)
            for shape in reversed(self.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    print 'polygon touched', shape.canvas
                    dist, line = shape.closest_line_segment(touch.pos[0], touch.pos[1])
                    print 'closest line segment', dist, line
                    shape_selected = True
                    self.moving_shape = shape
                    break
                elif shape.collide_point(*touch.pos):
                    print 'shape touched', shape.canvas
                    shape_selected = True
                    self.connecting_shape = shape
                    break

            if not shape_selected:
                with self.canvas.after:
                    Color(1, 1, 0)
                    d = 100.
                    #RectangleLIS(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d),
                            #x=touch.x, y=touch.y, width=100.0, height=100.0,
                            #line_color=[1.0, .3, .2, .5], fill_color=[.4, .4, .4, .4])
                    #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                    shape = StateTriangleLVS(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d),
                            x=touch.x, y=touch.y, width=200.0, height=200.0,
                            state="Triangle State",
                            label_placement='constrained', label_containment='inside',
                            label_anchor='left_middle', stroke_width=5.0,
                            stroke_color=[.2, .9, .2, .8], fill_color=[.4, .4, .4, .4])
                    print 'shape added at', shape.pos, shape.points
                    shape.generate_connection_points(10)
                    for cp in shape.connection_points:
                        Line(circle=(cp[0], cp[1], 5))
                    self.shapes.append(shape)
                    line = Line(points=touch.pos, width=4)
                    if len(self.points):
                        line.points += self.points[-1]
                    self.points.append(touch.pos)

                    shape_selected = True

            if shape_selected:
                return True

        return super(DrawingArea, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if self.collide_point(*touch.pos):

            print
            print 'touch', touch.pos, 'shapes = ', len(self.shapes)
            #if not self.moving_shape:
            #    for shape in reversed(self.shapes):
            #        if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
            #            print 'polygon touched', shape.canvas
            #            dist, line = shape.closest_line_segment(touch.pos[0], touch.pos[1])
            #            print 'closest line segment', dist, line
            #            self.moving_shape = shape
            #            break

            if self.moving_shape:
                self.moving_shape.x += touch.dx
                self.moving_shape.y += touch.dy
                self.moving_shape.recalculate_points()

        #return super(DrawingArea, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        shape_found = False

        if self.connecting_shape:
            for shape in reversed(self.shapes):
                if shape.collide_point(*touch.pos):
                    print 'shape touched', shape.canvas
                    shape_found = shape
                    break

            for shape in reversed(self.shapes):
                if shape.point_on_polygon(touch.pos[0], touch.pos[1], 10):
                    print 'polygon touched', shape.canvas
                    dist, line = shape.closest_line_segment(touch.pos[0], touch.pos[1])
                    print 'closest line segment', dist, line
                    shape_found = shape
                    break

            if shape_found:
                self.connect(self.connecting_shape, shape_found)

        self.connecting_shape = None
        self.moving_shape = None

        return super(DrawingArea, self).on_touch_up(touch)

    def clear_points(self):
        self.points = []
        self.canvas.after.clear()

    def connect(self, shape1, shape2):
        point1, point2 = shape1.find_connection(shape2)

        print 'connection found', point1, point2
        points = [point1[0], point1[1], point2[0], point2[1]]
        with self.canvas.after:
            Color(1, 1, 0)
            d = 100.
            Line(points=points, width=4)


class DiagrammerApp(App):
    def build(self):
        root = RootWidget()
        return root


if __name__ in ('__main__', '__android__'):
    DiagrammerApp().run()
