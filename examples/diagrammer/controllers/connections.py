from kivy.controllers.listcontroller import ListController


class ConnectionsController(ListController):

    # A silly example of the type of filtering that is done by controllers.
    def blue_connections(self):

        return [s for s in self.data if s.fill_color[2] > .5]

    # See ShapesController for some discussion.
