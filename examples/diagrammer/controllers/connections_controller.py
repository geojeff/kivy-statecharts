from kivy_statecharts.system.controllers.list_controller import ListController

class ConnectionsController(ListController):

    # content property holds the data

    # A silly example of the type of filtering that is done by controllers.
    def blue_connections(self):

        return [s for s in self if s.fill_color[2] > .5]

    # See ShapesController for some discussion.
