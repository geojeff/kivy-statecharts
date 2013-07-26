from kivy_statecharts.system.controllers.list_controller import ListController


class ShapesController(ListController):

    # content property holds the data

    # A silly example of the type of filtering that is done by controllers.
    def blue_shapes(self):

        return [s for s in self.content if s.fill_color[2] > .5]

    # An idea for a filtering method is ... perhaps ...  def
    # closest_to_selected(), which would update on selection to only include
    # shapes that will within a distance to selected shape.

    # Alias properties, analagous to computed properties in Cocoa / Sproutcore,
    # will come into play here.
