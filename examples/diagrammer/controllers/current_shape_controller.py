from kivy_statecharts.system.controllers.object_controller \
        import ObjectController


class CurrentShapeController(ObjectController):

    # content property holds the data

    def __init__(self, **kwargs):

        super(CurrentShapeController, self).__init__(**kwargs)
