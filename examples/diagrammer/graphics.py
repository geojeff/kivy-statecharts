import os
import math
import operator
import itertools
from itertools import chain, izip

from kivy.uix.widget import Widget
from kivy.uix.listview import SelectableView

from kivy.uix.anchorlayout import AnchorLayout

from kivy.properties import AliasProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivy.graphics import Line

from kivy.lang import Builder

Builder.load_file(str(os.path.join(os.path.dirname(__file__), 'graphics.kv')))

# Abbreviation used in this file: cp == connection point


def pairwise(iterable):

    iterator = iter(iterable)
    return izip(iterator, iterator)


def cartesian_distance(x1, y1, x2, y2):
    '''Cartesian distance formula
    From:

      ftp://lnnr.lummi-nsn.gov/GIS_Scripts/CreatePointsAlongALine/DivideLine.py

    which has a print line with:

      "A Two-Bit Algorithms product
      Copyright 2011 Gerry Gabrisch
      gerry@gabrisch.us"

      (Code link: ftp://lnnr.lummi-nsn.gov/GIS_Scripts/)
    '''

    return float(math.pow(((math.pow((x2 - x1), 2)) +
                 (math.pow((y2 - y1), 2))), .5))


def cartesian_to_polar(xy1, xy2):
    '''
    From:

      ftp://lnnr.lummi-nsn.gov/GIS_Scripts/CreatePointsAlongALine/DivideLine.py

    which has a print line with:

      "A Two-Bit Algorithms product
      Copyright 2011 Gerry Gabrisch
      gerry@gabrisch.us"

    (Code link: ftp://lnnr.lummi-nsn.gov/GIS_Scripts/)

    Given coordinate pairs as two lists or tuples, return the polar
    coordinates with theta in radians. Values are in true radians along the
    unit-circle, for example, 3.14 and not -0 like a regular python
    return.'''
    try:
        x1, y1, x2, y2 = \
                float(xy1[0]), float(xy1[1]), float(xy2[0]), float(xy2[1])
        xdistance, ydistance = x2 - x1, y2 - y1
        distance = math.pow(((math.pow((x2 - x1), 2)) +
                            (math.pow((y2 - y1), 2))), .5)
        if xdistance == 0:
            if y2 > y1:
                theta = math.pi / 2
            else:
                theta = (3 * math.pi) / 2
        elif ydistance == 0:
            if x2 > x1:
                theta = 0
            else:
                theta = math.pi
        else:
            theta = math.atan(ydistance / xdistance)
            if xdistance > 0 and ydistance < 0:
                theta = 2 * math.pi + theta
            if xdistance < 0 and ydistance > 0:
                theta = math.pi + theta
            if xdistance < 0 and ydistance < 0:
                theta = math.pi + theta
        return [distance, theta]
    except:
        print"Error in cartesian_to_polar()"


def polar_to_cartesian(polarcoords):
    '''
    From:

      ftp://lnnr.lummi-nsn.gov/GIS_Scripts/CreatePointsAlongALine/DivideLine.py

    which has a print line with:

      "A Two-Bit Algorithms product
      Copyright 2011 Gerry Gabrisch
      gerry@gabrisch.us"

    (Code link: ftp://lnnr.lummi-nsn.gov/GIS_Scripts/)

    A tuple, or list, of polar values(distance, theta in radians)are
    converted to cartesian coords'''
    r = polarcoords[0]
    theta = polarcoords[1]
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return [x, y]


class ConnectionPoint(Widget):

    shapes = ListProperty()

    def __init__(self, **kwargs):
        super(ConnectionPoint, self).__init__(**kwargs)

    def can_connect(self, shape):
        if not shape in self.shapes:
            return True
        return False

    def connect(self, shape):
        if self.can_connect(shape):
            self.shapes.append(shape)
        shape.connect(self)


class Shape(SelectableView, Widget):

    stroke_width = NumericProperty(2.0)
    stroke_color = ListProperty([0, 0, 0, 0])
    fill_color = ListProperty([0, 0, 0, 0])

    x = NumericProperty(10.0)
    y = NumericProperty(10.0)
    width = NumericProperty(10.0)
    height = NumericProperty(10.0)

    #edit_button = ObjectProperty(None)

    def __init__(self, **kwargs):

        super(Shape, self).__init__(**kwargs)

        self.size_hint = (None, None)

        self.bind(is_selected=self.selection_changed)

    def selection_changed(self, *args):

        pass

