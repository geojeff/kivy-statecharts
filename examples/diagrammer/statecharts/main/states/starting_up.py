from kivy.app import App
from kivy.binding import DataBinding
from kivy.enums import binding_modes

from kivy_statecharts.system.state import State

from models.shape_tool import ShapeTool
from views.graphics.shapes import PolygonVectorShape


class StartingUp(State):

    def __init__(self, **kwargs):

        super(StartingUp, self).__init__(**kwargs)

        self.app = App.app()

    def enter_state(self, context=None):

        # Initialize controllers.
        self.app.generic_shape_tools_controller.data = [
                ShapeTool(
                    shape=PolygonVectorShape(
                        tool='generic_shape_triangle',
                        radius=20,
                        sides=3,
                        stroke_width=1.0,
                        stroke_color=[.2, .9, .2, .8],
                        fill_color=[.4, .4, .4, 1]),
                    action='generic_shape_tool_changed'),
                ShapeTool(
                    shape=PolygonVectorShape(
                        tool='generic_shape_rectangle',
                        radius=20,
                        sides=4,
                        stroke_width=1.0,
                        stroke_color=[.2, .9, .2, .8],
                        fill_color=[.4, .4, .4, 1]),
                    action='generic_shape_tool_changed'),
                ShapeTool(
                    shape=PolygonVectorShape(
                        tool='generic_shape_pentagon',
                        radius=20,
                        sides=5,
                        stroke_width=1.0,
                        stroke_color=[.2, .9, .2, .8],
                        fill_color=[.4, .4, .4, 1]),
                    action='generic_shape_tool_changed')]

        self.app.state_shape_tools_controller.data = [
            ShapeTool(
                shape=PolygonVectorShape(
                    tool='state_shape_triangle',
                    radius=20,
                    sides=3,
                    stroke_width=1.0,
                    stroke_color=[.2, .9, .2, .8],
                    fill_color=[.4, .4, .4, 1]),
                action='state_shape_tool_changed'),
            ShapeTool(
                shape=PolygonVectorShape(
                    tool='state_shape_rectangle',
                    radius=20,
                    sides=4,
                    stroke_width=1.0,
                    stroke_color=[.2, .9, .2, .8],
                    fill_color=[.4, .4, .4, 1]),
                action='state_shape_tool_changed'),
            ShapeTool(
                shape=PolygonVectorShape(
                    tool='state_shape_pentagon',
                    radius=20,
                    sides=5,
                    stroke_width=1.0,
                    stroke_color=[.2, .9, .2, .8],
                    fill_color=[.4, .4, .4, 1]),
                action='state_shape_tool_changed')]

        self.app.shape_tools_controller.data = [
                self.app.current_generic_shape_tool_controller.shape_tool_item,
                self.app.current_state_shape_tool_controller.shape_tool_item]

        self.go_to_showing_help()

    def exit_state(self, context=None):
        pass

    def go_to_showing_help(self, *args):
        self.go_to_state('ShowingHelpScreen')
