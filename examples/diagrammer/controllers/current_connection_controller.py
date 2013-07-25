from kivy_statecharts.system.controllers.object_controller \
        import ObjectController


class CurrentConnectionController(ObjectController):

    # content property holds the data

    def __init__(self, **kwargs):

        super(CurrentConnectionController, self).__init__(**kwargs)