#        if self.is_selected:
#
#            c = self.center()
#
#            self.edit_button = Button(
#                    pos=(c[0] + 5, c[1] - 5),
#                    size=(10, 10),
#                    text='E')
#
#            self.edit_button.bind(
#                on_release=
#                App.get_running_app().statechart.send_event('edit_shape'))
#
#            self.add_widget(self.edit_button)
#
#        else:
#
#            self.remove_widget(self.edit_button)

#    def center(self):
#        pass
        #return self.x + (self.width / 2.0), self.y + (self.height / 2.0)


class ConnectedShape(Shape):

    connection_points = ListProperty([])
    connections = ListProperty([])

    def __init__(self, **kwargs):

        super(ConnectedShape, self).__init__(**kwargs)

    def generate_connection_points(self, step_distance=10):
        pass

    def find_connection(self, shape):
        pass

    def adjust_connections(self, dx, dy):
        for connection in self.connections:
            connection.adjust(self, dx, dy)


class AnchoredLabel(AnchorLayout):

    anchor_widget = ObjectProperty
    label_anchor_layout_x = NumericProperty(1)
    label_anchor_layout_y = NumericProperty(1)

    def get_label_anchor_layout_size(self):

        return (self.label_anchor_layout_x * self.anchor_widget.width,
                self.label_anchor_layout_y * self.anchor_widget.height)

    def set_label_anchor_layout_size(self, value):

        min_width_allowed = .5 * self.anchor_widget.width
        min_height_allowed = .5 * self.anchor_widget.height
        max_width_allowed = 2. * self.anchor_widget.width
        max_height_allowed = 2. * self.anchor_widget.height

        if value[0] < min_width_allowed:
            value[0] = min_width_allowed
        elif value[0] > max_width_allowed:
            value[0] = max_width_allowed

        if value[1] < min_height_allowed:
            value[1] = min_height_allowed
        elif value[1] > max_height_allowed:
            value[1] = max_height_allowed

        self.label_anchor_layout_x = self.anchor_widget.width / value[0]
        self.label_anchor_layout_y = self.anchor_widget.height / value[1]

    def get_label_anchor_layout_pos(self):

        size = self.label_anchor_layout_size

        pos_change_x = 0
        pos_change_y = 0

        if size[0] > self.anchor_widget.width:
            margin = size[0] - self.anchor_widget.width
            pos_change_x = (margin / 2.) * -.1

        if size[1] > self.anchor_widget.height:
            margin = size[1] - self.anchor_widget.height
            pos_change_y = (margin / 2.) * -.1

        return tuple(map(operator.add, self.anchor_widget.pos, (pos_change_x,
                                                                pos_change_y)))

    def set_label_anchor_layout_pos(self, value):

        pos_difference = tuple(map(
            operator.sub, self.anchor_widget.pos, value))

        self.label_anchor_layout_x = \
            self.anchor_widget.width / self.anchor_widget.width \
            + pos_difference[0]
        self.label_anchor_layout_y = \
            self.anchor_widget.height / self.anchor_widget.width \
            + pos_difference[0]

    label_anchor_layout_pos = \
            AliasProperty(get_label_anchor_layout_pos,
                          set_label_anchor_layout_pos,
                          bind=('label_anchor_layout_x',
                                'label_anchor_layout_y'))

    label_anchor_layout_size = \
            AliasProperty(get_label_anchor_layout_size,
                          set_label_anchor_layout_size,
                          bind=('label_anchor_layout_x',
                                'label_anchor_layout_y'))

    label_anchor_x = StringProperty('center')
    label_anchor_y = StringProperty('center')

    def __init__(self, **kwargs):

        self.anchor_widget = kwargs['anchor_widget']

        super(AnchoredLabel, self).__init__(**kwargs)

        self.label_anchor_layout_pos = self.anchor_widget.pos
        self.label_anchor_layout_size = self.anchor_widget.size

        self.label.text = kwargs['text']


