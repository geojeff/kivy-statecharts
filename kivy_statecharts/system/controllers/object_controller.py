from kivy_statecharts.system.controllers.controller import Controller

class ObjectController(Controller):

    # content, from Controller, is an ObjectProperty

    def __init__(self, **kwargs):

        super(ObjectController, self).__init__(**kwargs)

    # Enhance for bindings to list controllers.

    # Add transformation methods.

    def update(self, *args):
        # args:
        #
        #     controller args[0]
        #     value      args[1]
        #     op_info    args[2]

        value = args[1]

        if isinstance(value, list):
            if value:
                self.content = value[0]
            else:
                self.content = None
        else:
            self.content = value
