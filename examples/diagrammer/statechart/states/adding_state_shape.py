import copy

from kivy.app import App

from kivy_statecharts.system.state import State

from kivy.graphics import Color

from kivy.uix.label import Label

from state_graphics import StateTriangleVectorShape
from state_graphics import StateRectangleVectorShape
from state_graphics import StatePentagonVectorShape


class AddingStateShape(State):
    '''The AddingStateShape state is a transient state -- after adding the
    shape, there is an immediate transition back to the ShowingDrawingScreen
    state.
    '''

    def __init__(self, **kwargs):
        super(AddingStateShape, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def enter_state(self, context=None):

        touch = self.app.touch

        # TODO: Finish other shapes.

        drawing_area = \
                self.app.screen_manager.current_screen.drawing_area

        shape_cls = self.app.state_shape_tools_adapter.current_shape.__class__
        radius = self.app.state_shape_tools_adapter.current_shape.radius
        sides = self.app.state_shape_tools_adapter.current_shape.sides

        with drawing_area.canvas.before:
            Color(1, 1, 0)
            d = 100.
            #shape = copy.deepcopy(self.app.state_shape_tools_adapter.current_shape)
            #shape.pos = (touch.x, touch.y)
            #shape.size = (d, d)
            #shape.stroke_width = 5.0
            #shape.stroke_color = [.2, .9, .2, .8]
            #shape.fill_color = [.4, .4, .4, .4]
            #shape.add_widget(Label(text="Some State", pos=shape.pos))
            #shape.recalculate_points()

            #RectangleImageShape(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d),
                    #x=touch.x, y=touch.y, width=100.0, height=100.0,
                    #line_color=[1.0, .3, .2, .5], fill_color=[.4, .4, .4, .4])
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            shape = shape_cls(
                    #pos=(touch.x - d / 2, touch.y - d / 2),
                    pos=(touch.x, touch.y),
                    size=(d, d),
                    radius=radius,
                    sides=sides,
                    #x=touch.x, y=touch.y, width=100.0, height=100.0,
                    stroke_width=5.0,
                    stroke_color=[.2, .9, .2, .8], fill_color=[.4, .4, .4, .4])

            #shape.add_widget(AnchoredLabel(
            #        anchor_widget=shape,
            #        text="Some State",
            #        label_anchor_x='left',
            #        label_anchor_y='bottom'))

            shape.generate_connection_points(10)

            self.app.shapes_controller.content.append(shape)

            self.app.shapes_controller.handle_selection(shape)

            print self.app.current_shape_controller.content
            print self.app.shapes_controller.selection

            self.go_to_state('ShowingDrawingScreen')

    def exit_state(self, context=None):
        pass