class VectorShape(ConnectedShape):

    points = ListProperty([])
    unit_circle_points = ListProperty([])
    cp_slices_for_edges = ListProperty([])

    def __init__(self, **kwargs):
        super(VectorShape, self).__init__(**kwargs)

        self.bind(size=self.recalculate_points)

    def shift_unit_circle_points_to_origin(self):

        x_values = self.unit_circle_points[::2]
        y_values = self.unit_circle_points[1::2]

        min_x = min(x_values)
        min_y = min(y_values)

        min_x = 0 if min_x > 0 else min_x * -1.
        min_y = 0 if min_y > 0 else min_y * -1.

        # Shift from unit circle to pos.
        x_values_pos = [x + min_x for x in x_values]
        y_values_pos = [y + min_y for y in y_values]

        max_x = max(x_values_pos)
        max_y = max(y_values_pos)

        # Normalize to max value 1.
        return list(
                chain.from_iterable(izip([x / max_x for x in x_values_pos],
                                         [y / max_y for y in y_values_pos])))

    def recalculate_points(self, *args):
        pass

    # http://stackoverflow.com/...
    #   questions/849211/shortest-distance-between-a-point-and-a-line-segment
    def dist(self, x1, y1, x2, y2, x3, y3):  # x3,y3 is the point
        px = x2 - x1
        py = y2 - y1

        something = px * px + py * py

        u = ((x3 - x1) * px + (y3 - y1) * py) / float(something)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = x1 + u * px
        y = y1 + u * py

        dx = x - x3
        dy = y - y3

        # Note: If the actual distance does not matter,
        # if you only want to compare what this function
        # returns to other results of this function, you
        # can just return the squared distance instead
        # (i.e. remove the sqrt) to gain a little performance

        dist = math.sqrt(dx * dx + dy * dy)

        return dist

    def point_on_polygon(self, x, y, min_dist):
        x, y = self.to_local(x, y)
        poly = self.points

        n = len(poly)
        p1x = poly[0]
        p1y = poly[1]

        for i in xrange(2, n + 2, 2):
            p2x = poly[i % n]
            p2y = poly[(i + 1) % n]

            dist = self.dist(p1x, p1y, p2x, p2y, x, y)
            #print '    distance', dist, p1x, p1y, '-->', p2x, p2y
            if dist < min_dist:
                return True
            p1x, p1y = p2x, p2y

        return False

    def closest_edge(self, x, y):
        x, y = self.to_local(x, y)
        poly = self.points

        n = len(poly)
        p1x = poly[0]
        p1y = poly[1]

        # edge here is the index into poly.

        minimum_and_edge = [100000, 0]

        for i in xrange(2, n + 2, 2):
            p2x = poly[i % n]
            p2y = poly[(i + 1) % n]

            dist = self.dist(p1x, p1y, p2x, p2y, x, y)
            #print '        possible distance', dist, p1x, p1y, '-->', p2x, p2y
            if dist < minimum_and_edge[0]:
                minimum_and_edge = [dist, i]
            p1x, p1y = p2x, p2y

        return minimum_and_edge

    def point_inside_polygon(self, x, y, poly):
        '''Taken from http://www.ariel.com.au/a/python-point-int-poly.html
        '''
        n = len(poly)
        inside = False
        p1x = poly[0]
        p1y = poly[1]

        for i in xrange(2, n + 2, 2):

            p2x = poly[i % n]
            p2y = poly[(i + 1) % n]

            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = \
                                    (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    def collide_point(self, x, y):
        x, y = self.to_local(x, y)
        return self.point_inside_polygon(x, y, self.points)

#    def center(self):
#        x_values = self.points[::2]
#        y_values = self.points[1::2]
#
#        min_x = min(x_values)
#        max_x = max(x_values)
#        min_y = min(y_values)
#        max_y = max(y_values)
#
#        return (self.pos[0] + ((max_x - min_x) / 2.),
#                self.pos[1] + ((max_y - min_y) / 2.))

    def generate_connection_points(self, step_distance=10):
        poly = self.points

        n = len(poly)
        x1 = poly[0]
        y1 = poly[1]

        self.connection_points.append([x1, y1])

        distance_remaining = []

        # Reference:
        #
        # A Two-Bit Algorithms product
        # Copyright 2011 Gerry Gabrisch
        # gerry@gabrisch.us"
        #
        # http://forums.arcgis.com/threads/9118- ...
        #   Placing-points-automatically-along-line-based-on-length-attribute
        # (Code link: ftp://lnnr.lummi-nsn.gov/GIS_Scripts/)

        step_distance = float(step_distance)

        counter = 0

        for i in xrange(2, n + 2, 2):
            x2 = poly[i % n]
            y2 = poly[(i + 1) % n]

            try:
                distance_along_line = cartesian_distance(x1, y1, x2, y2) + \
                                      distance_remaining[counter - 1]
            except:
                distance_along_line = cartesian_distance(x1, y1, x2, y2)

            if distance_along_line == step_distance:

                # If the line segment is short, matching exactly the
                # step_distance, we only need to store the start and end of the
                # line segment as a single point (there is only one connection
                # point -- the end of the line segment, which we add first).

                self.connection_points.append([x2, y2])
                self.cp_slices_for_edges.append(
                        (len(self.connection_points) - 1,
                         len(self.connection_points) - 1))
                distance_remaining.append(0)

            elif distance_along_line > step_distance:

                # If the line segment is longer than step_distance, there are
                # connection points along the line segment. We create these
                # points and set the start and end indices.

                number_divisions = int(distance_along_line / step_distance)
                distance_remaining.append(
                    distance_along_line - (number_divisions * step_distance))
                polarcoord = cartesian_to_polar((x1, y1), (x2, y2))

                cps_start_index = len(self.connection_points)

                counter2 = 1
                while counter2 <= number_divisions:
                    if len(distance_remaining) > 1:
                        adjustment = polar_to_cartesian([
                            ((step_distance * counter2) -
                                    distance_remaining[counter - 1]),
                            polarcoord[1]])
                    else:
                        adjustment = polar_to_cartesian([
                            ((step_distance * counter2)),
                            polarcoord[1]])
                    self.connection_points.append(
                            [x1 + adjustment[0], y1 + adjustment[1]])
                    counter2 += 1

                cps_end_index = len(self.connection_points) - 1

                self.cp_slices_for_edges.append(
                        (cps_start_index, cps_end_index))

            elif distance_along_line < step_distance:

                # If the distance along the line segment is shorter than the
                # step_distance, store the short remainder distance for use in
                # the next line segment's calculations.

                if len(distance_remaining) < 1:
                    distance_remaining.append(distance_along_line)
                else:
                    distance_remaining.append(distance_along_line)

            x1, y1 = x2, y2

    def closest_cp_to_center_line(self, shape2):
        '''Return the index of the closest cp to the center line between self
        and shape2.
        '''

        center1 = self.center
        center2 = shape2.center

        min_distance = 100000.

        for i, cp in enumerate(self.connection_points):

            dist = self.dist(
                    center1[0], center1[1], center2[0], center2[1],
                    cp[0], cp[1])

            if dist < min_distance:
                min_distance = dist
                closest_cp = i

        return closest_cp

        #for point in self.connection_points:
        #    if (point.pos[0]
        #          < shape.label.pos[0] and
        #        point.pos[0]
        #          > shape.label.pos[0] + shape.label.texture.size[0] and
        #        point.pos[1]
        #          < shape.label.pos[1] and
        #        point.pos[1]
        #          > shape.label.pos[1] + shape.label.texture.size[1]):
        #        print point

    def draw_connection_points(self):
        for cp in self.connection_points:
            Line(circle=(cp[0], cp[1], 5))

    def draw_connection_point(self, index):
        cp = self.connection_points[index]
        Line(circle=(cp[0], cp[1], 5))

    def vertices(self, origin=None):
        '''Return vertices for Mesh.'''
        pass

    def indices(self):
        '''Return indices for Mesh.'''
        pass


class ConnectionVectorShape(VectorShape):
    shape = ListProperty([.9, .9])
    shape1 = ObjectProperty(None)
    shape2 = ObjectProperty(None)
    shape1_cp_index = NumericProperty()
    shape2_cp_index = NumericProperty()

    def __init__(self, **kwargs):

        super(ConnectionVectorShape, self).__init__(**kwargs)

        #if 'text' in kwargs:
            #self.label.text = kwargs['text']
        #else:
            #self.label.text = 'unknown'

        self.points.append(
                self.shape1.connection_points[self.shape1_cp_index][0])
        self.points.append(
                self.shape1.connection_points[self.shape1_cp_index][1])
        self.points.append(
                self.shape2.connection_points[self.shape2_cp_index][0])
        self.points.append(
                self.shape2.connection_points[self.shape2_cp_index][1])

    def on_touch_down(self, touch):
        return super(VectorShape, self).on_touch_down(touch)

    def adjust(self, shape, dx, dy):
        connection_point1 = self.shape1.connection_points[self.shape1_cp_index]
        self.pos[0] = connection_point1[0]
        self.pos[1] = connection_point1[1]

        if shape == self.shape1:
            self.x += dx
            self.y += dy

        self.points[0] = self.pos[0]
        self.points[1] = self.pos[1]

        connection_point2 = self.shape2.connection_points[self.shape2_cp_index]

        self.width = connection_point2[0] - connection_point1[0]
        self.height = connection_point2[1] - connection_point1[1]

        self.points[2] = self.pos[0] + self.width
        self.points[3] = self.pos[1] + self.height

        self.size = (self.width, self.height)

    def recalculate_points(self, *args):
        pass

        # TODO: This was present before the refactor to PolygonVectorShape and
        #       the use of vertices /indices. The line was incorrectly being
        #       shortened dramatically on one end. So, if needed, this is now
        #       wrong.

        #self.points[0] = self.pos[0] + int(float(self.size[0]) * self.shape[0])
        #self.points[1] = self.pos[1] + int(float(self.size[1]) * self.shape[1])

    def vertices(self, origin=None, for_perimeter=False):
        '''For now, just return the two end points. See comment in indices().
        '''

        return self.points

    def indices(self):
        '''Return indices for Mesh.

        TODO: Now we treat the connection as a line, but it could be a polygon
              such as a line with width (fill possible) and with arrowheads on
              one end or the other. For now, just make the Mesh happy.
        '''

        return range(2)

    def connection_point1(self):
        return self.shape1.connection_points[self.shape1_cp_index]

    def connection_point2(self):
        return self.shape2.connection_points[self.shape2_cp_index]

    def bump_connection_point1(self):

        old_connection_point = \
                self.shape1.connection_points[self.shape1_cp_index]

        if self.shape1_cp_index < len(self.shape1.connection_points) - 1:
            self.shape1_cp_index += 1
        else:
            self.shape1_cp_index = 0

        new_connection_point = \
                self.shape1.connection_points[self.shape1_cp_index]

        dx = new_connection_point[0] - old_connection_point[0]
        dy = new_connection_point[1] - old_connection_point[1]

        self.adjust(self.shape1, dx, dy)

    def bump_connection_point2(self):

        old_connection_point = \
                self.shape2.connection_points[self.shape2_cp_index]

        if self.shape2_cp_index < len(self.shape2.connection_points) - 1:
            self.shape2_cp_index += 1
        else:
            self.shape2_cp_index = 0

        new_connection_point = \
                self.shape2.connection_points[self.shape2_cp_index]

        dx = new_connection_point[0] - old_connection_point[0]
        dy = new_connection_point[1] - old_connection_point[1]

        self.adjust(self.shape2, dx, dy)


class PolygonVectorShape(VectorShape):
    '''The points list is recalculated if size changes (see superclass), so it
    may be used when efficiency is a concern. If the vertices() method is
    called directly, with an origin given as some pos, the vertices will be
    calculated freshly.'''

    origin = ListProperty([0.0, 0.0])
    radius = NumericProperty(50)
    sides = NumericProperty(3)

    def __init__(self, **kwargs):
        super(PolygonVectorShape, self).__init__(**kwargs)

        self.points = [0] * (self.sides * 2)

        self.recalculate_points()

    def recalculate_points(self, *args):

        self.unit_circle_points = self.vertices(for_perimeter=True)

        self.unit_circle_points = self.shift_unit_circle_points_to_origin()

        w = self.size[0]
        h = self.size[1]
        pos_x = self.pos[0]
        pos_y = self.pos[1]

        x_mult_values = self.unit_circle_points[::2]
        y_mult_values = self.unit_circle_points[1::2]

        self.points = list(
                chain.from_iterable(izip(
                    [pos_x + w * mult_x for mult_x in x_mult_values],
                    [pos_y + h * mult_y for mult_y in y_mult_values])))

        # TODO: Resolve the mismatch between vertices and points (fill not
        # full size, or points spread too large).

        #x_values = self.points[::2]
        #y_values = self.points[1::2]

        #print 'w=', max(x_values) - min(x_values)
        #print 'h=', max(y_values) - min(y_values)

    def vertices(self, origin=None, for_perimeter=False):
        '''Return vertices for perimeter or Mesh.'''

        if not origin:
            origin = self.origin

        if for_perimeter:

            radius = 1

            return list(itertools.chain(*[
                            (radius * math.cos(2 * math.pi * i / self.sides),
                             radius * math.sin(2 * math.pi * i / self.sides))
                                for i in range(self.sides)]))
        else:

            vertices = list(itertools.chain(*[
                           ((origin[0])
                                + math.cos(i * ((2 * math.pi) / self.sides))
                                    * self.radius,
                            (origin[1])
                                + math.sin(i * ((2 * math.pi) / self.sides))
                                    * self.radius,
                            math.cos(i * ((2 * math.pi) / self.sides)),
                            math.sin(i * ((2 * math.pi) / self.sides)))
                                for i in xrange(self.sides)]))

            # TODO: Resolve the mismatch between vertices and points (fill not
            # full size, or points spread too large).

            #x_values1 = vertices[::2]
            #x_values = x_values1[::2]
            #y_values1 = vertices[1::2]
            #y_values = y_values1[::2]

            #print 'wv=', max(x_values) - min(x_values)
            #print 'hv=', max(y_values) - min(y_values)

            return vertices

    def indices(self):
        '''Return indices for Mesh.'''

        return range(self.sides)
