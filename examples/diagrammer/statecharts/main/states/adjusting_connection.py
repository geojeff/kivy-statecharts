from kivy.app import App

from kivy_statecharts.system.state import State

from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

Builder.load_string('''
<ConnectionBubble>
    size_hint: (None, None)
    size: (150, 40)
    pos_hint: {'center_x': .5, 'y': .6}
    arrow_pos: 'bottom_mid'
    orientation: 'horizontal'
    padding: 4, 0, 4, 0
    spacing: 3
#    canvas.before:
#        Color:
#            rgba: self.background_color
#        Rectangle:
#            size: self.size
#            pos: self.pos
#    ConnectionPointBubbleButton:
#        text: 'Drag'
#        on_press: root.statechart.send_event('drag_for_point')
#    ConnectionPointBubbleButton:
#        text: 'Accept'
#        on_press: root.statechart.send_event('accept_point')
''')


class ConnectionPointDragButton(Button):

    statechart = ObjectProperty(None)
    action = StringProperty('')

    def __init__(self, statechart, action, **kwargs):
        self.statechart = statechart
        self.action = action
        super(ConnectionPointDragButton, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print 'CPDB DDDDDDDDDOOOOOOOOOWWWWWWWWWWNNNNNNNN'
        return super(ConnectionPointDragButton, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        print 'CPDB MOVE'
        if self.collide_point(*touch.pos):
            self.statechart.send_event(self.action, touch)

        return super(ConnectionPointDragButton, self).on_touch_move(touch)

        # in Button
        #if touch.grab_current is self:
        #    return True
        #if super(Button, self).on_touch_move(touch):
        #    return True
        #return self in touch.ud


class ConnectionPointAcceptButton(Button):

    statechart = ObjectProperty(None)
    action = StringProperty('')

    def __init__(self, statechart, action, **kwargs):
        self.statechart = statechart
        self.action = action
        super(ConnectionPointAcceptButton, self).__init__(**kwargs)

    def on_touch_up(self, touch):

        if self.collide_point(*touch.pos):
            self.statechart.send_event(self.action, touch)

        return super(ConnectionPointAcceptButton, self).on_touch_up(touch)


class ConnectionBubble(Bubble):

    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_up',
                          'drawing_area_touch_move', ])
    def handle_touch(self, event, touch, context):

        print 'ConnectionBubble', event


class AdjustingConnection(State):
    '''The AdjustingConnection state shows bubbles on either end of a
    provisional connection, allowing for dragging to the desired connection
    point. Upon finalization, or cancelling, we go back to
    ShowingDrawingScreen.
    '''

    drawing_area = ObjectProperty(None, allownone=True)

    connection_bubble1 = ObjectProperty(None, allownone=True)
    connection_bubble2 = ObjectProperty(None, allownone=True)

    dragging_op1 = BooleanProperty(False)
    dragging_op2 = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(AdjustingConnection, self).__init__(**kwargs)

    def enter_state(self, context=None):

        self.app = App.get_running_app()

        self.drawing_area = \
                self.app.screen_manager.current_screen.drawing_area

        point1 = self.app.adjusting_connection.connection_point1()
        point2 = self.app.adjusting_connection.connection_point2()

        self.connection_bubble1 = ConnectionBubble(
                pos=(point1[0] - 75, point1[1]),
                background_image='design/images/DiagrammerBubble.png',
                background_color=(1, 0, 0, 1),
                arrow_image='design/images/DiagrammerBubbleArrow.png')

        self.connection_bubble1.add_widget(ConnectionPointDragButton(
                self.statechart, 'drag_connection_point1', text='Drag'))

        self.connection_bubble1.add_widget(ConnectionPointAcceptButton(
                self.statechart, 'accept_connection_point1', text='Accept'))

        self.drawing_area.add_widget(self.connection_bubble1)

        self.connection_bubble2 = ConnectionBubble(
                pos=(point2[0] - 75, point2[1]),
                background_image='design/images/DiagrammerBubble.png',
                background_color=(1, 0, 0, 1),
                arrow_image='design/images/DiagrammerBubbleArrow.png')

        self.connection_bubble2.add_widget(ConnectionPointDragButton(
                self.statechart, 'drag_connection_point2', text='Drag'))

        self.connection_bubble2.add_widget(ConnectionPointAcceptButton(
                self.statechart, 'accept_connection_point2', text='Accept'))

        self.drawing_area.add_widget(self.connection_bubble2)

    def exit_state(self, context=None):
        pass

    @State.event_handler(['drag_connection_point1',
                          'drag_connection_point2', ])
    def drag_connection_point(self, event, touch, context):

        connection = self.app.connections_controller.last()

        if event == 'drag_connection_point1':
            dragging_op = self.dragging_op1
            bubble = self.connection_bubble1
            old_index = connection.shape1_cp_index
            connection.bump_connection_point1()
            shape = connection.shape1
            new_index = connection.shape1_cp_index
            point = connection.connection_point1()
        else:
            dragging_op = self.dragging_op2
            bubble = self.connection_bubble2
            old_index = connection.shape2_cp_index
            connection.bump_connection_point2()
            shape = connection.shape2
            new_index = connection.shape2_cp_index
            point = connection.connection_point2()

        if not dragging_op:
            dragging_op = True

        with self.drawing_area.canvas.before:

            # Draw connection_points.
            Color(1, 1, 0)
            shape.draw_connection_points()

            # Handle highlighting of connection point.
            shape.draw_connection_point(old_index)
            Color(1, 0, 0)
            shape.draw_connection_point(new_index)

            # Move the bubble.
            bubble.pos = (point[0] - 75, point[1])

    def accept_connection_point1(self, *args):

        connection = self.app.connections_controller.last()

        self.drawing_area.remove_widget(connection.shape1)
        self.drawing_area.remove_widget(self.connection_bubble1)
        self.connection_bubble1 = None
        self.dragging_op1 = False

        # TODO: Need a better way to clear -- perhaps call clear() on after?
        #       Perhaps then it won't be necessary to remove/add the shape.

        with self.drawing_area.canvas.before:

            # Draw connection_points.
            Color(0, 0, 0)
            connection.shape1.draw_connection_points()

        self.drawing_area.add_widget(connection.shape1)

        if not self.connection_bubble2:
            self.go_to_state('ShowingDrawingScreen')

    def accept_connection_point2(self, *args):

        connection = self.app.connections_controller.last()

        self.drawing_area.remove_widget(connection.shape2)
        self.drawing_area.remove_widget(self.connection_bubble2)
        self.connection_bubble2 = None
        self.dragging_op2 = False

        # TODO: Need a better way to clear -- perhaps call clear() on after?
        #       Perhaps then it won't be necessary to remove/add the shape.

        with self.drawing_area.canvas.before:

            # Draw connection_points.
            Color(0, 0, 0)
            connection.shape2.draw_connection_points()

        self.drawing_area.add_widget(connection.shape2)

        if not self.connection_bubble1:
            self.go_to_state('ShowingDrawingScreen')

    # Consume drawing_area touch events while this state is current.
    @State.event_handler(['drawing_area_touch_down',
                          'drawing_area_touch_up',
                          'drawing_area_touch_move', ])
    def handle_touch(self, event, touch, context):
        print 'drawing_area touch in connection bubbles...'
